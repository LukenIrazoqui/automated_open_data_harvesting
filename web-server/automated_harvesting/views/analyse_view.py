from django.shortcuts import render
from django.db import connection

def analyse(request):
    if request.method == 'POST':
        sql_query = request.POST.get('sql_query')

        if not sql_query:
            return render(request, 'analyse.html', {'error': 'Please provide a SQL query.'})

        try:
            with connection.cursor() as cursor:
                cursor.execute(sql_query)
                result = cursor.fetchall()
                column_names = [desc[0] for desc in cursor.description]

                return render(request, 'analyse.html', {'result': result, 'columns': column_names})

        except Exception as e:
            return render(request, 'analyse.html', {'error': str(e)})

    return render(request, 'analyse.html')
