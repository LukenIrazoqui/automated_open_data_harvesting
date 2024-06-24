from django.urls import path

from .views.model_views import list_models, view_model_data, modify_record, delete_record, add_record
from .views.datasets_views import view_datasets, modify_dataset, delete_dataset, add_dataset, refresh_dataset, refresh_all_datasets
from .views.url_table_mapping_view import watch_dataset, delete_url_table_mapping, delete_all_url_table_mappings, refresh
from .views.base_view import base
from .views.analyse_view import analyse
from .views.data_table_view import view_table_data, submit_columns


urlpatterns = [
    path('', base, name='base'),
    path('analyse/', analyse, name='base'),

    path('models/', list_models, name='list_models'),

    path('models/<str:model_name>/', view_model_data, name='view_model_data'),
    path('models/<str:model_name>/modify/<int:record_id>/', modify_record, name='modify_record'),
    path('models/<str:model_name>/delete/<int:record_id>/', delete_record, name='delete_record'),
    path('models/<str:model_name>/add/', add_record, name='add_record'),

    path('dataset/', view_datasets, name='view_datasets'),

    path('dataset/add/', add_dataset, name='add_dataset'),
    path('datasets/refresh_all/', refresh_all_datasets, name='refresh_all'),

    path('dataset/modify/<int:record_id>/', modify_dataset, name='modify_dataset'),
    path('dataset/delete/<int:record_id>/', delete_dataset, name='delete_dataset'),
    path('dataset/refresh/<int:record_id>/', refresh_dataset, name='refresh_dataset'),

    path('watch_dataset/<int:url_id>/', watch_dataset, name='watch_dataset'),
    path('watch_dataset/refresh/<int:id>/<int:url_id>/', refresh, name='refresh'),
    
    path('delete-all-mappings/<int:url_id>/', delete_all_url_table_mappings, name='delete_all_mappings'),
    path('delete_url_table_mapping/<int:mapping_id>/', delete_url_table_mapping, name='delete_url_table_mapping'),

    path('view_table_data/<str:table_name>/', view_table_data, name='view_table_data'),
    path('submit_columns/', submit_columns, name='submit_columns'),
]