from django import forms
from django.shortcuts import render, get_object_or_404, redirect
from django.apps import apps
from django.http import Http404
from django.forms import modelform_factory, ModelChoiceField


def list_models(request):
    return render(request, 'model_views/list_models.html')


def view_model_data(request, model_name):
    try:
        model = apps.get_model('automated_harvesting', model_name)
    except LookupError:
        raise Http404("Model not found")

    objects = model.objects.all()

    verbose_name = model._meta.verbose_name.title()


    if model_name == "BranchesSubBranches" : 

        grouped_objects = {}
        for obj in objects:
            if obj.id_branches not in grouped_objects:
                grouped_objects[obj.id_branches] = []
            grouped_objects[obj.id_branches].append(obj)

        context = {
            'model_name': model_name,
            'verbose_name': verbose_name,
            'objects': grouped_objects,
        }

        return render(request, 'model_views/branches_sub_branches_view.html', context)    
    

    context = {
        'model_name': model_name,
        'verbose_name': verbose_name,
        'objects': objects,
    }
    
    return render(request, 'model_views/view_model_data.html', context)


def modify_record(request, model_name, record_id):
    model = apps.get_model('automated_harvesting', model_name)
    obj = get_object_or_404(model, id=record_id)
    ModelForm = modelform_factory(model, fields='__all__')
    if request.method == 'POST':
        form = ModelForm(request.POST, instance=obj)
        if form.is_valid():
            form.save()
            return redirect('view_model_data', model_name=model_name)
    else:
        form = ModelForm(instance=obj)  
    
    return render(request, 'model_views/actions/modify_record.html', {'form': form, 'model_name': model_name})


def delete_record(request, model_name, record_id):
    model = apps.get_model('automated_harvesting', model_name)
    obj = get_object_or_404(model, id=record_id)
    obj.delete()
    return redirect('view_model_data', model_name=model_name)


def add_record(request, model_name):
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
            return redirect('view_model_data', model_name=model_name)
    else:
        form = CustomModelForm()  
    
    return render(request, 'model_views/actions/add_record.html', {'form': form, 'model_name': model_name})
