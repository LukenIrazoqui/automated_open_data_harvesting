from django import forms
from .models import Datasets, Bvbv, Branches, SubBranches, Precision, Sources, Region, Urls

class DatasetFilterForm(forms.Form):
    def __init__(self, *args, **kwargs):
        super(DatasetFilterForm, self).__init__(*args, **kwargs)

        # Fetch distinct values for each related field
        self.fields['name'].choices = [('', 'Aucun filtre')] + [(name, name) for name in Datasets.objects.values_list('name', flat=True).distinct()]
        self.fields['id_bvbv'].choices = [('', 'Aucun filtre')] + [(bvbv.id, bvbv.name) for bvbv in Bvbv.objects.all().distinct()]
        self.fields['id_branches'].choices = [('', 'Aucun filtre')] + [(branch.id, branch.name) for branch in Branches.objects.all().distinct()]
        self.fields['id_sub_branches'].choices = [('', 'Aucun filtre')] + [(sub_branch.id, sub_branch.name) for sub_branch in SubBranches.objects.all().distinct()]
        self.fields['id_precision'].choices = [('', 'Aucun filtre')] + [(precision.id, precision.name) for precision in Precision.objects.all().distinct()]
        self.fields['id_sources'].choices = [('', 'Aucun filtre')] + [(source.id, source.name) for source in Sources.objects.all().distinct()]
        self.fields['id_region'].choices = [('', 'Aucun filtre')] + [(region.id, region.name) for region in Region.objects.all().distinct()]
        self.fields['id_urls'].choices = [('', 'Aucun filtre')] + [(url.id, url.url) for url in Urls.objects.all().distinct()]

    name = forms.ChoiceField(required=False, choices=[])
    id_bvbv = forms.ChoiceField(required=False, choices=[])
    id_branches = forms.ChoiceField(required=False, choices=[])
    id_sub_branches = forms.ChoiceField(required=False, choices=[])
    id_precision = forms.ChoiceField(required=False, choices=[])
    id_sources = forms.ChoiceField(required=False, choices=[])
    id_region = forms.ChoiceField(required=False, choices=[])
    id_urls = forms.ChoiceField(required=False, choices=[])
