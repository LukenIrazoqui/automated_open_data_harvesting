from django.shortcuts import render
from django.http import Http404, JsonResponse
from django.db import connection
import json

def view_table_data(request, table_name):
    schema_name = 'data'

    with connection.cursor() as cursor:
        cursor.execute(f"SELECT table_name FROM information_schema.tables WHERE table_schema = '{schema_name}'")
        valid_tables = [row[0] for row in cursor.fetchall()]

    if table_name not in valid_tables:
        raise Http404("Table not found")

    with connection.cursor() as cursor:
        cursor.execute(f'SELECT * FROM data."{table_name}" ORDER BY id ASC')
        columns = [col[0] for col in cursor.description]
        rows = cursor.fetchall()

    context = {
        'table_name': table_name,
        'columns': columns,
        'rows': rows,
    }
    
    return render(request, 'datasets_views/table_data_view.html', context)

def submit_columns(request):
    if request.method == 'POST':
        data = json.loads(request.body)
        table_name = data.get('table_name')
        static_columns = data.get('static_columns', [])
        dynamic_columns = data.get('dynamic_columns', [])

        static_table_name = f"{table_name}_s"
        dynamic_table_name = f"{table_name}_d" 
        view_name = f"{table_name}_view"

        with connection.cursor() as cursor:
            # Drop tables if they already exist
            cursor.execute(f'DROP VIEW IF EXISTS data."{view_name}"')
            cursor.execute(f"DROP TABLE IF EXISTS data.{dynamic_table_name}")
            cursor.execute(f"DROP TABLE IF EXISTS data.{static_table_name}")

            # Add table names to the tables and get back the id
            cursor.execute(f"UPDATE table_names SET dynamic = true WHERE name = '{table_name}' RETURNING id;")
            table_name_id = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO dynamic_data_table_names (name) VALUES ('{dynamic_table_name}') RETURNING id")
            dynamic_table_name_id = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO static_data_table_names (name) VALUES ('{static_table_name}') RETURNING id")
            static_table_name_id = cursor.fetchone()[0]
            cursor.execute(f"INSERT INTO view_names (name) VALUES ('{view_name}') RETURNING id")
            view_name_id = cursor.fetchone()[0]

            # Add to the mapping table
            cursor.execute(f'INSERT INTO dynamic_table_mapping (id_table_names, id_static_data_table_names, id_dynamic_data_table_names, id_view_names) VALUES ({table_name_id}, {dynamic_table_name_id}, {static_table_name_id}, {view_name_id})')

            # Create static table
            static_columns_definition = ', '.join([f'"{col}" VARCHAR(255)' for col in static_columns])
            cursor.execute(f'CREATE TABLE data."{static_table_name}" (id SERIAL PRIMARY KEY, {static_columns_definition})')

            # Create dynamic table with a foreign key reference to the static table
            dynamic_columns_definition = ', '.join([f'"{col}" VARCHAR(255)' for col in dynamic_columns])
            cursor.execute(f'CREATE TABLE data."{dynamic_table_name}" (id SERIAL PRIMARY KEY, "static_id" INTEGER REFERENCES data."{static_table_name}"(id), {dynamic_columns_definition})')

            # Populate static table and keep a mapping of static column values to static table IDs
            static_columns_quoted = ', '.join([f'"{col}"' for col in static_columns])
            cursor.execute(f'SELECT DISTINCT {static_columns_quoted} FROM data."{table_name}"')
            static_data = cursor.fetchall()
            static_data_mapping = {}
            for row in static_data:
                cursor.execute(f'INSERT INTO data."{static_table_name}" ({static_columns_quoted}) VALUES ({", ".join(["%s"] * len(static_columns))}) RETURNING id', row)
                static_id = cursor.fetchone()[0]
                static_data_mapping[tuple(row)] = static_id

            # Populate dynamic table with a reference to the static table ID
            dynamic_columns_quoted = ', '.join([f'"{col}"' for col in dynamic_columns])
            cursor.execute(f'SELECT id, {static_columns_quoted}, {dynamic_columns_quoted} FROM data."{table_name}"')
            for row in cursor.fetchall():
                row_id = row[0]
                static_values = row[1:len(static_columns) + 1]
                dynamic_values = row[len(static_columns) + 1:]
                static_id = static_data_mapping[tuple(static_values)]
                cursor.execute(f'INSERT INTO data."{dynamic_table_name}" ("static_id", {dynamic_columns_quoted}) VALUES (%s, {", ".join(["%s"] * len(dynamic_columns))})', [static_id] + list(dynamic_values))

            columns_combined = ', '.join([f'"{col}"' for col in static_columns] + [f'"{col}"' for col in dynamic_columns])
            cursor.execute(f'''
                CREATE VIEW data."{view_name}" AS
                SELECT {columns_combined}
                FROM data."{static_table_name}" s
                JOIN data."{dynamic_table_name}" d ON s.id = d.static_id
            ''')

        return JsonResponse({'status': 'success'})

    return JsonResponse({'status': 'fail'}, status=400)