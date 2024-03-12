
from django import template
from produtos.utils import get_attribute

register = template.Library()

@register.filter(name='get_attribute')
def get_attribute_filter(obj, attr):
    return get_attribute(obj, attr)
