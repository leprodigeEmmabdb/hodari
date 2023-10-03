from django.contrib import admin

# Register your models here.
from .models import *

admin.site.register(Model_Offre)
admin.site.register(Model_Candidat)
admin.site.register(Model_Candidature)
admin.site.register(Model_Domaine_Recrutement)
admin.site.register(Model_Poste_Recrutement)

