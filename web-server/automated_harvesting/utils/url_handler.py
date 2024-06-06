import os
import tempfile
import zipfile
import requests
from bs4 import BeautifulSoup
from .data_parsing.xls_parsing import process_xls
from .data_parsing.xslx_parsing import process_xlsx
from .data_parsing.ods_parsing import process_ods
from .data_parsing.shp_parsing import process_shp
from .data_parsing.dbf_parsing import process_dbf
from .data_parsing.csv_parsing import process_csv
from .data_parsing.sanitize_names import sanitize_table_name
import logging


logger = logging.getLogger(__name__)


def download_file(url):
    response = requests.get(url, allow_redirects=True)
    if response.status_code == 200:
        return response
    else:
        return None


def is_folder(filename):
    return os.path.isdir(filename)


def handle_file(id, data, file_name):
    logger.info(f"Handling file: {file_name}")

    try:
        if file_name.endswith('.csv'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing CSV file {file_name} into table {table_name}")
            process_csv(id, data, table_name)
        elif file_name.endswith('.xlsx'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing Excel file {file_name} into table {table_name}")
            process_xlsx(id, data, table_name)
        elif file_name.endswith('.xls'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing Excel (xls) file {file_name} into table {table_name}")
            process_xls(id, data, table_name)
        elif file_name.endswith('.ods'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing ODS file {file_name} into table {table_name}")
            process_ods(id, data, table_name)
        elif file_name.endswith('.shp'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing Shapefile {file_name} into table {table_name}")
            process_shp(id, data, table_name)
        elif file_name.endswith('.dbf'):
            table_name = sanitize_table_name(file_name)
            logger.info(f"Processing DBF file {file_name} into table {table_name}")
            process_dbf(id, data, table_name)
        elif file_name.endswith('.zip'):
            logger.info(f"Extracting files from ZIP archive for ID {id}")
            process_zip(id, data)
        else:
            logger.warning(f"Unsupported file format: {file_name}. Skipping processing.")
    except Exception as e:
        logger.error(f"Error processing file {file_name}: {e}")


def process_folder(id, folder_path):
    try:
        for root, dirs, files in os.walk(folder_path):
            for file_name in files:
                file_path = os.path.join(root, file_name)
                with open(file_path, 'rb') as file:
                    handle_file(id, file.read(), os.path.relpath(file_path, folder_path))
            for sub_folder in dirs:
                sub_folder_path = os.path.join(root, sub_folder)
                process_folder(id, sub_folder_path)
    except Exception as e:
        logger.error(f"Error processing folder {folder_path}: {e}")


def process_zip(id, data):
    try:
        with tempfile.NamedTemporaryFile(delete=False) as temp_file:
            temp_file.write(data)

        with zipfile.ZipFile(temp_file.name, 'r') as zip_ref:
            for file in zip_ref.namelist():
                with zip_ref.open(file) as f:
                    if file.endswith('/'):
                        folder_path = os.path.join(tempfile.gettempdir(), file[:-1])
                        zip_ref.extract(file, tempfile.gettempdir())
                        process_folder(id, folder_path)
                    else:
                        handle_file(id, f.read(), f.name)
    except Exception as e:
        logger.error(f"Error processing ZIP file: {e}")


def handle_data_gouv(id, url):
    try:
        response = requests.get(url)
        if response.status_code == 200:
            soup = BeautifulSoup(response.content, 'html.parser')
            articles = soup.find_all("article")
            for article in articles:
                h4_element = article.find("h4")
                link = article.find("a", class_="matomo_download")
                if h4_element and link:
                    file_name = h4_element.text.strip()

                    file_url = link.get("href")
                    response = download_file(file_url)
                    if response is not None:
                        handle_file(id, response.content, file_name)
        else:
            logger.error(f"Failed to fetch data from '{url}'. Status code: {response.status_code}")
    except Exception as e:
        logger.error(f"Error handling data from URL '{url}': {e}")


def handle_url(id, url):
    try:
        response = download_file(url)

        if response is None:
            return

        content_disposition = response.headers.get('content-disposition')
        if content_disposition is None:
            return

        file_name = url

        if 'filename=' in content_disposition:
            file_name = content_disposition.split('filename=')[1].strip('"')

        handle_file(id, response.content, file_name)
    except Exception as e:
        logger.error(f"Error handling URL '{url}': {e}")


