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

# Create your models here.

class Model_Personne(models.Model):
    
    postnom				    =	models.CharField(max_length = 50, null = True, blank = True, default="")
    prenom					=	models.CharField(max_length = 50, null = True, blank = True, default="")
    nom						=	models.CharField(max_length = 50, null = True, blank = True, default="")
    date_naissance          =   models.DateField(blank=True, null=True)
    image					=	models.CharField(max_length = 500, null = True, blank = True, default="")
    email					=	models.CharField(max_length = 150, null = True, blank = True, default="")
    phone					=	models.CharField(max_length = 50, null = True, blank = True, default="")
    adresse					=	models.CharField(max_length = 500, null = True, blank = True, default="")
    commune_quartier		=	models.ForeignKey("Model_Place", on_delete = models.SET_NULL, related_name="personnes", null = True, blank = True)
    est_actif 				=	models.BooleanField(default = True)
    date_creation			= 	models.DateTimeField(blank=True, null=True)
    auteur					= 	models.ForeignKey("Model_Personne", on_delete = models.SET_NULL, related_name="personnes_creees", null = True, blank = True)
    
    def __str__(self):
        return "%s %s %s" % (self.nom,self.postnom,self.prenom)

    @property    
    def nom_complet(self):
        if self.nom == None:self.nom = ""
        if self.postnom == None:self.postnom = ""
        if self.prenom == None:self.prenom = ""
        return "%s %s %s" % (self.nom,self.postnom,self.prenom)
      
class Model_Employe(Model_Personne):
    profil				    =	models.ForeignKey("Model_Profil", on_delete=models.SET_NULL, blank=True, null=True, related_name="profil_employe")
    poste					=	models.CharField(max_length = 150 , null = True, blank = True, default="")
    user 					=	models.OneToOneField(User, null = True, blank = True, related_name = "personne", on_delete = models.CASCADE)
    est_caissier            =   models.BooleanField(default=False)
    
    def __str__(self):
        return "%s %s %s" % (self.nom,self.postnom,self.prenom)

class Model_Profil(models.Model):
    designation             =   models.CharField(max_length=50)
    est_profil_caisse       =   models.BooleanField(default=False)
    est_total_caisse       =   models.BooleanField(default=False)
    
    def __str__(self):
        return self.designation


class Model_Droit(models.Model):
    menu                    =   models.ForeignKey(Model_Menu, on_delete = models.SET_NULL, related_name="droit_menu", null = True, blank = True)
    droit                   =   models.CharField(max_length=50)
    profils                 =   models.TextField(null = True, blank = True)
    auteur                  =    models.ForeignKey(Model_Personne, related_name="auteur_droit", null = True, blank = True, on_delete=models.SET_NULL)
    
    def __str__(self):
        return ' / '+ str(self.droit)


class Model_Devise(models.Model):
    designation             =   models.CharField(max_length = 50)
    symbole                 =   models.CharField(max_length = 5, null=True, blank=True)
    est_actif               =   models.BooleanField(default=False)
    est_reference           =   models.BooleanField(default=False)
    auteur					= 	models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_devise", null = True, blank = True)

    def __str__(self):
        return self.designation

    @property
    def taux_actuel(self):
        tx = Model_Taux_du_jour.objects.filter(devise_id = self.id, est_actif = True).first()
        if tx:
            return tx.taux
        else:
            return 0

class Model_Taux_du_jour(models.Model):
    date                    =   models.DateTimeField(auto_now_add=True, blank=True, null=True)
    taux                    =   models.FloatField()
    devise                  =   models.ForeignKey(Model_Devise, on_delete=models.CASCADE, related_name="devise_taux")
    est_actif               =   models.BooleanField(default=False)
    auteur					= 	models.ForeignKey(Model_Personne, on_delete = models.SET_NULL, related_name="auteur_taux", null = True, blank = True)
    est_caisse              =   models.BooleanField(default=False)
    est_coffre              =   models.BooleanField(default=False)
    
    def __str__(self):
        localisation = ""
        if self.est_caisse == True:
            localisation = "Caisse"
        elif self.est_coffre == True:
            localisation = "Coffre-fort"
            
        return str(self.taux) +' / '+ localisation +' / '+ str(self.est_actif)



class Model_Place(models.Model):
    designation				=	models.CharField(max_length = 50)
    code_telephone			=	models.CharField(max_length = 5)
    #place_type				=	models.IntegerField(choices = PlaceType)
    code_pays				=	models.CharField(max_length=3, null = True, blank = True, default="")
    parent					=	models.ForeignKey("Model_Place", null = True, blank = True, on_delete = models.CASCADE, related_name="fils")

    def __str__(self):
        return self.designation
    
    @property
    def places_filles(self):
        return Model_Place.objects.filter(parent_id = self.id)