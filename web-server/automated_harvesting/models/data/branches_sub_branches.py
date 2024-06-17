from django.db import models
from .branches import Branches
from .sub_branches import SubBranches


class BranchesSubBranches(models.Model):
    id = models.BigAutoField(primary_key=True)
    id_sub_branches = models.OneToOneField(SubBranches, models.DO_NOTHING, db_column='id_sub_branches')
    id_branches = models.ForeignKey(Branches, models.DO_NOTHING, db_column='id_branches')

    class Meta:
        managed = False
        db_table = 'branches_sub_branches'
        verbose_name = "Liens branche - sous-branche"


    def get_branch_name(self):
        return self.id_branches.name if self.id_branches else None
    
    def get_sub_branch_name(self):
        return self.id_sub_branches.name if self.id_sub_branches else None