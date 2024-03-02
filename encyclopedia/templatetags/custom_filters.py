# custom_filters.py

from django import template
from markdown import markdown

register = template.Library()

@register.filter
def markdown_to_html(markdown_text):
    return markdown(markdown_text)
