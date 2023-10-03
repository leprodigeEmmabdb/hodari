## -*- coding: utf-8 -*-

from App_Configuration.models import Model_Employe, Model_Personne

from App_Courrier.models import Model_Courrier, Model_Destinataire_Courrier, Model_Document_Courrier, Model_Exped_Destinataire, Model_Nature_Courrier

import os
from django.db.models.aggregates import Avg
from django.db.models.base import Model

from django.db.models import Q, Sum, Min, Count

from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User, Group
from django.db import transaction
from django.template import loader
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
from django.db.models.functions import (TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth, text)
from django.db.models.functions import Lower
from MainApp.Utils.EmailThread import send_async_mail, send_whatsapp
import datetime
import json
import array
from django.db import transaction
from django.db.models import Sum
import time
import datetime

from datetime import*
import calendar
#from dateutil.relativedelta import*

from os import listdir, pardir
from os.path import isfile, join

from MainApp.Utils.auth import auth
from MainApp.Utils.utils import utils

from django.contrib.staticfiles.templatetags.staticfiles import static


def get_home(request):
    
    droit = "VOIR_TABLEAU_DE_BORD_COURRIER"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
    if reponse != None:
        return reponse


    context = {
        'title' : 'Tableau de Bord',
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/index.html")
    return HttpResponse(template.render(context, request))

# Exp/Destinataires

def get_lister_exped(request):
    droit = "VOIR_EXPEDITEUR"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    exp = Model_Exped_Destinataire.objects.all()
    context = {
        'title' : 'Liste des Expéditeurs',
        'model' : exp,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/expediteur/list.html")
    return HttpResponse(template.render(context, request))


def get_creer_exped(request):

    droit = "CREER_EXPEDITEUR"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse

    context = {
        'title' : "Expéditeur",
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/expediteur/add.html")
    return HttpResponse(template.render(context, request))

def post_creer_exped(request):
    try:
        auteur = auth.getEmploye(request)
        nom = request.POST["nom"]
        email = request.POST["email"]
        phone = request.POST["phone"]
        adresse = request.POST["adresse"]
        
        print('SAVE BEGIN')

        client = Model_Exped_Destinataire()
        client.nom = nom
        client.nom_complet = nom 
        client.adresse = adresse
        client.email = email
        client.phone = phone
        client.save()

        print("SAVE OKKKK")

        return HttpResponseRedirect(reverse('app_courrier_details_exped', args=(client.id,)))        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_courrier_add_exped'))



def get_details_exped(request, ref):

    try:
        droit = "VOIR_EXPEDITEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse 

        ref = int(ref)
        expediteur = Model_Exped_Destinataire.objects.get(pk = ref)

        context = {
            'title' : str(expediteur.nom),
            'model' : expediteur,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Courrier/expediteur/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("ERREUR DETAIL")
        print(e)
        return HttpResponseRedirect(reverse('app_courrier_list_exped'))



# COURRIER ARRIVEE

def get_lister_date_arrivee(request):
    droit = "VOIR_COURRIER_ARRIVEE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    courrier = Model_Courrier.objects.filter(type_id = 1).annotate(date_reception_date=TruncDay('date_reception')).values('date_reception_date').annotate(id=Min('id')).order_by('-id')     

    data = []
    
    for i in courrier: 
        item = {
            'date_reception' : i['date_reception_date']
        }
        data.append(item)

    context = {
        'title' : 'Liste des Courriers arrivés',
        'model' : data,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/arrivee/list_date_jour.html")
    return HttpResponse(template.render(context, request))


def get_lister_arrivee(request):
    droit = "VOIR_COURRIER_ARRIVEE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    date_reception = request.POST['date_reception']

    day = date_reception[0:2]
    month = date_reception[3:5]
    year = date_reception[6:10]
    
    today = month + '-' + day + '-' + year
    today = datetime.strptime(today, '%m-%d-%Y')

    courrier = Model_Courrier.objects.filter(type_id = 1, date_reception__date = today).order_by('id')

    context = {
        'title' : 'Liste des Courriers arrivés',
        'model' : courrier,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/arrivee/list.html")
    return HttpResponse(template.render(context, request))


def get_creer_arrivee(request):

    droit = "CREER_COURRIER_ARRIVEE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse

    natures = Model_Nature_Courrier.objects.all()
    expediteurs = Model_Personne.objects.all()
    employes = Model_Employe.objects.all()

    context = {
        'title' : "Création courrier arrivé",
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
        'natures' : natures,
        'expediteurs' : expediteurs,
        'employes' : employes,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/arrivee/add.html")
    return HttpResponse(template.render(context, request))

def post_creer_arrivee(request):
    try:

        droit = "CREER_COURRIER_ARRIVEE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        auteur = auth.getEmploye(request)
        nature_id = request.POST["nature_id"]
        numero = request.POST["numero"]
        date_envoi = request.POST["date_envoi"]
        date_envoi = utils.toDate(date_envoi)

        expediteur_id = request.POST["expediteur_id"]

        objet = request.POST["objet"]
        date_reception = request.POST["date_reception"]
        date_reception = utils.toDate(date_reception)
        date_reponse = request.POST["date_reponse"]
        date_reponse = utils.toDate(date_reponse)
        
        remarques = request.POST["remarques"]
        
        list_destinataire_id = request.POST.getlist("destinataire_id",None) 
        list_action = request.POST.getlist("action", None)

        try:
            nature = Model_Nature_Courrier.objects.filter(pk=nature_id).first()
        except Exception as e:
            nature = Model_Nature_Courrier()
            nature.designation = nature_id
            nature.save()
            nature_id = nature.id

        try:
            expediteur = Model_Personne.objects.filter(pk=expediteur_id).first()
        except Exception as e:
            expediteur = Model_Exped_Destinataire()
            expediteur.nom_complet = expediteur_id
            expediteur.nom = expediteur_id
            expediteur.save()
            expediteur_id = expediteur.id
        
        courrier = Model_Courrier()
        courrier.type_id = 1
        courrier.numero = numero
        courrier.nature_id = nature_id
        courrier.date_envoi = date_envoi
        courrier.expediteur_id = expediteur_id
        courrier.objet = objet
        courrier.date_reception = date_reception
        courrier.date_reponse = date_reponse
        courrier.remarque = remarques
        courrier.numero_enregistrement = utils.toGenerateNumero("CA-")
        courrier.save()
        
        recipient_list = []
        
        for i in range(0, len(list_destinataire_id)):
            destinataire_id = int(list_destinataire_id[i])
            action = list_action[i]
            
            pers = Model_Personne.objects.get(pk = destinataire_id)
            recipient_list.append(pers.email)

            dest = Model_Destinataire_Courrier()
            dest.courrier_id = courrier.id
            dest.destinataire_id = destinataire_id
            dest.action = action
            dest.save()

        
        
        if request.FILES:
            for fichier in request.FILES.getlist('fichiers'):
                base_dir = settings.BASE_DIR
                media_dir = settings.MEDIA_ROOT
                media_url = settings.MEDIA_URL

                nom_fichier = fichier.name
                print(nom_fichier)
        
                file = fichier
                docs_dir = 'courrier/arrivee/' + courrier.numero_enregistrement + '/'
                media_dir = media_dir + '/' + docs_dir
                save_path = os.path.join(media_dir, str(nom_fichier))
                path = default_storage.save(save_path, file)
                url = media_url + docs_dir + str(nom_fichier)

                document = Model_Document_Courrier()
                document.courrier_id = courrier.id
                document.url_document = url
                document.description = nom_fichier
                document.save()

        # SEND MAIL
        texte = 'Vous avez reçu un nouveau courrier qui a comme objet ' + objet + ' venant de ' + expediteur.nom_complet
        url = ''
        send_async_mail('Nouveau courrier arrivé','Mail',texte,url,recipient_list,False)     

        return HttpResponseRedirect(reverse('app_courrier_details_arrivee', args=(courrier.id,)))        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_courrier_add_exped'))


def get_details_arrivee(request, ref):

    try:
        droit = "VOIR_COURRIER_ARRIVEE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse 

        ref = int(ref)
        model = Model_Courrier.objects.get(pk = ref)
        
        context = {
            'title' : str(model.numero),
            'model' : model,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }

        template = loader.get_template("Soluplus/App_Courrier/courrier/arrivee/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("ERREUR DETAIL")
        print(e)
        return HttpResponseRedirect(reverse('app_courrier_list_exped'))


def get_traiter_arrivee(request,ref):
    droit = "TRAITER_COURRIER_ARRIVEE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    courrier = Model_Courrier.objects.get(pk = ref)

    context = {
        'title' : 'Traiter courrier arrivé',
        'model' : courrier,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/arrivee/traiter.html")
    return HttpResponse(template.render(context, request))


def post_traiter_arrivee(request):
    try:

        droit = "CREER_COURRIER_ARRIVEE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        ref = request.POST["ref"]
        date_traitement = request.POST["date_traitement"]
        date_traitement = utils.toDate(date_traitement)
        
        courrier = Model_Courrier.objects.get(pk = ref)
        courrier.est_traite = True
        courrier.date_traitement = date_traitement
        courrier.save()
        
        return HttpResponseRedirect(reverse('app_courrier_details_arrivee', args=(ref)))        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_courrier_arrivee_traiter'))


# COURRIER DEPART

def get_lister_date_depart(request):
    droit = "VOIR_COURRIER_DEPART"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    courrier = Model_Courrier.objects.filter(type_id = 2).annotate(date_reception_date=TruncDay('date_envoi')).values('date_envoi__date').annotate(id=Min('id')).order_by('-id')     

    data = []
    
    for i in courrier: 
        item = {
            'date_envoi' : i['date_envoi__date']
        }
        data.append(item)

    context = {
        'title' : 'Liste des Courriers départs',
        'model' : data,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/depart/list_date_jour.html")
    return HttpResponse(template.render(context, request))


def get_lister_depart(request):
    droit = "VOIR_COURRIER_DEPART"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    date_envoi = request.POST['date_envoi']

    day = date_envoi[0:2]
    month = date_envoi[3:5]
    year = date_envoi[6:10]
    
    today = month + '-' + day + '-' + year
    today = datetime.strptime(today, '%m-%d-%Y')

    courrier = Model_Courrier.objects.filter(type_id = 2, date_envoi__date = today).order_by('id')

    context = {
        'title' : 'Liste des Courriers départs',
        'model' : courrier,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/depart/list.html")
    return HttpResponse(template.render(context, request))


def get_creer_depart(request):

    droit = "CREER_COURRIER_DEPART"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse

    natures = Model_Nature_Courrier.objects.all()
    expediteurs = Model_Personne.objects.all()
    employes = Model_Employe.objects.all()


    context = {
        'title' : "Création courrier départ",
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
        'natures' : natures,
        'expediteurs' : expediteurs,
        'employes' : employes,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/depart/add.html")
    return HttpResponse(template.render(context, request))

def post_creer_depart(request):
    try:

        droit = "CREER_COURRIER_DEPART"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        auteur = auth.getEmploye(request)
        nature_id = request.POST["nature_id"]
        
        date_envoi = request.POST["date_envoi"]
        date_envoi = utils.toDate(date_envoi)

        expediteur_id = request.POST["expediteur_id"]

        objet = request.POST["objet"]
        
        remarques = request.POST["remarques"]
        
        list_destinataire_id = request.POST.getlist("destinataire_id",None) 
        list_action = request.POST.getlist("action", None)

        try:
            nature = Model_Nature_Courrier.objects.filter(pk=nature_id).first()
        except Exception as e:
            nature = Model_Nature_Courrier()
            nature.designation = nature_id
            nature.save()
            nature_id = nature.id

        try:
            expediteur = Model_Personne.objects.filter(pk=expediteur_id).first()
        except Exception as e:
            expediteur = Model_Exped_Destinataire()
            expediteur.nom_complet = expediteur_id
            expediteur.nom = expediteur_id
            expediteur.save()
            expediteur_id = expediteur.id
        
        courrier = Model_Courrier()
        courrier.type_id = 2
        courrier.nature_id = nature_id
        courrier.date_envoi = date_envoi
        courrier.expediteur_id = expediteur_id
        courrier.objet = objet
        courrier.remarque = remarques
        courrier.numero_enregistrement = utils.toGenerateNumero("CD-")
        courrier.save()
        

        for i in range(0, len(list_destinataire_id)):
            destinataire_id = int(list_destinataire_id[i])

            dest = Model_Destinataire_Courrier()
            dest.courrier_id = courrier.id
            dest.destinataire_id = destinataire_id            
            dest.save()


        if request.FILES:
            for fichier in request.FILES.getlist('fichiers'):
                base_dir = settings.BASE_DIR
                media_dir = settings.MEDIA_ROOT
                media_url = settings.MEDIA_URL

                nom_fichier = fichier.name
                print(nom_fichier)
        
                file = fichier
                docs_dir = 'courrier/depart/' + courrier.numero_enregistrement + '/'
                media_dir = media_dir + '/' + docs_dir
                save_path = os.path.join(media_dir, str(nom_fichier))
                path = default_storage.save(save_path, file)
                url = media_url + docs_dir + str(nom_fichier)

                document = Model_Document_Courrier()
                document.courrier_id = courrier.id
                document.url_document = url
                document.description = nom_fichier
                document.save()

        return HttpResponseRedirect(reverse('app_courrier_details_depart', args=(courrier.id,)))        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_courrier_add_depart'))


def get_details_depart(request, ref):

    try:
        droit = "VOIR_COURRIER_DEPART"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse 

        ref = int(ref)
        model = Model_Courrier.objects.get(pk = ref)
        
        context = {
            'title' : str(model.numero),
            'model' : model,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }

        template = loader.get_template("Soluplus/App_Courrier/courrier/depart/item.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("ERREUR DETAIL")
        print(e)
        return HttpResponseRedirect(reverse('app_courrier_list_exped'))


def get_traiter_depart(request,ref):
    droit = "TRAITER_COURRIER_DEPART"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    courrier = Model_Courrier.objects.get(pk = ref)

    context = {
        'title' : 'Traiter courrier arrivé',
        'model' : courrier,
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
    }
    template = loader.get_template("Soluplus/App_Courrier/courrier/depart/traiter.html")
    return HttpResponse(template.render(context, request))


def post_traiter_depart(request):
    try:

        droit = "CREER_COURRIER_DEPART"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse

        ref = request.POST["ref"]
        date_traitement = request.POST["date_traitement"]
        date_traitement = utils.toDate(date_traitement)
        
        courrier = Model_Courrier.objects.get(pk = ref)
        courrier.est_traite = True
        courrier.date_traitement = date_traitement
        courrier.save()
        
        return HttpResponseRedirect(reverse('app_courrier_details_depart', args=(ref)))        
    except Exception as e:
        print("ERREUR !")
        print(e)
        messages.add_message(request, messages.ERROR, e)
        return HttpResponseRedirect(reverse('app_courrier_depart_traiter'))



#FILTRAGE COURRIER RECU

def get_rapport_recu_filter(request):
    droit = "VOIR_FILTRE_COURRIER_RECU"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    natures = Model_Nature_Courrier.objects.all().order_by('designation')

    expediteurs = Model_Personne.objects.all()
    destinataires = Model_Employe.objects.all()

    
    context = {
        'title' : 'Filtres Courriers arrivés',
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
        'natures' : natures,
        'expediteurs' : expediteurs,
        'destinataires' : destinataires,
    }
    template = loader.get_template("Soluplus/App_Courrier/rapport_recu/create.html")
    return HttpResponse(template.render(context, request))


def get_rapport_recu_rapport(request):
    try:
        droit = "VOIR_FILTRE_COURRIER_RECU"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        
        utilisateur = auth.getEmploye(request)
        today = datetime.today()

        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']
        
        date_debut_bcp = request.POST['date_debut']
        date_fin_bcp = request.POST['date_fin']

        date_debut = utils.toDate(date_debut)
        date_fin = utils.toDate(date_fin)

        date_filtre = int(request.POST['date_filtre'])
        nature_id = int(request.POST['nature_id'])
        expediteur_id = int(request.POST['expediteur_id'])
        destinataire_id = int(request.POST['destinataire_id'])
        numero_filtre = int(request.POST['numero_filtre'])
        numero = request.POST['numero']

        courriers = []

        if date_filtre == 1:
            courriers = Model_Courrier.objects.filter(type_id = 1,date_creation__date__range = [date_debut, date_fin])
        elif date_filtre == 2:
            courriers = Model_Courrier.objects.filter(type_id = 1,date_reception__date__range = [date_debut, date_fin])
        elif date_filtre == 3:
            courriers = Model_Courrier.objects.filter(type_id = 1,date_reponse__date__range = [date_debut, date_fin])

        if nature_id != 0:
            courriers = courriers.filter(nature_id = nature_id)
        
        if expediteur_id != 0:
            courriers = courriers.filter(expediteur_id = expediteur_id)

        if numero != "":
            if numero_filtre == 1:
                courriers = courriers.filter(numero = numero)
            elif numero_filtre == 2:
                courriers = courriers.filter(numero_enregistrement = numero)

        if destinataire_id != 0:
            valid_courriers = courriers
            for item in courriers:
                data = Model_Destinataire_Courrier.objects.filter(destinataire_id = destinataire_id, courrier_id = item.id)
                if not data:
                    valid_courriers = valid_courriers.exclude(pk=item.id)
            courriers = valid_courriers
                
        
        context = {
            'title' : 'Filtre des courriers arrivés du ' + date_debut_bcp + ' au ' + date_fin_bcp,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model' : courriers,
            'total' : courriers.count,
            'traites' : courriers.filter(est_traite = True).count,
            'instance' : courriers.filter(date_reponse__date__gte = today).count,
            'retard' : courriers.filter(date_reponse__date__lt = today).count,
        }
        
        template = loader.get_template("Soluplus/App_Courrier/rapport_recu/rapport.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)



#FILTRAGE COURRIER ENVOYE

def get_rapport_envoye_filter(request):
    droit = "VOIR_FILTRE_COURRIER_ENVOYE"
    reponse, modules, menus, module, menu = auth.getAuth(request, droit)
    if reponse != None:
        return reponse    

    natures = Model_Nature_Courrier.objects.all().order_by('designation')

    expediteurs = Model_Employe.objects.all()
    destinataires =  Model_Personne.objects.all()

    context = {
        'title' : 'Filtres Courriers départs',
        'modules' : modules,
        'module' : module,
        'menus' : menus,
        'menu' : menu,
        'natures' : natures,
        'expediteurs' : expediteurs,
        'destinataires' : destinataires,
    }
    template = loader.get_template("Soluplus/App_Courrier/rapport_envoye/create.html")
    return HttpResponse(template.render(context, request))


def get_rapport_envoye_rapport(request):
    try:
        droit = "VOIR_FILTRE_COURRIER_ENVOYE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        
        utilisateur = auth.getEmploye(request)
        today = datetime.today()

        date_debut = request.POST['date_debut']
        date_fin = request.POST['date_fin']
        
        date_debut_bcp = request.POST['date_debut']
        date_fin_bcp = request.POST['date_fin']

        date_debut = utils.toDate(date_debut)
        date_fin = utils.toDate(date_fin)

        date_filtre = int(request.POST['date_filtre'])
        nature_id = int(request.POST['nature_id'])
        expediteur_id = int(request.POST['expediteur_id'])
        destinataire_id = int(request.POST['destinataire_id'])
        numero = request.POST['numero']

        courriers = []

        if date_filtre == 1:
            courriers = Model_Courrier.objects.filter(type_id = 2,date_creation__date__range = [date_debut, date_fin])
        elif date_filtre == 2:
            courriers = Model_Courrier.objects.filter(type_id = 2,date_envoi__date__range = [date_debut, date_fin])
        

        if nature_id != 0:
            courriers = courriers.filter(nature_id = nature_id)
        
        if expediteur_id != 0:
            courriers = courriers.filter(expediteur_id = expediteur_id)

        if numero != "":
            courriers = courriers.filter(numero_enregistrement = numero)

        if destinataire_id != 0:
            valid_courriers = courriers
            for item in courriers:
                data = Model_Destinataire_Courrier.objects.filter(destinataire_id = destinataire_id, courrier_id = item.id)
                if not data:
                    valid_courriers = valid_courriers.exclude(pk=item.id)
            courriers = valid_courriers
                
        context = {
            'title' : 'Filtre des courriers du ' + date_debut_bcp + ' au ' + date_fin_bcp,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'model' : courriers,
            'total' : courriers.count,
            
        }
        
        template = loader.get_template("Soluplus/App_Courrier/rapport_envoye/rapport.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)