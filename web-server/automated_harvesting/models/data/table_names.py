from django.db import models


class TableNames(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'table_names'
        verbose_name = "Table names"
    
    def __str__(self):
        return self.name 