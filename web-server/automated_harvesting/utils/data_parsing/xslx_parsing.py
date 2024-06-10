import os
import logging
from concurrent.futures import ThreadPoolExecutor
from io import BytesIO
import openpyxl
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names, sanitize_table_name
import time
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def detect_header_row(ws):
    for i, row in enumerate(ws.iter_rows(values_only=True)):
        non_empty_count = len([cell for cell in row if cell is not None])
        string_count = sum([1 for cell in row if isinstance(cell, str)])
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return i
    return None


def process_xlsx(id, data, table_name):
    try:
        wb = openpyxl.load_workbook(BytesIO(data), data_only=True)

        for sheet_name in wb.sheetnames:
            ws = wb[sheet_name]

            # Detect header row
            header_row_index = detect_header_row(ws) + 1
            if header_row_index is None:
                logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                continue

            # Read field names from the detected header row
            field_names = sanitize_field_names([cell for cell in ws[header_row_index]])

            
            print(f"Field_names: {field_names}")
            print(f"Number of fields: {len(field_names)}")

            sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"

            table_data = {
                "schema": "data",
                "name": sheet_table_name,
                "field_names": field_names,
                "id" : id
            }

            try:
                create_table(table_data)

                with ThreadPoolExecutor(max_workers=os.cpu_count() // (3/4)) as executor:
                    for row in ws.iter_rows(min_row=header_row_index + 1, values_only=True):
                        while psutil.virtual_memory().percent >= 80:
                            print("Memory usage is too high, waiting...")
                            time.sleep(1)
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

            except Exception as create_table_error:
                logger.error(f"Error creating table {sheet_table_name}: {create_table_error}")
                continue
    except Exception as xlsx_process_error:
        logger.error(f"Error processing XLSX: {xlsx_process_error}")
        raise xlsx_process_error
