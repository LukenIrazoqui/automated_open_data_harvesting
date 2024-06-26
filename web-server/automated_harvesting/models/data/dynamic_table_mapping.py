from django.db import models


class DynamicTableMapping(models.Model):
    id_table_names = models.OneToOneField('TableNames', models.DO_NOTHING, db_column='id_table_names', blank=True, null=True)
    id_static_data_table_names = models.OneToOneField('StaticDataTableNames', models.DO_NOTHING, db_column='id_static_data_table_names', blank=True, null=True)
    id_dynamic_data_table_names = models.OneToOneField('DynamicDataTableNames', models.DO_NOTHING, db_column='id_dynamic_data_table_names', blank=True, null=True)
    id_view_names = models.OneToOneField('ViewNames', models.DO_NOTHING, db_column='id_view_names', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'dynamic_table_mapping'
        verbose_name = "Table names"
    
    def __str__(self):
        return self.name 