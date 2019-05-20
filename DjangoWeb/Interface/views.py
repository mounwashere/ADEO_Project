from django.shortcuts import render
from dataCRUD.models import *
from .scriptETL import *
from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from .forms import ContactForm
from django.core.mail import EmailMessage
from django.shortcuts import redirect
from django.http import HttpResponse
from django.contrib.auth.decorators import user_passes_test
from django.db.models import Max

# Create your views here.
@login_required
def home(request):
    return render(request, 'home.html')

# def descriptiveStats(request):
#     query_results=ProgramTable.objects.all()
#     context={'query_results':query_results}
#     return render(request, 'descriptiveStats.html', context)

@login_required
def descriptiveStats(request):
    # https://simpleisbetterthancomplex.com/tutorial/2016/12/06/how-to-create-group-by-queries.html
            #     City.objects.values('country__name') \
            # .annotate(country_population=Sum('population')) \
            # .order_by('-country_population')

    query_results=mergedTables.objects.all()
    # .count()
    context={'query_results':query_results}
    return render(request, 'descriptiveStats2.html', context)

@login_required
@user_passes_test(lambda u: u.is_superuser)
def etl(request):
    df_new=showMissingValues( PRG_STUDENT_SITE.pdobjects.all().to_dataframe() )

    df1_new=showMissingValues( ADR_STUDENTS.pdobjects.all().to_dataframe() )

    df2_new=showMissingValues( STUDENT_INTERNSHIP.pdobjects.all().to_dataframe() )

    context={'PRG_STUDENT_SITE':df_new.to_dict('split'),
             'ADR_STUDENTS':df1_new.to_dict('split'),
             'STUDENT_INTERNSHIP':df2_new.to_dict('split')
            }
    
    return render(request, 'etl.html', context)

@login_required
def etl_mergetables(request):    
    version=int(mergedTables.objects.all().aggregate(Max('idCSV'))['idCSV__max']) + 1
    description='Delete Null Values'
    ADR=redefineDFTypes(ADR_STUDENTS.pdobjects.all().to_dataframe())    
    PRG=redefineDFTypes(PRG_STUDENT_SITE.pdobjects.all().to_dataframe())
    STU=redefineDFTypes(STUDENT_INTERNSHIP.pdobjects.all().to_dataframe())
       
    df=mergeTables(ADR,PRG,STU)
    numberlines = df.ID_ANO.count()
    table = mergedTables.objects
    #writeDF2Table(df, table, version, description )

    df=showMissingValues( mergedTables.pdobjects.filter(idCSV=version).to_dataframe() )
    context={'MERGEDTABLES' :df.to_dict('split') ,
             'NUMBERLINES'  :numberlines ,
             'VERSION'      :str(version) + " - " + description
            }
    return render(request, 'etl_mergedtables.html', context)

@login_required
def etl_mergetablesRF(request):    
    version=int(mergedTables.objects.all().aggregate(Max('idCSV'))['idCSV__max']) + 1
    description='Fill with RandomForest Algorithm'
    ADR=redefineDFTypes(ADR_STUDENTS.pdobjects.all().to_dataframe())    
    PRG=redefineDFTypes(PRG_STUDENT_SITE.pdobjects.all().to_dataframe())
    STU=redefineDFTypes(STUDENT_INTERNSHIP.pdobjects.all().to_dataframe())
       
    df=mergeTables(ADR,PRG,STU)
    numberlines = df.ID_ANO.count()
    table = mergedTables.objects
    writeDF2Table(df, table, version, description )

    df=showMissingValues( mergedTables.pdobjects.filter(idCSV=version).to_dataframe() )
    context={'MERGEDTABLES' :df.to_dict('split') ,
             'NUMBERLINES'  :numberlines ,
             'VERSION'      :str(version) + " - " + description
            }
    return render(request, 'etl_mergedtables.html', context)


@login_required
def maps(request):
    return render(request, 'maps.html')

@login_required
def contact_us(request):
    form_class = ContactForm
    if request.method == 'POST':
        form = form_class(data=request.POST)

        if form.is_valid():
            contact_name = request.POST.get('contact_name', '')
            contact_email = request.POST.get('contact_email', '')
            form_content = request.POST.get('content', '')

            # Email the profile with the
            # contact information
            template = get_template('contacttemplate.txt')
            context = {
                'contact_name': contact_name,
                'contact_email': contact_email,
                'form_content': form_content,
                }
            content = template.render(context)

            email = EmailMessage(
                "New contact form submission",
                content,
                "Your website" +'',
                ['induraj2020@gmail.com'],
                headers = {'Reply-To': contact_email }
            )
            email.send()
            return redirect('home')

    return render(request, 'contact_us.html', {
        'form': form_class,
    })

#indu 17-may
def is_valid_queryparam(param):
    if (param!='Choose...'):
        return(True)

def is_valid_queryparam2(param1,param2):
    if (param1!='Choose...') and (param2 != 'Choose...'):
        return(True)

def checking(request):
    #query_results= mergedTables.objects.all()
    #query_results=mergeTables.objects.filter(item=item).distinct('ID_ANO')
    #query_results= mergedTables.objects.raw('SELECT DISTINCT PRG FROM mergedTables')

    # .count()
    #context = {'query_results': query_results}
    query_results=mergedTables.objects.all()

    df_new_prg = return_distinct_prg(mergedTables.pdobjects.all().to_dataframe())
    df_new_ville = return_distinct_ville(mergedTables.pdobjects.all().to_dataframe())
    df_new_cp = return_distinct_cp(mergedTables.pdobjects.all().to_dataframe())
    df_new_rem = return_distinct_rem(mergedTables.pdobjects.all().to_dataframe())
    df_new_year= return_distinct_year(mergedTables.pdobjects.all().to_dataframe())


    prg_filtered= request.GET.get('program')
    #print(prg_filtered)
    vil_filtered= request.GET.get('ville')
    #print(vil_filtered)
    cod_filtered= request.GET.get('code_postal')
    rem_filtered= request.GET.get('remuneration')
    #print(rem_filtered)
    yfr_filtered=request.GET.get('years_from')
    #print(yfr_filtered)
    yto_filtered=request.GET.get('years_to')
    qs= query_results
    message=''

    if is_valid_queryparam(prg_filtered):
        qs=qs.filter(PRG=prg_filtered)
        #qs= qs & query_results.filter(ADR_VILLE='CERGY' )
        #print(str(qs.query))
        #print(prg_filtered)

    if is_valid_queryparam(vil_filtered):
        qs=qs.filter(ADR_VILLE=vil_filtered)
        print(qs)

    if is_valid_queryparam(cod_filtered):
        qs=qs.filter(ADR_CP=cod_filtered)

    if is_valid_queryparam(rem_filtered):
        qs=qs.filter(REMUNERATION=rem_filtered)

    elif is_valid_queryparam2(yfr_filtered,yto_filtered):
        if (yfr_filtered <= yto_filtered):
            yfr_filtered=(int)(yfr_filtered)
            yfr_anotherhalf= yfr_filtered+1
            yto_filtered=(int)(yto_filtered)
            yto_anotherhalf = yto_filtered + 1
            yfr_filtered  =(str)(yfr_filtered)
            yto_filtered  = (str)(yto_filtered)
            yfr_anotherhalf = (str)(yfr_anotherhalf)
            yto_anotherhalf = (str)(yto_anotherhalf)
            yfr_filtered=yfr_filtered + '/' + (yfr_anotherhalf)
            yto_filtered=yto_filtered + '/' + (yto_anotherhalf)
            print('\n')
            print('helllooooooo')
            print(yfr_filtered)
            qs=query_results.filter(ANNEE_SCOLAIRE__gte=yfr_filtered,ANNEE_SCOLAIRE__lte=yto_filtered)
        else:
            message="Years From-To not correct"

    #qs = query_results

    context = {'prg': df_new_prg,
               'ville': df_new_ville,
               'cp': df_new_cp,
               'rem': df_new_rem,
               'year':df_new_year,
               'message':message,
               'query_results':qs,
               }


    return render(request,'checking.html',context)
    #return HttpResponse('<h1> hi </h1>')