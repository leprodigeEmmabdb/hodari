# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max,Sum
import datetime
import json
from App_Configuration.models import Model_Personne

from MainApp.Utils.utils import utils
from App_Configuration.models import Model_Personne

class Model_Type_Courrier(models.Model):
    designation                              =   models.CharField(max_length=100)
    
    def __str__(self):
        return self.designation


class Model_Nature_Courrier(models.Model):    
    designation                              =   models.CharField(max_length=100)
    
    def __str__(self):
        return self.designation
    

class Model_Exped_Destinataire(Model_Personne):
    def __str__(self):
        return self.nom


class Model_Courrier(models.Model):
    numero                              =   models.CharField(max_length=25, blank=True, null=True)
    date_creation                       =   models.DateTimeField(auto_now_add=True)
    type                                =   models.ForeignKey(Model_Type_Courrier, on_delete=models.CASCADE, related_name="type_courriers")
    nature                              =   models.ForeignKey(Model_Nature_Courrier, on_delete=models.CASCADE, related_name="nature_courriers")
    expediteur                          =   models.ForeignKey("App_Configuration.Model_Personne", on_delete=models.CASCADE, related_name="expediteur_courriers")
    date_envoi                          =   models.DateTimeField(blank=True, null=True)
    objet                               =   models.TextField()
    date_reception                      =   models.DateTimeField(blank=True, null=True)
    numero_enregistrement               =   models.CharField(max_length=25)
    date_reponse                        =   models.DateTimeField(blank=True, null=True)
    remarque                            =   models.TextField(blank=True, null=True)
    est_traite                          =   models.BooleanField(default=False)
    date_traitement                     =   models.DateTimeField(null=True, blank=True)

    def __str__(self):
        return self.numero_enregistrement

    @property
    def etat(self):
        if self.est_traite == False:
            return 'Non traité'
        else:
            return 'Traité'

    @property
    def destinataires(self):
        return Model_Destinataire_Courrier.objects.filter(courrier_id = self.pk)
    
    @property
    def documents(self):
        return Model_Document_Courrier.objects.filter(courrier_id = self.pk)


class Model_Destinataire_Courrier(models.Model):
    destinataire                        =   models.ForeignKey("App_Configuration.Model_Personne", on_delete=models.CASCADE, related_name="destinataire_courrier")
    courrier                            =   models.ForeignKey(Model_Courrier, on_delete=models.CASCADE, related_name="courrier_destinataire")
    action                              =   models.TextField()

    def __str__(self):
        return self.destinataire.nom_complet +' / ' + self.courrier.numero



class Model_Document_Courrier(models.Model):
    courrier                            =   models.ForeignKey(Model_Courrier, on_delete=models.CASCADE, related_name="courrier_docs")
    url_document			=	models.CharField(max_length = 150, null = True, blank = True, default="")
    description             =   models.CharField(max_length = 150, null = True, blank = True, default="")
    creation_date			=	models.DateTimeField(auto_now = True)
    type                    =   models.CharField(max_length = 50, blank=True, null=True)
    auteur					=	models.ForeignKey("App_Configuration.Model_Personne", related_name="documents_courr",on_delete = models.SET_NULL,null = True, blank = True)
    #created                 =   models.DateTimeField(auto_now_add=True)
    def __str__(self):
        return self.courrier.numero_enregistrement