from django.shortcuts import render, redirect
from django.apps import apps
from ..models import UrlTableMapping, Urls 
from django.http import Http404
from django.db import connection, transaction


def watch_dataset(request, url_id):
    model_name = "Datasets"
    model = apps.get_model('automated_harvesting', model_name)
    datasets = model.objects.filter(id_urls=url_id)
    if not datasets:
        raise Http404("No datasets found for this URL")

    # Fetch related UrlTableMapping entries
    url_table_mappings = UrlTableMapping.objects.filter(id_urls=url_id)
    
    context = {
        'datasets': datasets,
        'url_table_mappings': url_table_mappings,
    }
    
    return render(request, 'datasets_views/url_table_mapping_view.html', context)



def view_table_data(request, table_name):
    schema_name = 'data'

    # Get the list of valid table names to avoid SQL injection
    with connection.cursor() as cursor:
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'")
        valid_tables = [row[0] for row in cursor.fetchall()]

    if table_name not in valid_tables:
        raise Http404("Table not found")

    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM data."{table_name}" ORDER BY id ASC')
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    context = {
        'table_name': table_name,
        'columns': columns,
        'rows': rows,
    }
    
    return render(request, 'datasets_views/table_data_view.html', context)


def delete_url_table_mapping(request, mapping_id):
    try:
        mapping = UrlTableMapping.objects.get(id=mapping_id)
    except UrlTableMapping.DoesNotExist:
        raise Http404("Mapping not found")

    schema_name = 'data'
    table_name = mapping.table_name

    with transaction.atomic():
        # Delete the mapping entry
        mapping.delete()

        # Drop the table
        with connection.cursor() as cursor:
            cursor.execute(f'DROP TABLE IF EXISTS {schema_name}."{table_name}"')

    return redirect('watch_dataset', mapping.id_urls.id)