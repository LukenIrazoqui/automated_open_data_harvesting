from django.db import models


class UrlTableMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_urls = models.ForeignKey('Urls', models.DO_NOTHING, db_column='id_urls', blank=True, null=True)
    id_table_names = models.ForeignKey('TableNames', models.DO_NOTHING, db_column='id_table_names', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'url_table_mapping'
        verbose_name = "Liens url - table"

    def get_urls_name(self):
        return self.id_urls.url if self.id_urls else None
    

    def get_table_name(self):
        print(self)
        print(self.id_table_names.name)
        return self.id_table_names.name if self.id_table_names else None