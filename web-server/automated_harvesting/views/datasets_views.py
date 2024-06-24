from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.http import Http404
from django.forms import modelform_factory
from ..forms import DatasetFilterForm
from django.urls import reverse

from ..utils.datasets.download_dataset import download_dataset

model_name = "Datasets"


def view_datasets(request):
    try:
        model = apps.get_model('automated_harvesting', 'Datasets')
    except LookupError:
        raise Http404("Model not found")

    filter_form = DatasetFilterForm(request.GET)

    objects = model.objects.all()
    if filter_form.is_valid():
        if filter_form.cleaned_data['name']:
            objects = objects.filter(name__icontains=filter_form.cleaned_data['name'])
        if filter_form.cleaned_data['id_bvbv']:
            objects = objects.filter(id_bvbv=filter_form.cleaned_data['id_bvbv'])
        if filter_form.cleaned_data['id_branches']:
            objects = objects.filter(id_branches=filter_form.cleaned_data['id_branches'])
        if filter_form.cleaned_data['id_sub_branches']:
            objects = objects.filter(id_sub_branches=filter_form.cleaned_data['id_sub_branches'])
        if filter_form.cleaned_data['id_precision']:
            objects = objects.filter(id_precision=filter_form.cleaned_data['id_precision'])
        if filter_form.cleaned_data['id_sources']:
            objects = objects.filter(id_sources=filter_form.cleaned_data['id_sources'])
        if filter_form.cleaned_data['id_region']:
            objects = objects.filter(id_region=filter_form.cleaned_data['id_region'])
        if filter_form.cleaned_data['id_urls']:
            objects = objects.filter(id_urls=filter_form.cleaned_data['id_urls'])

    # Group objects by URL
    grouped_objects = {}
    for obj in objects:
        url_name = obj.get_urls_name()
        if url_name not in grouped_objects:
            grouped_objects[url_name] = []
        grouped_objects[url_name].append(obj)

    verbose_name = model._meta.verbose_name

    context = {
        'model_name': model._meta.model_name,
        'verbose_name': verbose_name,
        'grouped_objects': grouped_objects,
        'filter_form': filter_form,
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

    obj.delete()
    return redirect('view_datasets')
    

def add_dataset(request):
    model = apps.get_model('automated_harvesting', model_name)
    ModelForm = modelform_factory(model, fields='__all__')


    if request.method == 'POST':
        form = ModelForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('view_datasets')
    else:
        form = ModelForm()  
    
    return render(request, 'datasets_views/actions/add_record.html', {'form': form, 'model_name': model_name})


def refresh_dataset(request, record_id):
    if request.method == 'POST':
        return redirect('view_datasets')
    
    download_dataset(record_id)
    
    query_string = request.GET.urlencode()
    redirect_url = f"{reverse('view_datasets')}?{query_string}"
    
    return redirect(redirect_url)



def refresh_all_datasets(request):
    model = apps.get_model('automated_harvesting', model_name)
    filter_form = DatasetFilterForm(request.GET)
    objects = model.objects.all()

    if filter_form.is_valid():
        if filter_form.cleaned_data['name']:
            objects = objects.filter(name__icontains=filter_form.cleaned_data['name'])
        if filter_form.cleaned_data['id_bvbv']:
            objects = objects.filter(id_bvbv=filter_form.cleaned_data['id_bvbv'])
        if filter_form.cleaned_data['id_branches']:
            objects = objects.filter(id_branches=filter_form.cleaned_data['id_branches'])
        if filter_form.cleaned_data['id_sub_branches']:
            objects = objects.filter(id_sub_branches=filter_form.cleaned_data['id_sub_branches'])
        if filter_form.cleaned_data['id_precision']:
            objects = objects.filter(id_precision=filter_form.cleaned_data['id_precision'])
        if filter_form.cleaned_data['id_sources']:
            objects = objects.filter(id_sources=filter_form.cleaned_data['id_sources'])
        if filter_form.cleaned_data['id_region']:
            objects = objects.filter(id_region=filter_form.cleaned_data['id_region'])
        if filter_form.cleaned_data['id_urls']:
            objects = objects.filter(id_urls=filter_form.cleaned_data['id_urls'])

    for dataset in objects:
        refresh_dataset(dataset.id)
 
    query_string = request.GET.urlencode()
    redirect_url = f"{reverse('view_datasets')}?{query_string}"
    
    return redirect(redirect_url)