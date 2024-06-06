from django.db import models


class Sources(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=128)

    class Meta:
        managed = False
        db_table = 'sources'
        verbose_name = "Sources"
    
    def __str__(self):
        return self.name 