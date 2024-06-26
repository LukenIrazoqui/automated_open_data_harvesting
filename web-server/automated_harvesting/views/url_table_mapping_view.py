from django.shortcuts import render, redirect
from django.apps import apps
from ..models import UrlTableMapping, Urls 
from django.http import Http404, JsonResponse
from django.db import connection, transaction
from django.urls import reverse

from ..utils.datasets.download_dataset import download_dataset

def watch_dataset(request, url_id):
    model_name = "Datasets"
    model = apps.get_model('automated_harvesting', model_name)
    datasets = model.objects.filter(id_urls=url_id)
    if not datasets:
        raise Http404("No datasets found for this URL")

    url_table_mappings = UrlTableMapping.objects.filter(id_urls=url_id)
    
    context = {
        'datasets': datasets,
        'url_table_mappings': url_table_mappings,
    }
    
    return render(request, 'datasets_views/url_table_mapping_view.html', context)

def delete_url_table_mapping(request, mapping_id):
    try:
        mapping = UrlTableMapping.objects.get(id=mapping_id)
    except UrlTableMapping.DoesNotExist:
        raise Http404("Mapping not found")

    schema_name = 'data'
    table_id = mapping.id_table_names.id
    table_name = mapping.get_table_name()

    with transaction.atomic():
        mapping.delete()

        with connection.cursor() as cursor:
            cursor.execute('DELETE FROM dynamic_table_mapping WHERE id_table_names = %s', [table_id])
            cursor.execute('DROP TABLE IF EXISTS {schema}."{table}"'.format(schema=schema_name, table=table_name))
            cursor.execute('DELETE FROM table_names WHERE id = %s', [table_id])

    return redirect('watch_dataset', mapping.id_urls.id)


def delete_all_url_table_mappings(request, url_id):
    schema_name = 'data'
    with transaction.atomic():
        mappings = UrlTableMapping.objects.filter(id_urls_id=url_id)
        for mapping in mappings:
            table_id = mapping.id_table_names.id
            table_name = mapping.get_table_name()

            mapping.delete()

            with connection.cursor() as cursor:
                cursor.execute('DELETE FROM dynamic_table_mapping WHERE id_table_names = %s', [table_id])
                cursor.execute('DROP TABLE IF EXISTS {schema}."{table}"'.format(schema=schema_name, table=table_name))
                cursor.execute('DELETE FROM table_names WHERE id = %s', [table_id])

    
    return redirect('watch_dataset', url_id)


def refresh(request, id, url_id) :    
    download_dataset(id)
    
    return redirect('watch_dataset', url_id)
