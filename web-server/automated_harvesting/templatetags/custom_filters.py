from django import template

register = template.Library()

@register.filter
def get_attributes(obj):
    return [field.name for field in obj._meta.fields if field.name != 'id']

@register.filter
def get_values(obj):
    return [getattr(obj, field.name) for field in obj._meta.fields]

@register.filter
def get_field_value(obj, field_name):
    return getattr(obj, field_name)
