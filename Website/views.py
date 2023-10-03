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

from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger

from random import randint
from django.core.mail import send_mail
from django.conf import settings
from django.db.models import Q, Sum, Min, Count

from _datetime import date
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

from MainApp.models import *

from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse


from django.db.models.functions import (TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth)

import random
import string
import time


from django.shortcuts import get_object_or_404
from weasyprint import HTML, CSS

from MainApp.Utils.report_css import report_css
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache

from App_Recutement.models import *

#WEBSITE

@never_cache
def get_site_index(request):
    context = {
        'title' : 'Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/index.html")
    return HttpResponse(template.render(context, request))

@never_cache
def get_site_about(request):
    context = {
        'title' : 'À propos de nous - Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/about.html")
    return HttpResponse(template.render(context, request))

@never_cache
def get_site_valeur(request):
    context = {
        'title' : 'Nos Valeurs - Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/valeur.html")
    return HttpResponse(template.render(context, request))

@never_cache
def get_site_mission(request):
    context = {
        'title' : 'Notre mission - Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/mission.html")
    return HttpResponse(template.render(context, request))

@never_cache
def get_site_contact(request):
    context = {
        'title' : 'Contact - Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/contact.html")
    return HttpResponse(template.render(context, request))

@never_cache
def get_site_conversation(request):
    context = {
        'title' : 'Conversation - Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/conversation.html")
    return HttpResponse(template.render(context, request))


def get_site_recrutement(request):
    try:
        context = {
            'title' : 'Recrutement - Hodari : Services RH et Juridique',
            
        }
        template = loader.get_template("Soluplus/Website/Recrutement/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Liste des offres")
        print(e)
        

#DEPOT CV
def get_page_depot_apply(request):
    try:
        offres = Model_Offre.objects.filter(est_actif = 1).order_by('-id')
        
        context = {
            'title' : 'Hodari : Deposer votre CV',
            'domaines' : Model_Domaine_Recrutement.objects.all().order_by('designation'),
            'recente' : offres[:3]
        }
        
        template = loader.get_template("Soluplus/Website/Depot_CV/apply.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Postuler d'offre")
        print(e)

#   POST POSTULER FORM
@transaction.atomic
def post_apply_depot(request):
    sid = transaction.savepoint()
    try:
        
        nom = request.POST['nom']
        postnom = request.POST['postnom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        tel = "243" + request.POST['tel']
        cv = request.FILES['fileUpload']
        profession_id = request.POST['profession_id']
        
        today = date.today()
        CandidatID = None
        
        

        Candidat = Model_Candidat.objects.filter(phone = tel).first()
        if Candidat != None:
            CandidatID = Candidat.id
        else:
            Candidat = Model_Candidat()
            Candidat.reference = toGenerateNumeroCandit()
            Candidat.nom = nom
            Candidat.postnom = postnom
            Candidat.prenom = prenom
            
            Candidat.image = ''
            Candidat.email = email
            Candidat.phone = tel
            Candidat.est_actif  = True
            Candidat.date_creation = today
            Candidat.profession_id = profession_id
            Candidat.auteur_id = None
            Candidat.save()

            CandidatID = Candidat.id

        #SAVE MULTIPLE DIPLOME
        List_D_Id = []
        list_diplome = request.FILES.getlist('diplome', None)
        for i in range(0, len(list_diplome)):
            fileupload = list_diplome[i]

            diplome = DiplomaFile()
            diplome.file = fileupload
            diplome.save()

            List_D_Id.append(diplome.id)
        print("CV VV   %s" % cv)
        Candidature = Model_Candidature()
        Candidature.reference = toGenerateNumeroCandit()
        Candidature.path_cv2 = cv
        Candidature.candidat_id = CandidatID
        Candidature.status = 4
        Candidature.est_depot_cv = True
        Candidature.save()

        for i in range(0, len(List_D_Id)):
            diplomeid = List_D_Id[i]
            Candidature.diplome.add(diplomeid)
        Candidature.save()

        candidat_id = int(Candidature.id)
        # print('***candidat save', candidat_id)
        


        #CONFIRMATION MAIL
        texte = "<h1>Cher " + str(Candidature.candidat.prenom)+" "+ Candidature.candidat.nom +",<br></h1><p>Nous vous remercions pour l'intérêt que vous portez à notre entreprise et de l'initiative que vous avez prise de deposer votre CV.</p><p>Vos documents sont bien arrivés chez nous et nous les examinerons dès que possible.</p><p>Lorsque nous aurons évalué votre profil et que nous souhaiterons vous considérer pour l'étape suivante de notre processus de sélection, vous serez invité à un entretien.</p><p>Nous serons heureux de répondre à toutes les questions que vous pourriez avoir, que ce soit sur le poste vacant ou sur notre processus de recrutement. Veuillez contacter en cliquant ici <a href='https://hodari.cd/contact'>Hodari</a>, soit en envoyant un courriel à contact@hodari.cd, soit en appelant +243 800 000 000.</p>"
        
        url = ''
        recipient_list = email
        send_async_mail('Hodari - CV deposé','Mail',texte,url,recipient_list,False)
        # print('****CANDIDATURE END****')

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("website_get_confirmation_cv", args=(candidat_id,)))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("ERREUR POST OFFRE")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de création Offre")
        return HttpResponseRedirect(reverse("website_apply_depot"))


def ajax_get_poste_recrutement(request):
        try:
            data = []

            domaine_id = request.GET["domaine_id"]
            print("COMMMMMMMMMMMMMMMMMMMMMMM %s" % domaine_id)

            domaine = Model_Domaine_Recrutement.objects.get(pk=domaine_id)
            postes = Model_Poste_Recrutement.objects.filter(domaine_id = domaine_id).order_by('designation')

            for item in postes:
                item = {
                    'id' : item.id,
                    'designation' : item.designation,
                }
                data.append(item)

            return JsonResponse(data, safe=False)
        except Exception as e:
            print('ERREUR LOAD NOTIFICATION')
            print(e)
            return JsonResponse([], safe=False)


def get_page_offre_apply(request, ref):
    try:
        offre = Model_Offre.objects.get(pk=ref)
        offres = Model_Offre.objects.filter(est_actif = 1).order_by('-id')

        #Statistique
        kinshasa = Model_Offre.objects.filter(localisation__contains='kinshasa').count()
        lubumbashi = Model_Offre.objects.filter(localisation__contains='lubumbashi').count()
        goma = Model_Offre.objects.filter(localisation__contains='goma').count()
        matadi = Model_Offre.objects.filter(localisation__contains='matadi').count()
        kisangani = Model_Offre.objects.filter(localisation__contains='kisangani').count()
        lualaba = Model_Offre.objects.filter(localisation__contains='lualaba').count()
        bukavu = Model_Offre.objects.filter(localisation__contains='bukavu').count()
        domaine =  Model_Domaine_Recrutement.objects.all().order_by('designation')
        
        print("OFFFFFFF %s" % domaine)

        ville ={
            'kin':kinshasa,
            'lushi':lubumbashi,
            'goma':goma,
            'matadi':matadi,
            'kisang':kisangani,
            'lualaba':lualaba,
            'bukavu':bukavu,
        }

        context = {
            'title' : 'Postuler à l\'Offre d\'emploi',
            'model':offre,
            'recente':offres[:3],
            'ville': ville,
            'domaines_activite' : domaine,
        }
        template = loader.get_template("Soluplus/Website/Recrutement/apply.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Postuler d'offre")
        print(e)
        

def get_confirmation_depot_cv(request,ref):
    try:
        candidature = Model_Candidature.objects.get(pk = ref)
           
        context = {
            'title' : 'CV deposé',
            'model' : candidature
        }
        template = loader.get_template("Soluplus/Website/Depot_CV/confirmation.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Confirmation")
        print(e)
        

def get_page_offre_view(request):
    try:
        # today = date.today()
        # , dateclose__gt=today  Check if date is more than date now
        offres = Model_Offre.objects.filter(est_actif = 1).order_by('-id')

        #Statistique
        kinshasa = Model_Offre.objects.filter(localisation__contains='kinshasa').count()
        lubumbashi = Model_Offre.objects.filter(localisation__contains='lubumbashi').count()
        goma = Model_Offre.objects.filter(localisation__contains='goma').count()
        matadi = Model_Offre.objects.filter(localisation__contains='matadi').count()
        kisangani = Model_Offre.objects.filter(localisation__contains='kisangani').count()
        lualaba = Model_Offre.objects.filter(localisation__contains='lualaba').count()
        bukavu = Model_Offre.objects.filter(localisation__contains='bukavu').count()

        ville ={
            'kin':kinshasa,
            'lushi':lubumbashi,
            'goma':goma,
            'matadi':matadi,
            'kisang':kisangani,
            'lualaba':lualaba,
            'bukavu':bukavu,
        }

        page = request.GET.get('page', 1)
        paginator = Paginator(offres, 4)

        try:
            LesOffres = paginator.page(page)
        except PageNotAnInteger:
            LesOffres = paginator.page(1)
        except EmptyPage:
            LesOffres = paginator.page(paginator.num_pages)
        context = {
            'title' : 'Offres d\'emploi',
            'model':LesOffres,
            'recente':offres[:3],
            'entete': 'DERNIÈRES OFFRES D\'EMPLOI',
            'ville': ville,
        }
        template = loader.get_template("Soluplus/Website/Recrutement/offre.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Liste des offres")
        print(e)

@transaction.atomic
def post_search_offre_view(request):
    sid = transaction.savepoint()
    try:
        search_key = request.POST['search_key']
        region = request.POST['region']
        metier = request.POST['metier']

        recente = Model_Offre.objects.filter(est_actif = 1).order_by('-id')

        offres = Model_Offre.objects.filter(
            Q(titre__contains= search_key ) | Q(localisation__contains=region)
            ).order_by('-id')
        page = request.GET.get('page', 1)
        paginator = Paginator(offres, 4)

        #Statistique
        kinshasa = Model_Offre.objects.filter(localisation__contains='kinshasa').count()
        lubumbashi = Model_Offre.objects.filter(localisation__contains='lubumbashi').count()
        goma = Model_Offre.objects.filter(localisation__contains='goma').count()
        matadi = Model_Offre.objects.filter(localisation__contains='matadi').count()
        kisangani = Model_Offre.objects.filter(localisation__contains='kisangani').count()
        lualaba = Model_Offre.objects.filter(localisation__contains='lualaba').count()
        bukavu = Model_Offre.objects.filter(localisation__contains='bukavu').count()

        ville ={
            'kin':kinshasa,
            'lushi':lubumbashi,
            'goma':goma,
            'matadi':matadi,
            'kisang':kisangani,
            'lualaba':lualaba,
            'bukavu':bukavu,
        }

        try:
            LesOffres = paginator.page(page)
        except PageNotAnInteger:
            LesOffres = paginator.page(1)
        except EmptyPage:
            LesOffres = paginator.page(paginator.num_pages)

        context = {
            'title' : 'Liste Offre d\'emploi',
            'model':LesOffres,
            'recente':recente[:3],
            'entete': 'L\'OFFREE TROUVEE',
            'ville':ville
        }
        transaction.savepoint_commit(sid)
        template = loader.get_template("Soluplus/Website/Recrutement/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("Erreur Liste des offres SEARCHING")
        print(e)



def get_page_offre_item(request, ref):
    try:
        offre = Model_Offre.objects.get(pk=ref)
        offres = Model_Offre.objects.filter(est_actif = 1).order_by('-id')

        #Statistique
        kinshasa = Model_Offre.objects.filter(localisation__contains='kinshasa').count()
        lubumbashi = Model_Offre.objects.filter(localisation__contains='lubumbashi').count()
        goma = Model_Offre.objects.filter(localisation__contains='goma').count()
        matadi = Model_Offre.objects.filter(localisation__contains='matadi').count()
        kisangani = Model_Offre.objects.filter(localisation__contains='kisangani').count()
        lualaba = Model_Offre.objects.filter(localisation__contains='lualaba').count()
        bukavu = Model_Offre.objects.filter(localisation__contains='bukavu').count()
        

        ville ={
            'kin':kinshasa,
            'lushi':lubumbashi,
            'goma':goma,
            'matadi':matadi,
            'kisang':kisangani,
            'lualaba':lualaba,
            'bukavu':bukavu,
        }

        context = {
            'title' : 'Détail Offre d\'emploi',
            'model':offre,
            'recente':offres[:3],
            'ville':ville
        }
        template = loader.get_template("Soluplus/Website/Recrutement/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Detail d'offre")
        print(e)



#   POST POSTULER FORM
@transaction.atomic
def post_apply_offre(request):
    sid = transaction.savepoint()
    try:
        # print("**************BEGIN POSTULATION****************")
        idoffre = int(request.POST['idoffre'])
        # auteur = auth.getEmploye(request)
        # print('L\'id de offre est', idoffre)
        # print('Test before get Tel')
        nom = request.POST['nom']
        postnom = request.POST['postnom']
        prenom = request.POST['prenom']
        email = request.POST['email']
        tel = "243" + request.POST['tel']
        
        cv = request.FILES['fileUpload']
        # print('getting file 1')
        motivation = request.FILES['fileUpload2']
        # print('getting file 2')

        # print('**FILE UPLAOD**', cv)
        # print('**FILE UPLAOD**', motivation)

        today = date.today()
        candidatID = 0
        
        Candidat = Model_Candidat.objects.filter(phone = tel).first()
        if Candidat != None:
            candidatID = Candidat.id
        else:
            Candidat = Model_Candidat()
            Candidat.reference = toGenerateNumeroCandit()
            Candidat.nom = nom
            Candidat.postnom = postnom
            Candidat.prenom = prenom
            Candidat.image = ''
            Candidat.email = email
            Candidat.phone = tel
            Candidat.est_actif  = True
            Candidat.date_creation = today
            Candidat.auteur_id = None
            Candidat.save()

            candidatID = Candidat.id

        #SAVE MULTIPLE DIPLOME
        List_D_Id = []
        list_diplome = request.FILES.getlist('diplome', None)
        for i in range(0, len(list_diplome)):
            fileupload = list_diplome[i]

            diplome = DiplomaFile()
            diplome.file = fileupload
            diplome.save()

            List_D_Id.append(diplome.id)

        Candidature = Model_Candidature()
        Candidature.reference = toGenerateNumeroCandit()
        Candidature.cv = cv
        Candidature.motivation = motivation
        Candidature.offre_id = idoffre
        Candidature.candidat_id = candidatID
        Candidature.status = 1
        Candidature.save()

        for i in range(0, len(List_D_Id)):
            diplomeid = List_D_Id[i]
            Candidature.diplome.add(diplomeid)
        Candidature.save()

        candidat_id = int(Candidature.id)
        # print('***candidat save', candidat_id)

        #CONFIRMATION MAIL
        texte = 'Cher Monsieur Untel, Nous vous remercions de l\'intérêt que vous portez à notre entreprise et de l\'initiative que vous avez prise de postuler pour le poste'
        url = ''
        recipient_list = email
        send_async_mail('Confirmation Application !','Mail',texte,url,recipient_list,False)
        # print('****CANDIDATURE END****')

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("website_get_confirmation", args=(candidat_id,)))
    except Exception as e:
        transaction.savepoint_rollback(sid)
        print("ERREUR DEPOT CV")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de depot de CV")
        return HttpResponseRedirect(reverse("website_apply_offre", args=(idoffre,)))

def get_confirmation(request,ref):
    try:
        candidature = Model_Candidature.objects.get(pk = ref)

        context = {
            'title' : 'Confirmation',
            'model' : candidature
        }
        template = loader.get_template("Soluplus/Website/Recrutement/confirme.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Confirmation")
        print(e)
        

        
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