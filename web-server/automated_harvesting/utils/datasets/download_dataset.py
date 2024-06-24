from django.shortcuts import get_object_or_404
from django.apps import apps
import threading

from ..url_handler import handle_data_gouv, handle_url

model_name = "Datasets"

def download_dataset(record_id):
    model = apps.get_model('automated_harvesting', model_name)
    
    dataset = get_object_or_404(model, id=record_id)
    
    if dataset.id_urls and dataset.id_urls.url:
        id = dataset.id_urls.id
        url = dataset.id_urls.url
        if "data.gouv.fr" in url:
            thread = threading.Thread(target=handle_data_gouv, args=(id, url))
            thread.start()
        else:
            thread = threading.Thread(target=handle_url, args=(id, url))
            thread.start()