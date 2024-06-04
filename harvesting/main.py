from db_operations import get_urls
from url_handler import handle_url, handle_data_gouv
import sys

print(sys.path)

rows = get_urls()
for row in rows[6:]:
    id, url = row
    print("URL ID:", id)
    print("URL:", url)
    if "data.gouv.fr" in url:
        handle_data_gouv(id, url)
    else:
        handle_url(id, url)

