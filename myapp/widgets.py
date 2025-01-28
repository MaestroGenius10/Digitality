from django.forms.widgets import ClearableFileInput
from django.utils.safestring import mark_safe

class CustomClearableFileInput(ClearableFileInput):
    def render(self, name, value, attrs=None, renderer=None):
        input_html = super().render(name, value, attrs, renderer)
        if value and hasattr(value, "url"):
            img_html = f'<img src="{value.url}" alt="Текущее изображение" style="max-height: 100px; max-width: 100px; margin-top: 10px; border-radius: 5px;"/>'
            return mark_safe(f'{img_html}<br>{input_html}')
        return input_html
