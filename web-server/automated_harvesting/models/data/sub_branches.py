from django.db import models


class SubBranches(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=64)

    class Meta:
        managed = False
        db_table = 'sub_branches'
        verbose_name = "Sous-branches"
    
    def __str__(self):
        return self.name 