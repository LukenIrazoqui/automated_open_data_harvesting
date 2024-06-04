import re
import logging

# Configure logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)


def sanitize_field_names(field_names):
    try:
        if isinstance(field_names, list) and all(isinstance(field, str) for field in field_names):
            cleaned_names = [
                re.sub(r'^\ufeff', '', field.strip()) for field in field_names
            ]
        elif hasattr(field_names, '__iter__'):
            cleaned_names = [
                re.sub(r'^\ufeff', '', str(cell.value).strip()) for cell in field_names
            ]
        elif hasattr(field_names, 'field_names'):
            cleaned_names = [
                re.sub(r'^\ufeff', '', field.strip()) for field in field_names.field_names
            ]
        elif hasattr(field_names, 'fields'):
            cleaned_names = [
                re.sub(r'^\ufeff', '', field.strip()) for field in field_names.fields
            ]
        else:
            raise ValueError("Invalid field names format")

        cleaned_names = [
            re.sub(r'[Nn]°', 'numero', field) for field in cleaned_names
        ]
        cleaned_names = [
            re.sub(r'[ \n]', '_', field) for field in cleaned_names
        ]
        cleaned_names = [
            re.sub(r'[èé]', 'e', field) for field in cleaned_names
        ]
        cleaned_names = [
            re.sub(r'à', 'a', field) for field in cleaned_names
        ]
        cleaned_names = [
            re.sub(r'[^a-zA-Z0-9_]', '', field) for field in cleaned_names
        ]
    except Exception as e:
        logger.error(f"Error sanitizing field names: {e}")
        raise e

    return cleaned_names


def truncate_table_name(table_name, max_length=63):
    try:
        if len(table_name) <= max_length:
            return table_name
        else:
            words = table_name.split('_')
            truncated_words = []

            for word in words:
                if word.isdigit():
                    truncated_words.append(word)
                elif len(word) < 4:
                    continue
                else:
                    truncated_words.append(word[0:3])

            abbreviated_name = '_'.join(truncated_words)

            abbreviated_name = abbreviated_name[:max_length]
            logger.info(f"Truncated table name to '{abbreviated_name}'")

            return abbreviated_name
    except Exception as e:
        logger.error(f"Error truncating table name: {e}")
        raise e


def sanitize_table_name(file_name):
    try:
        table_name = re.sub(r'\W+', '_', file_name)
        table_name = re.sub(r'[èé]', 'e', table_name)
        table_name = re.sub(r'à', 'a', table_name)

        table_name = truncate_table_name(table_name)

        if not table_name[0].isalpha() and table_name[0] != '_':
            table_name = '_' + table_name

        logger.info(f"Final sanitized table name: '{table_name}'")

        return table_name
    except Exception as e:
        logger.error(f"Error sanitizing table name: {e}")
        raise e
