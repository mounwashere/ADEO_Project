from django.db import models
from django_pandas.managers import DataFrameManager

#MIGRATED FOR dataCRUD\models.py

# class ProgramTable(models.Model):
#     ID_ANO       =models.IntegerField()
#     PRG          =models.CharField(max_length=120)
#     ANNE_SCOLAIRE=models.CharField(max_length=120)
#     SITE         =models.CharField(max_length=120)

#     pdobjects = DataFrameManager() 
    
#     class Meta:
#         db_table = 'PRG_STUDENT_SITE'

# class mergedTables(models.Model):
#     # id      =models.IntegerField()
#     ID_ANO  =models.CharField(max_length=120)
#     PRG      =models.CharField(max_length=120)
#     ANNEE_SCOLAIRE =models.CharField(max_length=120)
#     SITE    =models.CharField(max_length=120)
#     ADR_CP  =models.IntegerField()
#     ADR_VILLE =models.CharField(max_length=120)
#     ADR_PAYS   =models.CharField(max_length=120)
#     ANNEE   =models.CharField(max_length=120)
#     ENTREPRISE =models.CharField(max_length=120)
#     CODE_POSTAL =models.IntegerField()
#     VILLE =models.CharField(max_length=120)
#     PAYS =models.CharField(max_length=120)
#     SUJET =models.CharField(max_length=120)
#     REMUNERATION =models.CharField(max_length=120)
#     # REMUNERATION =models.DecimalField()
#     # idCSV =models.IntegerField()

#     objects = models.Manager()
#     pdobjects = DataFrameManager() 

#     class Meta:
#         db_table = 'mergedtables'