from django.db import models


class ViewNames(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.TextField()

    class Meta:
        managed = False
        db_table = 'view_names'
        verbose_name = "Table names"
    
    def __str__(self):
        return self.name 