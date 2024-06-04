from django.db import models


class UrlTableMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_urls = models.ForeignKey('Urls', models.DO_NOTHING, db_column='id_urls', blank=True, null=True)
    table_name = models.TextField()

    class Meta:
        managed = False
        db_table = 'url_table_mapping'
        unique_together = (('id_urls', 'table_name'),)