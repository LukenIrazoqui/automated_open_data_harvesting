from django.db import models


class Urls(models.Model):
    id = models.BigAutoField(primary_key=True)
    url = models.TextField()

    class Meta:
        managed = False
        db_table = 'urls'
