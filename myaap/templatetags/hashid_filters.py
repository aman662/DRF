# your_app_name/templatetags/hashid_filters.py

from django import template
from hashids import Hashids

register = template.Library()
hashids = Hashids(salt="your_unique_salt_here", min_length=8)

@register.filter(name='hashid_encode')
def hashid_encode(value):
    return hashids.encode(value)