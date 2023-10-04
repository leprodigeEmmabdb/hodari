## -*- coding: utf-8 -*-
from __future__ import unicode_literals
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
#from weasyprint import HTML
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

from App_Recutement.models import *


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
#from weasyprint import HTML, CSS

from MainApp.Utils.report_css import report_css
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache
from _datetime import date
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.db.models import Q

# Create your views here.


def get_index(request):
    try:
        droit = "VOIR_TABLEAU_DE_BORD_RECRUTEMENT"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        utilisateur = auth.getEmploye(request)
        today = datetime.datetime.today()
        offres = Model_Offre.objects.all().count()
        candidat = Model_Candidat.objects.all().count()

        offres_val = Model_Offre.objects.filter(status = 1).count()
        offres_decl = Model_Offre.objects.filter(status = 2).count()

        context = {
            'title' : 'Accueil',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'offres': offres,
            'candidat': candidat,
            'offres_val': offres_val,
            'offres_decl': offres_decl
        }
        template = loader.get_template("Soluplus/App_Recutement/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index Recrutement")
        print(e)
        # return HttpResponseRedirect(reverse("index"))



def get_list_offres_admin(request):
    try:
        droit = "VOIR_LIST_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        utilisateur = auth.getEmploye(request)
        offres = Model_Offre.objects.all().order_by('-id')
        today = datetime.datetime.today()
        context = {
            'title' : 'Listes Offres',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': offres
        }
        template = loader.get_template("Soluplus/App_Recutement/Recrutement_Admin/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Listes offre Admin")
        print(e)

@never_cache
def get_add_offres_admin(request):
    try:
        droit = "CREER_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        context = {
            'title' : 'Création de l\'Offre',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu, # 29,
        }
        template = loader.get_template("Soluplus/App_Recutement/Recrutement_Admin/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Ajout Offre")
        print(e)

@transaction.atomic
def post_add_offre_admin(request):
    sid = transaction.savepoint()
    try:
        droit = "CREER_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        auteur = auth.getEmploye(request)
        titre = request.POST['titre']
        status = int(request.POST['status'])
        datepublish = request.POST['datepublish']
        localisation = request.POST['localisation']
        dateclose = request.POST['dateclose']
        typecontrat = request.POST['typecontrat']
        entreprise = request.POST['entreprise']
        proccess = request.POST['proccess']
        responsable = request.POST['responsable']
        description = request.POST['description']
        tache = request.POST['tache']
        qualification = request.POST['qualification']

        datepublish = timezone.datetime(int(datepublish[6:10]), int(datepublish[3:5]), int(datepublish[0:2]))
        dateclose = timezone.datetime(int(dateclose[6:10]), int(dateclose[3:5]), int(dateclose[0:2]))

        today = date.today()

        offre = Model_Offre()
        offre.reference = toGenerateNumeroOffre()
        offre.titre = titre
        offre.status = status
        offre.datepublish = datepublish
        offre.localisation = localisation
        offre.typecontrat = typecontrat
        offre.entreprise = entreprise
        offre.responsable = responsable
        offre.description = description
        offre.tache = tache
        offre.dateclose = dateclose
        offre.qualification = qualification
        offre.proccess = proccess
        offre.est_actif = True
        offre.auteur_id = auteur.id
        offre.save()

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("app_recrutement_list_offre_admin"))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("ERREUR")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de création Offre")
        return HttpResponseRedirect(reverse("app_recrutement_add_offre_admin"))

def get_detail_offre_admin(request, ref):
    try:
        droit = "VOIR_LIST_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        offres = Model_Offre.objects.get(pk=ref)

        context = {
            'title' :'Offre'+' '+offres.reference,
            'model' : offres,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }

        template = loader.get_template("Soluplus/App_Recutement/Recrutement_Admin/detail.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Detail Offre")
        print(e)
        return HttpResponseRedirect(reverse("app_recrutement_list_offre_admin"))

def get_update_offres_admin(request, ref):
    try:
        droit = "MODIFIER_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        offre = Model_Offre.objects.get(pk=ref)
        print('***Offre', offre)

        context = {
            'title' : 'Modifier de l\'Offre',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': offre,
        }
        template = loader.get_template("Soluplus/App_Recutement/Recrutement_Admin/update.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Modifier Offre")
        print(e)

@transaction.atomic
def post_update_offre_admin(request):
    sid = transaction.savepoint()
    try:
        droit = "MODIFIER_OFFRE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        auteur = auth.getEmploye(request)
        ident = int(request.POST['ident'])
        reference = request.POST['ref']
        titre = request.POST['titre']
        status = int(request.POST['status'])
        datepublish = request.POST['datepublish']
        localisation = request.POST['localisation']
        dateclose = request.POST['dateclose']
        typecontrat = request.POST['typecontrat']
        entreprise = request.POST['entreprise']
        proccess = request.POST['proccess']
        responsable = request.POST['responsable']
        description = request.POST['description']
        tache = request.POST['tache']
        qualification = request.POST['qualification']
        actif = int(request.POST['actif'])

        datepublish = timezone.datetime(int(datepublish[6:10]), int(datepublish[3:5]), int(datepublish[0:2]))
        dateclose = timezone.datetime(int(dateclose[6:10]), int(dateclose[3:5]), int(dateclose[0:2]))

        if actif == 1:is_actif = True
        else: is_actif = False


        today = date.today()

        offre = Model_Offre.objects.get(pk=ident)
        offre.titre = titre
        offre.status = status
        offre.datepublish = datepublish
        offre.localisation = localisation
        offre.typecontrat = typecontrat
        offre.entreprise = entreprise
        offre.responsable = responsable
        offre.description = description
        offre.tache = tache
        offre.dateclose = dateclose
        offre.qualification = qualification
        offre.proccess = proccess
        offre.est_actif = is_actif
        offre.auteur_id = auteur.id
        offre.save()

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("app_recrutement_list_offre_admin"))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("ERREUR")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de création Offre")
        return HttpResponseRedirect(reverse("app_recrutement_update_offre_admin",args=(ident,)))


#LIST OF CANDIDAT
def get_list_of_candidat_admin(request):
    try:
        droit = "VOIR_LIST_CANDIDAT_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        candidats = Model_Candidat.objects.all().order_by('-id')
        
        context = {
            'title' : 'Listes Candidats',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': candidats
        }
        template = loader.get_template("Soluplus/App_Recutement/Candidat_Admin/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Listes Candidat Admin")
        print(e)

def get_detail_of_candidat_admin(request, ref):
    try:
        droit = "VOIR_LIST_CANDIDAT_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)

        if reponse != None:
            return reponse


        candidat = Model_Candidat.objects.get(pk=ref)
        type=list(Typestatusdossier)
        dossiers_type=[list(i) for i in type]
        print(dossiers_type)
        context = {
            'title' : 'Candidat'+''+candidat.reference,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': candidat,
            'type':dossiers_type
        }
        template = loader.get_template("Soluplus/App_Recutement/Candidat_Admin/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Listes Candidat Admin")
        print(e)


#LIST DE CANDIDATURE
def get_list_of_candidature_admin(request):
    try:
        droit = "VOIR_LIST_CANDIDATURE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        offres = Model_Offre.objects.all().order_by('-id')
        candidatures=Model_Candidature.objects.filter(id=ref)
        # for item in candidatures:
        #     for el in item.diplome.all():
        #         print(el.file.name)
            # print(item.diplome)
        context = {
            'title' : 'Listes Candidatures',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': offres
        }
        template = loader.get_template("Soluplus/App_Recutement/Dossier_Candidature/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Listes Candidature Admin")
        print(e)
        return HttpResponseRedirect(reverse("app_tableau_recrutement"))

def get_detail_of_candidature_admin(request, ref:int):
    try:
        droit = "VOIR_LIST_CANDIDATURE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        candidatures = Model_Candidature.objects.filter(candidat_id=ref)
        totalCandidature = len(candidatures)
        totalcandidatvalide = Model_Candidature.objects.filter(offre_id=ref, status = 2).count()
        print(f"total {totalcandidatvalide}")
        totalcandidatdecline = Model_Candidature.objects.filter(offre_id=ref, status = 3).count()
        totalcandidatwaiting = Model_Candidature.objects.filter(offre_id=ref, status = 1).count()
        statistique = {
            'totalCandidature':totalCandidature,
            'totalcandidatvalide':totalcandidatvalide,
            'totalcandidatdecline':totalcandidatdecline,
            'totalcandidatwaiting': totalcandidatwaiting
        }
        offre = Model_Offre.objects.filter(id=ref)
        print(f"candidatures {candidatures}")
        context = {
            'title' : 'Détail Candidature',
            'modules' : modules,
            'module' : module,  
            'menus' : menus,
            'menu' : menu,
            'model': candidatures,
            'offre':offre,
            'statistique': statistique
        }
        template = loader.get_template("Soluplus/App_Recutement/Candidat_Admin/singleCandidature.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Detail Candidature Admin")
        print(e)
        print(f"ref {ref}")
        return HttpResponseRedirect(reverse("app_recrutement_list_candidatures"))


def get_traitement_candidature_admin(request, ref):
    try:
        droit = "VOIR_LIST_CANDIDATURE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        candidature = Model_Candidature.objects.get(pk=ref)
        email = candidature.candidat.email

        context = {
            'title' : 'Détail Candidature',
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model': candidature,
            'destinationemail':email,
        }
        template = loader.get_template("Soluplus/App_Recutement/Dossier_Candidature/traitement.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Traitement Candidature Admin")
        print(e)
        return HttpResponseRedirect(reverse("app_recrutement_list_candidatures"))

def get_json_get_statut_change(request):
    try:
        id = int(request.POST["ref_valide"])
        statut = int(request.POST["statut_val"])

        module = Model_Candidature.objects.get(pk=id)
        module.status = statut
        module.save()

        ref = module.offre.id

        return HttpResponseRedirect(reverse("app_recrutement_detail_candidature" ,args=(ref,)))
    except Exception as e:
        print("ERREUR")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de traitement")
        return HttpResponseRedirect(reverse("app_recrutement_get_traitement_candidature",args=(id,)))

def traitement_decline_offre(request):
    try:
        print('****DECLINE FONCTION******')
        id = int(request.POST["ref_decline"])
        print('****ID', id)
        statut = int(request.POST["statut_decline"])

        module = Model_Candidature.objects.get(pk=id)
        module.status = statut
        module.save()
        ref = module.offre.id

        return HttpResponseRedirect(reverse("app_recrutement_detail_candidature" ,args=(ref,)))
    except Exception as e:
        print("*****************ERREUR DECLINE FONCTION**********")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de traitement")
        return HttpResponseRedirect(reverse("app_recrutement_get_traitement_candidature",args=(id,)))


def get_json_cloturer_dossier(request):
    try:
        id = int(request.GET["ref"])
        print("***IDENTIFIANT", id)
        dossier = Model_Offre.objects.get(pk=id)
        dossier.est_actif = False
        dossier.status = 2
        dossier.save()

        data = {
			"message" : "Success!",
		}
        return JsonResponse(data, safe=False)
    except Exception as e:
        print('ERREUR GETTING DATA JSON')
        print(e)
        return JsonResponse([], safe=False)

#PRINTING RAPPORTING DOSSIER
def printing_dossier_candidature(request, ref):
    try:
        droit = "PRINTING_CANDIDATURE_ADMIN"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        model_accept = Model_Candidature.objects.filter(offre_id=ref, status = 2)
        model_decline = Model_Candidature.objects.filter(offre_id=ref, status = 3)
        model_waiting = Model_Candidature.objects.filter(offre_id=ref, status = 1)
        print('******ALL QUERY SET IS OK*****')

        context = {
            'title' : 'Dossier',
            'model_accept' : model_accept,
            'model_decline' : model_decline,
            'model_waiting' : model_waiting,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Recutement/Dossier_Candidature/rapport.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Rapport Dossier")
        print(e)
        return HttpResponseRedirect(reverse("app_recrutement_list_candidatures"))

def toGenerateNumeroOffre():
    total_Offre = Model_Offre.objects.all().count()
    total_Offre = total_Offre + 1
    temp_numero = str(total_Offre)

    for i in range(len(str(total_Offre)), 4):
        temp_numero = "0" + temp_numero

    mois = timezone.now().month
    if mois < 10: mois = "0%s" % mois

    temp_numero = "OFFRE-%s%s%s" % (timezone.now().year, mois, temp_numero)
    return temp_numero

def toGenerateNumeroCandit():
    totalCand = Model_Candidat.objects.all().count()
    totalCand = totalCand + 1
    temp_numero = str(totalCand)

    for i in range(len(str(totalCand)), 4):
        temp_numero = "0" + temp_numero

    mois = timezone.now().month
    if mois < 10: mois = "0%s" % mois

    temp_numero = "CAD-%s%s%s" % (timezone.now().year, mois, temp_numero)
    return temp_numero