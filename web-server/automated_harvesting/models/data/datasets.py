from django.db import models

from .branches import Branches
from .bvbv import Bvbv
from .precision import Precision
from .region import Region
from .sources import Sources
from .sub_branches import SubBranches
from .urls import Urls


class Datasets(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_bvbv = models.ForeignKey(Bvbv, models.DO_NOTHING, db_column='id_bvbv', blank=True, null=True)
    id_branches = models.ForeignKey(Branches, models.DO_NOTHING, db_column='id_branches', blank=True, null=True)
    id_sub_branches = models.ForeignKey(SubBranches, models.DO_NOTHING, db_column='id_sub_branches', blank=True, null=True)
    id_precision = models.ForeignKey(Precision, models.DO_NOTHING, db_column='id_precision', blank=True, null=True)
    id_sources = models.ForeignKey(Sources, models.DO_NOTHING, db_column='id_sources', blank=True, null=True)
    id_region = models.ForeignKey(Region, models.DO_NOTHING, db_column='id_region', blank=True, null=True)
    id_urls = models.ForeignKey(Urls, models.DO_NOTHING, db_column='id_urls', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasets'
        verbose_name = "Jeux de données"

    def get_bvbv_name(self):
        return self.id_bvbv.name if self.id_bvbv else None

    def get_branches_name(self):
        return self.id_branches.name if self.id_branches else None

    def get_sub_branches_name(self):
        return self.id_sub_branches.name if self.id_sub_branches else None

    def get_precision_name(self):
        return self.id_precision.name if self.id_precision else None

    def get_sources_name(self):
        return self.id_sources.name if self.id_sources else None

    def get_region_name(self):
        return self.id_region.name if self.id_region else None

    def get_urls_name(self):
        return self.id_urls.url if self.id_urls else None
