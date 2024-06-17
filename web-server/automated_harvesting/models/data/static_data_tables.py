from django.db import models


class StaticDataTables(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'static_data_tables'
        verbose_name = "Table names"
    
    def __str__(self):
        return self.name 