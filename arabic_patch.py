# arabic_patch.py
"""
Arabic support for Kivy:
✔ Static text (Label / Button)
✔ Real-time TextInput (safe)
✔ hint_text support
"""

import re
import arabic_reshaper
from bidi.algorithm import get_display


# =========================
# Helpers
# =========================

ARABIC_RE = re.compile(
    r'[\u0600-\u06FF\u0750-\u077F\u08A0-\u08FF\uFB50-\uFDFF\uFE70-\uFEFF]'
)

def contains_arabic(text):
    return bool(text and ARABIC_RE.search(text))


def shape_arabic(text):
    if not text or not contains_arabic(text):
        return text
    try:
        reshaped = arabic_reshaper.reshape(text)
        return get_display(reshaped)
    except:
        return text


# =========================
# Init
# =========================

def init_arabic_support():
    print("🔧 Arabic support enabled (COMPLETE FIX)...")

    from kivy.uix.label import Label
    from kivy.uix.button import Button
    from kivy.uix.textinput import TextInput


    # -------------------------------------------------
    # STATIC TEXT (Label / Button)
    # -------------------------------------------------

    def patch_static(widget_cls):
        original_init = widget_cls.__init__

        def new_init(self, **kwargs):
            self._arabic_lock = False
            original_init(self, **kwargs)

            def on_text(instance, value):
                if instance._arabic_lock:
                    return
                if not contains_arabic(value):
                    return

                instance._arabic_lock = True
                instance.text = shape_arabic(value)
                instance._arabic_lock = False

            self.bind(text=on_text)

        widget_cls.__init__ = new_init


    patch_static(Label)
    patch_static(Button)


    # -------------------------------------------------
    # TEXTINPUT (COMPLETE FIX)
    # -------------------------------------------------

    original_textinput_init = TextInput.__init__

    def new_textinput_init(self, **kwargs):
        # معالجة hint_text في الإعداد الأولي
        if 'hint_text' in kwargs:
            kwargs['hint_text'] = shape_arabic(kwargs['hint_text'])

        original_textinput_init(self, **kwargs)

        # إعدادات الخط والمحاذاة
        self.font_name = 'AwanZaman'  # تأكد من تثبيت هذا الخط أو استبداله بخط عربي آخر
        self.halign = 'right'
        self.padding = [10, 10, 10, 10]
        self.multiline = True

        # النص الخام
        self._raw_text = self.text or ""
        self._updating = False
        
        # معالجة hint_text ديناميكيًا
        self._hint_arabic_lock = False

        # وظيفة لمعالجة hint_text
        def on_hint_text(instance, value):
            if instance._hint_arabic_lock:
                return
            if not contains_arabic(value):
                return
                
            instance._hint_arabic_lock = True
            instance.hint_text = shape_arabic(value)
            instance._hint_arabic_lock = False
        
        # ربط event handler لـ hint_text
        self.bind(hint_text=on_hint_text)

        # وظيفة لمعالجة النص الرئيسي
        def on_text(instance, value):
            if instance._updating:
                return

            instance._updating = True

            # الحصول على النص المعروض حالياً
            displayed = shape_arabic(instance._raw_text)

            # حذف أحرف
            if len(value) < len(displayed):
                diff = len(displayed) - len(value)
                instance._raw_text = instance._raw_text[:-diff]

            # إضافة أحرف
            elif len(value) > len(displayed):
                # الحصول على الأحرف المضافة فقط
                added_chars = value[len(displayed):]
                instance._raw_text += added_chars

            # تحديث النص المعروض
            new_display = shape_arabic(instance._raw_text)
            instance.text = new_display
            
            # تحديث موقع المؤشر (Cursor)
            instance.cursor = (len(new_display), 0)

            instance._updating = False

        self.bind(text=on_text)

    TextInput.__init__ = new_textinput_init

    print("✅ Arabic support fully enabled (text + hint_text)")


# =========================
# Auto run
# =========================

if __name__ != "__main__":
    init_arabic_support()