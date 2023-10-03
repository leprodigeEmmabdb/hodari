## -*- coding: utf-8 -*-
from App_Support.models import Model_Commentaire, Model_Fichier, Model_Reclamation

import os

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.template import loader,RequestContext
from django.views import generic
from django.views.generic.edit import CreateView, UpdateView, DeleteView
from django.core.files.storage import default_storage
from django.urls import reverse_lazy, reverse
from django.contrib import messages
from django.utils import timezone
from django.core import serializers

from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Sum, Min, Count

import datetime
import json
import array
from django.db.models import Sum
import time

from MainApp.Utils.EmailThread import send_async_mail


from django.template.loader import render_to_string
from weasyprint import HTML
import tempfile

from django.utils.dateparse import parse_date 

from os import listdir
from os.path import isfile, join

from django.contrib.staticfiles.templatetags.staticfiles import static
from django.utils.safestring import mark_safe
from django.views.generic.base import TemplateView

from MainApp.Utils.auth import auth
from MainApp.Utils.utils import utils

from django.contrib.auth.models import User, Group

from App_Configuration.models import *

from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse


from django.db.models.functions import (TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth)

import random
import string
import time
import math


from django.shortcuts import get_object_or_404 
from weasyprint import HTML, CSS

from MainApp.Utils.report_css import report_css
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache


from MainApp.Utils.utils import utils


def get_index(request):
    try:
        droit = "VOIR_TABLEAU_DE_BORD_SUPPORT"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        
        utilisateur = auth.getEmploye(request)
        today = datetime.datetime.today()
       
        context = {
            'title' : 'Accueil',
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'menu' : menu, # 1,
        }
        
        template = loader.get_template("Soluplus/App_Support/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)


def get_lister_reclamation(request):
    droit = "VOIR_TOUTES_RECLAMATIONS"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse   


    model = Model_Reclamation.objects.all().order_by('-id')

    context = {
        'title' : 'Liste des Reclamations',
        'model' : model,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Support/reclamation/list.html")
    return HttpResponse(template.render(context, request))


def get_lister_reclamation_attente(request):
    droit = "VOIR_RECLAMATIONS_EN_ATTENTE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse   


    model = Model_Reclamation.objects.filter(resolu = False).order_by('-id')

    context = {
        'title' : 'Liste des Reclamations en attente',
        'model' : model,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Support/reclamation/list.html")
    return HttpResponse(template.render(context, request))

def get_details_reclamation(request, ref):

    droit = "VOIR_RECLAMATIONS_EN_ATTENTE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse

    try:
        ref = int(ref)
        reclamation = Model_Reclamation.objects.get(pk = ref)
        #membres = dao_reclamation.toListMembreAffaire(reclamation.id)
        fichiers = Model_Fichier.objects.filter(reclamation_id = ref)
        commentaires = Model_Commentaire.objects.filter(reclamation_id = reclamation.id)

        
        context = {
            'title' : reclamation.numero ,
            'model' : reclamation,
            'commentaires' : commentaires,
            'fichiers' : fichiers,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Support/reclamation/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("ERREUR DETAIL")
        print(e)
        return HttpResponseRedirect(reverse('app_support_list_reclamations'))


def get_commentaire(request, ref):
    
    try:

        droit = "RESOUDRE_RECLAMATION"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse    
        

        ref = int(ref)
        reclamation = Model_Reclamation.objects.get(pk = ref)
        
        context = {
            'title' : reclamation.numero,
            'model' : reclamation,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Support/reclamation/commentaire/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("ERREUR")
        print(e)
        return HttpResponseRedirect(reverse('app_support_list_reclamations'))


def post_commentaire(request):
    
    try:
    
        id = int(request.POST["ref"])
        auteur = auth.getEmploye(request)
        reclamation = Model_Reclamation.objects.get(pk=id)
        comment = request.POST["commentaire"]

        print(comment)
    
        commentaire = Model_Commentaire()
        commentaire.reclamation_id = id
        commentaire.commentaire = comment
        commentaire.auteur_id = auteur.id
        commentaire.save()

        reclamation.resolu = True
        reclamation.save()
        
        return HttpResponseRedirect(reverse('app_support_details_reclamation', args=(id,)))
        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_support_list_reclamations'))
