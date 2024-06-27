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


def setup_ods_table(sheet_table_name, field_names, id):
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
        raise create_table_error


def check_dynamic_columns_for_ods(sheet_table_name):
    is_dynamic = is_table_dynamic(sheet_table_name)
    if is_dynamic:
        static_column_names, dynamic_column_names = dynamic_mapping_columns(sheet_table_name, "data")
        if static_column_names is None or dynamic_column_names is None:
            is_dynamic = False
    else:
        static_column_names, dynamic_column_names = None, None
    return is_dynamic, static_column_names, dynamic_column_names


def insert_data_from_row_ods(sheet_table_name, field_names, values, is_dynamic, static_column_names, dynamic_column_names):
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


def process_ods_rows(ods_sheet, header_row_index, valid_columns, field_names, sheet_table_name, is_dynamic, static_column_names, dynamic_column_names):
    for row_idx, row in enumerate(ods_sheet.rows()):
        if row_idx <= header_row_index:
            continue

        row_data = [row[index].value for index in valid_columns]
        if not any(cell is not None for cell in row_data):
            continue

        values = [str(value) if value is not None else '' for value in row_data]
        if len(values) != len(field_names):
            raise ValueError("Number of values in row doesn't match number of fields")

        insert_data_from_row_ods(sheet_table_name, field_names, values, is_dynamic, static_column_names, dynamic_column_names)


def handle_ods_keywords(ods_sheet, sheet_name):
    keywords = ["param", "def", "déf", "conf"]

    if any(keyword in sheet_name.lower() for keyword in keywords):
        longest_row = find_longest_row(ods_sheet)
        if longest_row is None:
            logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
            return None, None

        header_row_index = 0
        field_names = [f"column_{i}" for i in range(longest_row)]
    else:
        header_row_index = detect_header_row(ods_sheet)
        if header_row_index is None:
            logger.warning(f"No header row detected in sheet '{sheet_name}'. Skipping this sheet.")
            return None, None

        header_row = ods_sheet.row(header_row_index)
        field_names = [name for name in sanitize_field_names(header_row) if name != 'None']

    return field_names, header_row_index


def process_ods_sheet(ods_sheet, sheet_name, table_name, id):
    field_names, header_row_index = handle_ods_keywords(ods_sheet, sheet_name)
    if field_names is None or header_row_index is None:
        return

    valid_columns = range(len(field_names))
    sheet_table_name = f"{table_name}_{sanitize_table_name(sheet_name)}"

    try:
        setup_ods_table(sheet_table_name, field_names, id)
    except Exception:
        return

    is_dynamic, static_column_names, dynamic_column_names = check_dynamic_columns_for_ods(sheet_table_name)

    try:
        process_ods_rows(ods_sheet, header_row_index, valid_columns, field_names, sheet_table_name, is_dynamic, static_column_names, dynamic_column_names)
    except Exception as create_table_error:
        logger.error(f"An error occurred while uploading the data for sheet {sheet_name}: {create_table_error}")


def process_ods(id, data, table_name):
    try:
        ods_file = BytesIO(data)
        doc = ezodf.opendoc(ods_file)

        for ods_sheet in doc.sheets:
            sheet_name = ods_sheet.name
            process_ods_sheet(ods_sheet, sheet_name, table_name, id)
    except Exception as ods_process_error:
        logger.error(f"An error occurred while processing ODS: {ods_process_error}")
        raise ods_process_error
