from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.http import Http404
from django.forms import modelform_factory, ModelChoiceField

from ..utils.url_handler import handle_data_gouv, handle_url

model_name = "Datasets"

def view_datasets(request):
    try:
        model = apps.get_model('automated_harvesting', model_name)
    except LookupError:
        raise Http404("Model not found")

    objects = model.objects.all()

    verbose_name = model._meta.verbose_name

    context = {
        'model_name': model_name,
        'verbose_name': verbose_name,
        'objects': objects,
    }
    
    return render(request, 'datasets_views/dataset_view.html', context)


def modify_dataset(request, record_id):
    model = apps.get_model('automated_harvesting', model_name)
    obj = get_object_or_404(model, id=record_id)
    ModelForm = modelform_factory(model, fields='__all__')
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('view_datasets')
    else:
        form = ModelForm(instance=obj)  
    
    return render(request, 'datasets_views/actions/modify_record.html', {'form': form, 'model_name': model_name})


def delete_dataset(request, record_id):
    model = apps.get_model('automated_harvesting', model_name)
    obj = get_object_or_404(model, id=record_id)
    if request.method == 'POST':
        obj.delete()
        return redirect('view_datasets')
    
    return render(request, 'datasets_views/actions/delete_record.html', {'object': obj, 'model_name': model_name})


def add_dataset(request):
    model = apps.get_model('automated_harvesting', model_name)
    ModelForm = modelform_factory(model, fields='__all__')

    class CustomModelForm(ModelForm):
        if model_name == 'BranchesSubBranches':
            id_branches = ModelChoiceField(
                queryset=apps.get_model('automated_harvesting', 'Branches').objects.all(),
                label="Branch",
                widget=forms.Select
            )
            id_sub_branches = ModelChoiceField(
                queryset=apps.get_model('automated_harvesting', 'SubBranches').objects.all(),
                label="Sub Branch",
                widget=forms.Select
            )

    if request.method == 'POST':
        form = CustomModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_datasets')
    else:
        form = CustomModelForm()  
    
    return render(request, 'datasets_views/actions/add_record.html', {'form': form, 'model_name': model_name})


def refresh_dataset(request, record_id):
    model = apps.get_model('automated_harvesting', model_name)
    

    if request.method == 'POST':
        return redirect('view_datasets')
    
    
    dataset = get_object_or_404(model, id=record_id)
    
    # Get the URL from the related Urls model
    if dataset.id_urls and dataset.id_urls.url:
        url = dataset.id_urls.url
        if "data.gouv.fr" in url:
            handle_data_gouv(record_id, url)
        else:
            handle_url(record_id, url)
    
    return redirect('view_datasets')
