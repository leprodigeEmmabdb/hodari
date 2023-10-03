from django.contrib import admin

# Register your models here.

from .models import *

admin.site.register(Model_Courrier)
admin.site.register(Model_Nature_Courrier)
admin.site.register(Model_Type_Courrier)
admin.site.register(Model_Exped_Destinataire)
admin.site.register(Model_Destinataire_Courrier)
admin.site.register(Model_Document_Courrier)
