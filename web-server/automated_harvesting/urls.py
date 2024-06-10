from django.urls import path

from .views.model_views import list_models, view_model_data, modify_record, delete_record, add_record
from .views.datasets_views import view_datasets, modify_dataset, delete_dataset, add_dataset, refresh_dataset
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
    path('dataset/modify/<int:record_id>/', modify_dataset, name='modify_dataset'),
    path('dataset/delete/<int:record_id>/', delete_dataset, name='delete_dataset'),
    path('dataset/refresh/<int:record_id>/', refresh_dataset, name='refresh_dataset'),
    path('dataset/add/', add_dataset, name='add_dataset'),
]