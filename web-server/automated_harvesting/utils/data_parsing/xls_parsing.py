import os
import logging
from concurrent.futures import ThreadPoolExecutor
import xlrd
from ..db_operations import insert_row, create_table, link_url_table
from .sanitize_names import sanitize_field_names, sanitize_table_name
import time
import psutil

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def find_longest_row(sheet):
    longest_row_length = 0
    for row_idx in range(sheet.nrows):
        row = sheet.row_values(row_idx)
        non_empty_count = len([cell for cell in row if cell])
        string_count = sum([1 for cell in row if isinstance(cell, str)])
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return row_idx
        row_length = len(row)
        while row_length > 0 and not row[row_length - 1]:
            row_length -= 1
        if row_length > longest_row_length:
            longest_row_length = row_length
    if longest_row_length > 0:
        return longest_row_length
    return None


def detect_header_row(sheet):
    for row_idx in range(sheet.nrows):
        row = sheet.row_values(row_idx)
        non_empty_count = len([cell for cell in row if cell])
        string_count = sum([1 for cell in row if isinstance(cell, str)])
        if non_empty_count > 2 and string_count / non_empty_count > 0.5:
            return row_idx
    return None


def process_xls(id, data, table_name):
    try:
        workbook = xlrd.open_workbook(file_contents=data)

        for sheet_index in range(workbook.nsheets):
            sheet = workbook.sheet_by_index(sheet_index)
            sheet_name = workbook.sheet_names()[sheet_index]

            if "param" in sheet_name.lower() or "def" in sheet_name.lower() :
                longest_row = find_longest_row(sheet)
                if longest_row is None:
                    logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                    continue

                header_row_index = 0

                field_names = []
                for i in range(longest_row):
                    field_names.append(f"column_{i}")

            else :
                header_row_index = detect_header_row(sheet)
                if header_row_index is None:
                    logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
                    continue

                raw_field_names = sheet.row_values(header_row_index)
                field_names = sanitize_field_names(raw_field_names)

            sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"

            table_data = {
                "schema": "data",
                "name": sheet_table_name,
                "field_names": field_names,
                "id" : id
            }

            try:

                create_table(table_data)

                header_row_index += 1

                for row_idx in range(header_row_index, sheet.nrows):
                    row = sheet.row_values(row_idx)
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

                    insert_row(insert_data)

            except Exception as create_table_error:
                logger.error(f"Error creating table {sheet_table_name}: {create_table_error}")
                continue

    except Exception as xls_process_error:
        logger.error(f"Error processing XLS: {xls_process_error}")
        raise xls_process_error
