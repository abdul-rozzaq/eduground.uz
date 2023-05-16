from django import template
from django.conf import settings
import os

from home.models import EducationCenter

register = template.Library()

@register.filter(name='color')
def color(filename, ec: EducationCenter):
    css_path = os.path.join(settings.BASE_DIR, 'static', filename)
    if not os.path.isfile(css_path):
        raise ValueError(f'Fayl topilmadi: {css_path}')
    with open(css_path, 'r') as f:
        css_content = f.read()

    css_content = css_content.replace('#15a362', ec.color)

    return css_content  # CSS faylning matni
