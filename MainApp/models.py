# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.db import models
from django.contrib.auth.models import User, Group
from django.utils import timezone
from django.db.models import Max,Sum
import datetime
import json

# Create your models here.

class Model_Module(models.Model):
    designation             =   models.CharField(max_length = 30)
    est_actif               =   models.BooleanField(default=False)
    url                     =   models.CharField(max_length=30, blank=True, null=True)
    order                   =   models.IntegerField()
    icon                    =   models.CharField(max_length = 50, blank=True, null=True)

    def __str__(self):
        return self.designation
    
class Model_Groupe_Menu(models.Model):
    designation             =   models.CharField(max_length=50)
    icon                    =   models.CharField(max_length=50, blank=True, null=True)
    ordre                   =   models.IntegerField()
    
    def __str__(self):
        return self.designation
    
    @property
    def menu_ordres(self):
        data = []
        menu = Model_Menu.objects.filter(groupe__pk = self.id)
        for i in menu:
            data.append(i.ordre)
        return data
    
class Model_Menu(models.Model):
    module                  =   models.ForeignKey(Model_Module, on_delete=models.CASCADE, related_name="module_menu")
    groupe                  =   models.ForeignKey(Model_Groupe_Menu, on_delete=models.SET_NULL, blank=True, null=True, related_name="groupe_menu")
    designation             =   models.CharField(max_length=50)
    ordre                   =   models.IntegerField(unique=True)
    icon                    =   models.CharField(max_length=50, blank=True, null=True)
    url                     =   models.CharField(max_length=50, blank=True, null=True)
    

    
    def __str__(self):
        return self.module.designation + ' / '+ self.designation
    
    @property
    def group(self):
        group = Model_Groupe_Menu.objects.filter(pk = self.groupe_id).first()
        return group
            