from django.urls import path

from .views.model_views import list_models, view_model_data, modify_record, delete_record, add_record
from .views.datasets_views import view_datasets, modify_dataset, delete_dataset, add_dataset, refresh_dataset, refresh_all_datasets
from .views.url_table_mapping_view import watch_dataset, view_table_data, delete_url_table_mapping
from .views.base_view import base


urlpatterns = [
    path('', base, name='base'),
    path('analyse/', base, name='base'),

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

    path('view_table_data/<str:table_name>/', view_table_data, name='view_table_data'),
    path('delete_url_table_mapping/<int:mapping_id>/', delete_url_table_mapping, name='delete_url_table_mapping'),
]