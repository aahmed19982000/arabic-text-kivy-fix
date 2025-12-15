# arabic-text-kivy-fix
# Arabic Text Support for Kivy

حل كامل لمشكلة عرض النصوص العربية في Kivy مع دعم الكتابة من اليمين لليسار (RTL) والحركات العربية.

## الميزات
- دعم كامل للنصوص العربية في Widgets.
- إعادة ترتيب النصوص تلقائيًا.
- مناسب لكل من Labels وTextInput.

## كيفية الاستخدام
1. انسخ `arabic_patch.py` إلى مشروعك.
2. استورد الملف قبل أي واجهة:
```python
from arabic_patch import apply_arabic_fix
apply_arabic_fix()
