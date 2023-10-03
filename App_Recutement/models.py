# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max,Sum
import datetime
import json

from MainApp.Utils.utils import utils
from MainApp.models import Model_Menu
from App_Configuration.models import *


# Create your models here.
Typestatus =    (
    (1, "en cours"),
    (2, "cloturée"),
)
Typestatusdossier=(
    (1, "en attente du verification"),
    (2, "accepté"),
    (3, "décliner"),
    (3, "cv deposé"),
)
etatdossier =(
    (1, "ouvert"),
    (2, "fermé"),
)


class Model_Offre(models.Model):
    reference      =   models.CharField(max_length=5000,blank=True,null=True)
    titre          =   models.CharField(max_length=5000,blank=True,null=True)
    description    =   models.TextField(blank=True,null=True)
    datepublish    =   models.DateTimeField(blank=True, null=True)
    localisation   =   models.CharField(max_length=5000,blank=True, null=True)
    typecontrat    =   models.CharField(max_length=5000,blank=True, null=True)
    dateclose      =   models.DateTimeField(blank=True, null=True)
    qualification  =   models.TextField(blank=True, null=True)
    proccess       =   models.TextField(blank=True, null=True)
    entreprise     =   models.CharField(max_length=5000,blank=True, null=True)
    responsable    =   models.CharField(max_length=5000,blank=True, null=True)
    tache          =   models.TextField(blank=True, null=True)
    status         =   models.IntegerField(choices=Typestatus, null = True, blank = True)
    est_actif      =   models.BooleanField(default = True)
    datecreate     =   models.DateTimeField(auto_now_add=True)
    auteur	       =   models.ForeignKey("App_Configuration.Model_Personne", on_delete = models.SET_NULL, related_name="offre_auteur", null = True, blank = True)

    def __str__(self):
        return self.reference


class Model_Candidat(Model_Personne):
    reference      =   models.CharField(max_length=50,blank=True,null=True)
    profession     =   models.ForeignKey("Model_Poste_Recrutement",on_delete=models.SET_NULL,blank=True,null=True, related_name="poste_candidat")
    datecreate     =   models.DateTimeField(auto_now_add=True)
    
    def __str__(self):
        return self.reference

    def all_candidature(self):
        candidatures = Model_Candidature.objects.filter(candidat_id = self.id)
        return candidatures

class DiplomaFile(models.Model):
    file = models.FileField(upload_to="media",blank=True,null=True)


class Model_Candidature(models.Model):
    reference      =   models.CharField(max_length=50,blank=True,null=True)
    dateinscrit    =   models.DateTimeField(auto_now_add=True)
    motivation     =   models.FileField(upload_to ='media',blank=True,null=True)
    diplome        =   models.ManyToManyField(DiplomaFile)
    offre	       =   models.ForeignKey("Model_Offre", on_delete = models.CASCADE, related_name="candidature_offre", null = True, blank = True)
    candidat	   =   models.ForeignKey("Model_Candidat", on_delete = models.CASCADE, related_name="candidature_candidat", null = True, blank = True)
    status         =   models.IntegerField(choices=Typestatusdossier, null = True, blank = True)
    est_depot_cv   =   models.BooleanField(default=False)
    path_cv        =   models.CharField(max_length=500, blank=True, null=True)
    path_cv2       =   models.FileField(upload_to ='CV/DEPOT',blank=True,null=True)
    deja_ouvert    =   models.BooleanField(default=False)
    
    def __str__(self):
        return self.reference


class Model_Domaine_Recrutement(models.Model):
    designation                     =   models.CharField(max_length=200)
    
    def __str__(self):
        return self.designation
    
class Model_Poste_Recrutement(models.Model):
    designation                     =   models.CharField(max_length=200)
    domaine                         =   models.ForeignKey(Model_Domaine_Recrutement,on_delete=models.CASCADE, blank=True,null=True,related_name="domaines_poste")
    
    def __str__(self):
        return self.designation