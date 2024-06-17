from django.db import models


class DinamicTableMapping(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)
    id_table_names = models.ForeignKey('TableNames', models.DO_NOTHING, db_column='id_table_names', blank=True, null=True)
    id_static_data_tables = models.ForeignKey('StaticDataTables', models.DO_NOTHING, db_column='id_static_data_tables', blank=True, null=True)
    id_dinamic_data_tables = models.ForeignKey('DinamicDataTables', models.DO_NOTHING, db_column='id_dinamic_data_tables', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dinamic_table_mapping'
        verbose_name = "Table names"
    
    def __str__(self):
        return self.name 