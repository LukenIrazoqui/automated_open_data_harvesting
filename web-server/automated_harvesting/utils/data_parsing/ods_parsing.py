import logging
from io import BytesIO
import ezodf
from ..db_operations import insert_row, create_table, is_table_dynamic, dynamic_mapping_columns
from .sanitize_names import sanitize_field_names, sanitize_table_name

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


def split_and_insert_dynamic_data(sheet_table_name, field_names, values, static_column_names, dynamic_column_names):
    static_data = {field: value for field, value in zip(field_names, values) if field in static_column_names}
    dynamic_data = {field: value for field, value in zip(field_names, values) if field in dynamic_column_names}

    static_insert_data = {
        "schema": "data",
        "name": sheet_table_name,
        "field_names": list(static_data.keys()),
        "data": list(static_data.values())
    }
    insert_row(static_insert_data)

    dynamic_insert_data = {
        "schema": "data",
        "name": sheet_table_name,
        "field_names": list(dynamic_data.keys()),
        "data": list(dynamic_data.values())
    }
    insert_row(dynamic_insert_data)


def process_rows(ods_sheet, header_row_index, valid_columns, field_names, sheet_table_name, is_dynamic, static_column_names, dynamic_column_names):
    for row_idx, row in enumerate(ods_sheet.rows()):
        if row_idx <= header_row_index:
            continue

        row_data = [row[index].value for index in valid_columns]
        if not any(cell is not None for cell in row_data):
            continue

        values = [str(value) if value is not None else '' for value in row_data]
        if len(values) != len(field_names):
            raise ValueError("Number of values in row doesn't match number of fields")

        if is_dynamic:
            split_and_insert_dynamic_data(sheet_table_name, field_names, values, static_column_names, dynamic_column_names)
        else:
            insert_data = {
                "schema": "data",
                "name": sheet_table_name,
                "field_names": field_names,
                "data": values
            }
            insert_row(insert_data)


def check_dynamic_and_get_columns(table_data):
    is_dynamic = is_table_dynamic(table_data)
    if is_dynamic:
        static_column_names, dynamic_column_names = dynamic_mapping_columns(table_data, "data")
        if not static_column_names or not dynamic_column_names:
            is_dynamic = False
    else:
        static_column_names, dynamic_column_names = None, None
    return is_dynamic, static_column_names, dynamic_column_names


def handle_special_keywords(ods_sheet, sheet_name):
    longest_row = find_longest_row(ods_sheet)
    if longest_row is None:
        logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
        return

    header_row_index = 0
    field_names = [f"column_{i}" for i in range(longest_row)]
    return field_names, header_row_index


def handle_standard_keywords(ods_sheet, sheet_name):
    header_row_index = detect_header_row(ods_sheet)
    if header_row_index is None:
        logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
        return

    header_row = ods_sheet.row(header_row_index)
    field_names = sanitize_field_names(header_row)
    field_names = [name for name in field_names if name is not None]
    return field_names, header_row


def process_ods_sheet(ods_sheet, id, table_name):
    sheet_name = ods_sheet.name

    keywords = ["param", "def", "déf", "conf"]

    if any(keyword in sheet_name.lower() for keyword in keywords):
        field_names, header_row_index = handle_special_keywords(ods_sheet, sheet_name)
    else:
        field_names, header_row_index = handle_standard_keywords(ods_sheet, sheet_name)

    valid_columns = range(len(field_names))
    sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"

    table_data = {
        "schema": "data",
        "name": sheet_table_name,
        "field_names": field_names,
        "id": id
    }

    try:
        create_table(table_data)
    except Exception as create_table_error:
        logger.error(f"Error occurred during table creation {sheet_table_name}: {create_table_error}")
        return

    is_dynamic, static_column_names, dynamic_column_names = check_dynamic_and_get_columns(table_data)
    
    
    try:
        process_rows(ods_sheet, header_row_index, valid_columns, field_names, table_name, is_dynamic, static_column_names, dynamic_column_names)
    except Exception as create_table_error:
        logger.error(f"Error uploading the data: {create_table_error}")


def process_ods(id, data, table_name):
    try:
        ods_file = BytesIO(data)
        doc = ezodf.opendoc(ods_file)

        for ods_sheet in doc.sheets:
            process_ods_sheet(ods_sheet, id, table_name)

    except Exception as ods_process_error:
        logger.error(f"An error occurred while processing ODS: {ods_process_error}")
        raise ods_process_error
