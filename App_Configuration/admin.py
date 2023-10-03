from django.contrib import admin
from . import models
# Register your models here.


admin.site.register(models.Model_Devise)
admin.site.register(models.Model_Employe)
admin.site.register(models.Model_Personne)
admin.site.register(models.Model_Place)

admin.site.register(models.Model_Taux_du_jour)
admin.site.register(models.Model_Profil)

admin.site.register(models.Model_Droit)
