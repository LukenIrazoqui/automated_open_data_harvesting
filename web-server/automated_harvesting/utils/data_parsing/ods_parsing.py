import os
import logging
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
from ezodf import newdoc, Sheet
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names, sanitize_table_name

# Configure logging
logging.basicConfig(level=logging.INFO)

logger = logging.getLogger('automated_harvesting.utils.data_parsing.ods_parsing')


def detect_header_row(sheet):
    for i, row in enumerate(sheet):
        non_empty_count = sum(1 for cell in row if cell is not None)
        string_count = sum(1 for cell in row if isinstance(cell, str))
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return i
    return None


def process_ods(id, data, table_name):
    try:
        ods_file = BytesIO(data)
        doc = newdoc(doctype="ods", filename=ods_file)

        for ods_sheet in doc.sheets:
            sheet_name = ods_sheet.name
            ods_sheet = doc.sheets[sheet_name]

            # Detect header row
            header_row_index = detect_header_row(ods_sheet)
            if header_row_index is None:
                logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                continue

            field_names = sanitize_field_names(ods_sheet[header_row_index])

            sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"

            table_data = {
                "schema": "data",
                "name": sheet_table_name,
                "field_names": field_names,
                "id" : id
            }

            try:

                create_table(table_data)

                with ThreadPoolExecutor(max_workers=os.cpu_count()) as executor:
                    for row in ods_sheet[header_row_index + 1:]:
                        if not any(row):
                            continue

                        values = [str(value) if value is not None else '' for value in row]
                        if len(values) != len(field_names):
                            raise ValueError("Number of values in row doesn't match number of fields")

                        insert_data = {
                            "schema": "data",
                            "name": sheet_table_name,
                            "field_names": field_names,
                            "data": values
                        }
                        executor.submit(insert_row, insert_data)

            except Exception as create_insert_error:
                logger.error(f"Error occurred during table creation or insertion: {create_insert_error}")
                raise create_insert_error
    except Exception as ods_process_error:
        logger.error(f"An error occurred while processing ODS: {ods_process_error}")
        raise ods_process_error