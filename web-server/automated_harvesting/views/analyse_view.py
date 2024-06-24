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

                return render(request, 'analyse.html', {'result': result})

        except Exception as e:
            return render(request, 'analyse.html', {'error': str(e)})

    return render(request, 'analyse.html')