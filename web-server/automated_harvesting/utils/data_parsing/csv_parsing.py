import csv
import os
import logging
from concurrent.futures import ThreadPoolExecutor
from io import StringIO
import pandas as pd
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names, sanitize_table_name
import time
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def detect_delimiter(csv_file):
    try:
        sample_lines = [csv_file.readline() for _ in range(1)]

        comma_count = sum(line.count(',') for line in sample_lines)
        semicolon_count = sum(line.count(';') for line in sample_lines)

        if comma_count > semicolon_count:
            return ','
        else:
            return ';'
    except Exception as e:
        logger.error(f"Error detecting delimiter: {e}")
        raise e


def detect_header_row(csv_file, delimiter):
    try:
        csv_file.seek(0)
        reader = csv.reader(csv_file, delimiter=delimiter)
        for i, row in enumerate(reader):
            non_empty_count = len([cell for cell in row if cell])
            string_count = sum([1 for cell in row if isinstance(cell, str)])
            if non_empty_count > 2 and string_count / non_empty_count > 0.5:
                return i
        return None
    except Exception as e:
        logger.error(f"Error detecting header row: {e}")
        raise e


def process_csv(id, data, table_name):
    try:
        content = data.decode('utf-8')
        csv_file = StringIO(content)

        delimiter = detect_delimiter(csv_file)
        csv_file.seek(0)

        header_row_index = detect_header_row(csv_file, delimiter)
        if header_row_index is None:
            raise ValueError(f"No header row detected in '{table_name}'.")
        csv_file.seek(0)

        # Skip rows before the header row
        for _ in range(header_row_index):
            next(csv_file)

        csv_data = csv.DictReader(csv_file, delimiter=delimiter)
        field_names = sanitize_field_names(csv_data.fieldnames)


        print(f"Field_names: {field_names}")
        print(f"Number of fields: {len(field_names)}")

        table_data = {
            "schema": "data",
            "name": table_name,
            "field_names": field_names,
            "id" : id
        }

        try:
            create_table(table_data)
        except Exception as e:
            logger.error(f"Error creating table {table_name}: {e}")
            raise


        with ThreadPoolExecutor(max_workers=os.cpu_count() // 2) as executor:
            for row in csv_data:
                while psutil.virtual_memory().percent >= 80:
                    print("Memory usage is too high, waiting...")
                    time.sleep(1)
                            
                if all(pd.isnull(value) for value in row.values()):
                    continue

                values = [str(value) if pd.notnull(value) else '' for value in row.values()]
                if len(values) != len(field_names):
                    raise ValueError("Number of values in row doesn't match number of fields")

                insert_data = {
                    "schema": "data",
                    "name": table_name,
                    "field_names": field_names,
                    "data": values
                }
                executor.submit(insert_row, insert_data)


    except Exception as e:
        logger.error(f"Error processing CSV: {e}")
        raise e