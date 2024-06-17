from django.db import models

from django import template

register = template.Library()

@register.filter
def get_attributes(obj):
    return [field.name for field in obj._meta.fields]

@register.filter
def get_values(obj):
    return [getattr(obj, field.name) for field in obj._meta.fields]

class Urls(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'urls'
        verbose_name = "Urls"
    
    def __str__(self):
        return self.url
