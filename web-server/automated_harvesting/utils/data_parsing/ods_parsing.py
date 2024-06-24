import os
import logging
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import ezodf
from ezodf import newdoc, Sheet
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names, sanitize_table_name
import time
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('automated_harvesting.utils.data_parsing.ods_parsing')


def find_longest_row(sheet):
    longest_row_length = 0
    for row_index, row in enumerate(sheet.rows()):
        non_empty_count = sum(1 for cell in row if cell.value is not None)
        string_count = sum(1 for cell in row if isinstance(cell.value, str))
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return row_index
        row_length = len(row)
        while row_length > 0 and row[row_length - 1].value is None:
            row_length -= 1
        if row_length > longest_row_length:
            longest_row_length = row_length
    if longest_row_length > 0:
        return longest_row_length
    return None


def detect_header_row(sheet):
    for i, row in enumerate(sheet.rows()):
        non_empty_count = sum(1 for cell in row if cell.value is not None)
        string_count = sum(1 for cell in row if isinstance(cell.value, str))
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return i
    return None


def process_ods(id, data, table_name):
    try:
        ods_file = BytesIO(data)

        doc = ezodf.opendoc(ods_file)


        for ods_sheet in doc.sheets:

            sheet_name = ods_sheet.name


            keywords = ["param", "def", "déf", "conf"]

            if any(keyword in sheet_name.lower() for keyword in keywords):
                longest_row = find_longest_row(ods_sheet)
                if longest_row is None:
                    logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                    continue

                header_row_index = 0

                field_names = []
                for i in range(longest_row):
                    field_names.append(f"column_{i}")
            else :
                header_row_index = detect_header_row(ods_sheet)
                if header_row_index is None:
                    logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                    continue

                
                header_row = ods_sheet.row(header_row_index)
                field_names = sanitize_field_names(header_row)
                field_names = [name for name in sanitize_field_names(header_row) if name != 'None']


            valid_columns = range(len(field_names))

            sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"
            print(sheet_table_name)

            table_data = {
                "schema": "data",
                "name": sheet_table_name,
                "field_names": field_names,
                "id" : id
            }

            try:

                create_table(table_data)

                for row_idx, row in enumerate(ods_sheet.rows()):                        
                    if row_idx <= header_row_index:
                        continue

                    row_data = [row[index].value for index in valid_columns]
                    if not any(cell is not None for cell in row_data):
                        continue

                    values = [str(value) if value is not None else '' for value in row_data]
                    if len(values) != len(field_names):
                        raise ValueError("Number of values in row doesn't match number of fields")

                    insert_data = {
                        "schema": "data",
                        "name": sheet_table_name,
                        "field_names": field_names,
                        "data": values
                    }
                    insert_row(insert_data)

            except Exception as create_insert_error:
                logger.error(f"Error occurred during table creation or insertion: {create_insert_error}")
                raise create_insert_error
    except Exception as ods_process_error:
        logger.error(f"An error occurred while processing ODS: {ods_process_error}")
        raise ods_process_error