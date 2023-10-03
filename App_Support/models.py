# -*- coding: utf-8 -*-
from __future__ import unicode_literals
from typing import MappingView
from unicodedata import normalize
from cffi import model

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max,Sum
import datetime
import json

from MainApp.Utils.utils import utils
from MainApp.models import Model_Menu
from App_Configuration.models import Model_Devise, Model_Personne

# Create your models here.

class Model_Type_Reclamation(models.Model):
    designation                             =   models.CharField(max_length=50)

    def __str__(self):
        return self.designation



class Model_Reclamation(models.Model):
    numero                                  =   models.CharField(max_length=30)
    date_creation                           =   models.DateTimeField(auto_now_add=True)
    type                                    =   models.ForeignKey(Model_Type_Reclamation, on_delete=models.CASCADE, related_name='type_reclamations')
    utilisateur                             =   models.ForeignKey('MakutaTransfert.Model_Utilisateur', on_delete=models.CASCADE, related_name="user_reclamation")
    description                             =   models.TextField(blank=True, null=True)
    resolu                                  =   models.BooleanField(default=False)      
    transfert                               =   models.CharField(max_length=30, blank=True, null=True)                                 

    def __str__(self):
        return self.numero

    @property
    def etat(self):
        if self.resolu == True:
            return 'Repondu'
        else:
            return 'En attente de reponse'

    @property
    def last_comment(self):
        try:
            comment = Model_Commentaire.objects.filter(reclamation_id = self.id).order_by('-id')[0]
            return comment.commentaire
        except Exception as e:
            return ""
    

class Model_Commentaire(models.Model):
    
    reclamation				=	models.ForeignKey(Model_Reclamation, related_name="commentaire_recl",on_delete = models.CASCADE)
    commentaire    			=	models.TextField()
    creation_date			=	models.DateTimeField(auto_now = True)
    auteur					=	models.ForeignKey("App_Configuration.Model_Personne", related_name="auteurs_comm",on_delete = models.SET_NULL,null = True, blank = True)

    def __str__(self):
        return self.commentaire

class Model_Fichier(models.Model):
    reclamation             =   models.ForeignKey(Model_Reclamation, on_delete=models.CASCADE, related_name='fichier_reclemation')
    url                     =   models.CharField(max_length=500)
    nom_fichier             =   models.CharField(max_length=500)
    creation_date           =   models.DateTimeField(auto_now_add=True, blank=True, null=True)


    def __str__(self):
        return self.nom_fichier
