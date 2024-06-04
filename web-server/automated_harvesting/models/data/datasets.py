from django.db import models


class Datasets(models.Model):
    id = models.BigAutoField(primary_key=True)
    name = models.CharField(max_length=256)
    id_bvbv = models.ForeignKey(Bvbv, models.DO_NOTHING, db_column='id_bvbv', blank=True, null=True)
    id_branches = models.ForeignKey(Branches, models.DO_NOTHING, db_column='id_branches', blank=True, null=True)
    id_sub_branches = models.ForeignKey('SubBranches', models.DO_NOTHING, db_column='id_sub_branches', blank=True, null=True)
    id_precision = models.ForeignKey('Precision', models.DO_NOTHING, db_column='id_precision', blank=True, null=True)
    id_sources = models.ForeignKey('Sources', models.DO_NOTHING, db_column='id_sources', blank=True, null=True)
    id_region = models.ForeignKey('Region', models.DO_NOTHING, db_column='id_region', blank=True, null=True)
    id_urls = models.OneToOneField('Urls', models.DO_NOTHING, db_column='id_urls', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'datasets'