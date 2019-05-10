from django.shortcuts import render
from .models import ProgramTable, mergedTables
from .scriptETL import showMissingValues

# Create your views here.
def home(request):
    return render(request, 'home.html')

# def descriptiveStats(request):
#     query_results=ProgramTable.objects.all()
#     context={'query_results':query_results}
#     return render(request, 'descriptiveStats.html', context)

def descriptiveStats(request):
    # https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
            #     City.objects.values('country__name') \
            # .annotate(country_population=Sum('population')) \
            # .order_by('-country_population')

    query_results=mergedTables.objects.all()
    # .count()
    context={'query_results':query_results}
    return render(request, 'descriptiveStats2.html', context)

def etl(request):
    qs = ProgramTable.pdobjects.all()
    df = qs.to_dataframe()
    df_new=showMissingValues(df)
    context=df_new.to_dict('split')
    return render(request, 'etl.html', context)

def maps(request):
    return render(request, 'maps.html')