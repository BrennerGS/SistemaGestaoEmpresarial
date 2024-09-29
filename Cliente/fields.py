from django.urls import reverse
from django.utils.html import format_html
from django.utils.safestring import mark_safe

class ListAction:
    def __init__(self, url_name, formGen=None, id=None, name=None, label=None, icon=None,cor=None):
        self.id = id
        self.formGen = formGen
        self.url_name = url_name
        self.name = name
        self.label = label
        self.icon = icon
        self.cor = cor


