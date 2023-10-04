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
#from App_Vente.models import Model_Pos

from django.contrib.auth.decorators import login_required
from django.template.loader import get_template
from django.template import RequestContext
from django.http import HttpResponse


from django.db.models.functions import (TruncDate, TruncDay, TruncHour, TruncMinute, TruncSecond, TruncMonth)

import random
import string
import time


from django.shortcuts import get_object_or_404 
#from weasyprint import HTML, CSS

from MainApp.Utils.report_css import report_css
from django.views.decorators.cache import cache_control
from django.views.decorators.cache import never_cache


def get_index(request):
    try:
        droit = "VOIR_TABLEAU_DE_BORD_CONFIGURATION"
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
        
        template = loader.get_template("Soluplus/App_Configuration/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        user = request.user
        if user.username == 'admin':
                return HttpResponseRedirect(reverse("permissions"))

# UTILISATEURS
def get_list_user(request):
    try:
        droit = "VOIR_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        utilisateurs = Model_Employe.objects.all()
        
        context = {
            'title' : 'Liste des Utilisateurs',
            'model' : utilisateurs,       
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'menu' : menu, # 11,
        }
        template = loader.get_template("Soluplus/App_Configuration/Utilisateur/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        
def get_add_user(request):
    try:
        droit = "CREER_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        profils = Model_Profil.objects.all().order_by('designation')
        #caisses = Model_Caisse.objects.filter(est_actif = True)
        
        context = {
            'title' : 'Création Utilisateur',
            #'caisses' : caisses,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'profils' : profils,
            'menu' : menu, # 11,
        }
        
        template = loader.get_template("Soluplus/App_Configuration/Utilisateur/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)

@transaction.atomic
def post_add_user(request):
    
    try:
        sid = transaction.savepoint()
        droit = "CREER_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        nom = request.POST['nom']
        #postnom = request.POST['postnom']
        #prenom = request.POST['prenom']
        adresse = request.POST['adresse']
        email = request.POST['email']
        telephone = request.POST['telephone']
        profile_id = request.POST['profil_id']
        password = request.POST['password']
        conf_password = request.POST['conf_password']
        username = request.POST['username']
        
        profile = Model_Profil.objects.get(pk = profile_id)
        
        if password != conf_password:
            messages.add_message(request, messages.ERROR, "Les mots de passes ne correspondent pas")
            return HttpResponseRedirect(reverse("add_user"))
        
        user = User.objects.create_user(
                username = username,
				password = password,
                email    = email,
                first_name = nom,
			)
        
        utilisateur = Model_Employe()
        utilisateur.nom = nom
        #utilisateur.postnom = postnom
        #utilisateur.prenom = prenom
        utilisateur.adresse = adresse
        utilisateur.email = email
        utilisateur.phone = telephone
        utilisateur.profil_id = profile_id
        utilisateur.user_id = user.id
        if profile.est_profil_caisse == True:
            utilisateur.est_caissier = True
        utilisateur.save()
        
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('list_user'))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survénue lors de l'enregistrement")
        return HttpResponseRedirect(reverse("add_user"))

def get_detail_user(request, ref):
    try:
        
        droit = "VOIR_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        today = datetime.datetime.today()
        
        utilisateur = Model_Employe.objects.get(pk = ref)
        #pos = Model_Pos.objects.all()

        context = {
            'title' : utilisateur.user.username,
            'model' : utilisateur,  
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'pos' : pos,
            'menu' : menu, 
        }
        template = loader.get_template("Soluplus/App_Configuration/Utilisateur/detail.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)

@transaction.atomic
def post_add_caisse_user(request):
    
    try:
        sid = transaction.savepoint()
        droit = "CREER_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        caisse_id = request.POST['caisse_id']
        user_id = request.POST['user_id']
        
        utilisateur = Model_Employe.objects.get(pk = user_id)
        utilisateur.caisse_id = caisse_id
        utilisateur.save()
        
        print(user_id)
        print(utilisateur.id)
        
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('detail_user', args=(user_id,)))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survénue lors de l'enregistrement")
        return HttpResponseRedirect(reverse('detail_user', args=(user_id,)))


@transaction.atomic
def post_add_pos_user(request):
    
    try:
        sid = transaction.savepoint()
        droit = "CREER_UTILISATEUR"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        pos_id = request.POST['pos_id']
        user_id = request.POST['user_id']
        
        utilisateur = Model_Employe.objects.get(pk = user_id)
        utilisateur.pos_id = pos_id
        utilisateur.save()
        
        print(user_id)
        print(utilisateur.id)
        
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('detail_user', args=(user_id,)))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survénue lors de l'enregistrement")
        return HttpResponseRedirect(reverse('detail_user', args=(user_id,)))


# PROFIL
def get_add_prodil(request):
    try:
        droit = "CREER_PROFIL"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        utilisateurs = Model_Employe.objects.all()
        
        context = {
            'title' : 'Création de profil',
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Configuration/Profil/add_profil.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        
@transaction.atomic
def post_add_profil(request):
    
    try:
        sid = transaction.savepoint()
        droit = "CREER_PROFIL"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        designation = request.POST['designation']
        EstCaisse = False
        
        try:
            est_caisse = request.POST['est_caisse']
            EstCaisse = True
        except Exception as e:
            pass
        
        profil = Model_Profil()
        profil.designation = designation
        profil.est_profil_caisse = EstCaisse
        profil.save()
        
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('permissions'))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survénue lors de l'enregistrement")
        return HttpResponseRedirect(reverse("add_profil"))

def toGenerateNumero(prefixe):
    
    annee = str(timezone.now().year)
    annee = annee[2:5]
    print(annee)
    temp_numero = prefixe + ''.join(random.choice(string.ascii_uppercase + string.digits) for _ in range(8)) + "-" + annee
    return temp_numero


# PERMISSION
def get_permissions(request):
    
    try:
        droit = "VOIR_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        today = datetime.datetime.today()
        profils = Model_Profil.objects.all()
        
        context = {
            'title' : "Permissions",
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'profils' : profils,
            'menu' : menu, # 10,
        }
        template = loader.get_template("Soluplus/App_Configuration/Permission/permissions.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)        

def get_detail_droit(request, ref):
    
    try:
        droit = "VOIR_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit)
        if reponse != None:
            return reponse
        
        today = datetime.datetime.today()
        profil = Model_Profil.objects.get(pk = ref)
        profil = profil.designation
        
        
        data = []
        droit_list = Model_Droit.objects.all()
        
        for item in droit_list:
            droit = item.profils.find(profil+',')
            if droit == -1:
                pass
            else : 
                data.append(item)
        
        print(data)
        context = {
            'title' : "Permissions : " + profil,
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'profil' : profil,
            'droits' : data,
            'ref' : ref,
            'menu' : menu, # 10,
        }
        
        template = loader.get_template("Soluplus/App_Configuration/Profil/detail_profil.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        
def get_add_permissions(request, ref):
    
    try:
        droit = "VOIR_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        profil = Model_Profil.objects.get(pk = ref)
        profil = profil.designation
        
        
        data = []
        droit_list = Model_Droit.objects.all()
        
        for item in droit_list:
            droit = item.profils.find(profil+',')
            if droit == -1:
                data.append(item)
            
                
        context = {
            'title' : "Ajouter Permissions : %s" % profil,
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'droits' : data,
            'profil_id' : ref,
            'menu' : menu, # 10,
        }
        template = loader.get_template("Soluplus/App_Configuration/Permission/add_permission.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        return HttpResponse(template.render(context, request))

@transaction.atomic
def post_add_permissions(request):
    
    try:
        sid = transaction.savepoint()
        droit = "MODIFIER_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        profil_id = request.POST['profil_id']
        profil = Model_Profil.objects.get(pk = profil_id)
        
        list_id_droits = request.POST.getlist('my_multi_select2[]', None)
        
        for i in range(0, len(list_id_droits)) :
            droit_id = int(list_id_droits[i])
        
            droit = Model_Droit.objects.get(pk = droit_id)

            if droit.profils == None or droit.profils == '':
                droit.profils = ',' + profil.designation + ','
            else:
                droit.profils = droit.profils + profil.designation + ','
            droit.save()
            
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('detail_profil', args=(profil_id,)))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
        return HttpResponseRedirect(reverse("login"))

def get_remove_permissions(request, ref):
    
    try:
        droit = "MODIFIER_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        profil = Model_Profil.objects.get(pk = ref)
        profil = profil.designation
        
        
        data = []
        droit_list = Model_Droit.objects.all()
        
        for item in droit_list:
            droit = item.profils.find(profil+',')
            if droit == -1:
                pass
            else:
                data.append(item)
            
                
        context = {
            'title' : "Enlever Permissions : %s" % profil,
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'droits' : data,
            'profil_id' : ref,
            'menu' : menu, # 10,
        }
        template = loader.get_template("Soluplus/App_Configuration/Permission/remove_permission.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        return HttpResponse(template.render(context, request))

@transaction.atomic
def post_remove_permissions(request):
    
    try:
        sid = transaction.savepoint()
        droit = "MODIFIER_PERMISSIONS"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        profil_id = request.POST['profil_id']
        profil = Model_Profil.objects.get(pk = profil_id)
        
        list_id_droits = request.POST.getlist('my_multi_select2[]', None)
        
        for i in range(0, len(list_id_droits)) :
            droit_id = int(list_id_droits[i])
        
            droit = Model_Droit.objects.get(pk = droit_id)

            profil_name = ','+profil.designation + ','
            droit_profil = droit.profils.replace(profil_name,',')
            if droit_profil == ',':
                droit_profil = ''
            else:
                droit_profil = droit_profil
            
            print("DROIIIIIIIIIIIIIIIIIIIT")
            print(droit_profil)

            droit.profils = droit_profil
            droit.save()
            
        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse('detail_profil', args=(profil_id,)))
    except Exception as e:
        print("ERREUR DROIT")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
        return HttpResponseRedirect(reverse("login"))


# CATEGORIE
def get_list_devise(request):
    try:
        droit = "VOIR_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        model = Model_Devise.objects.all()
        
        context = {
            'title' : 'Liste des Devises',
            'model' : model,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        template = loader.get_template("Soluplus/App_Configuration/Devise/list.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        return HttpResponseRedirect(reverse('index'))

@never_cache
def get_add_devise(request):
    try:
        droit = "CREER_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        context = {
            'title' : 'Création de Devise',
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            
        }
        template = loader.get_template("Soluplus/App_Configuration/Devise/add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)

@transaction.atomic
def post_add_devise(request):
    
    try:
        sid = transaction.savepoint()
        droit = "CREER_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        designation = request.POST['designation']
        symbole = request.POST['symbole']
        
        employe = auth.getEmploye(request)

        devise = Model_Devise()
        devise.designation = designation
        devise.symbole = symbole
        devise.save()

        tx = Model_Taux_du_jour.objects.filter(devise_id = devise.id)
        if tx:
            for it in tx:
                it.est_actif = False
                it.save()

        taux = Model_Taux_du_jour()
        taux.taux = 1
        taux.devise_id = devise.id
        taux.est_actif = True
        taux.auteur_id = employe.id
        taux.save()

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("app_configuration_list_devise"))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de création")
        return HttpResponseRedirect(reverse("app_configuration_add_devise"))

def get_detail_devise(request, ref):
    try:
        droit = "VOIR_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        devise = Model_Devise.objects.get(pk=ref)
        
        context = {
            'title' : devise.designation,
            'model' : devise,
            'modules' : modules,
            'module' : module,
            'menus' : menus,
            'menu' : menu,
        }
        
        template = loader.get_template("Soluplus/App_Configuration/Devise/detail.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)
        return HttpResponseRedirect(reverse("list_caisse"))

@never_cache
def get_add_taux(request, ref):
    try:
        droit = "MODIFIER_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse

        devise_id = ref
        
        context = {
            'title' : 'Taux',
            'modules' : modules,     
            'module' : module,
            'menus' : menus,
            'menu' : menu,
            'devise_id' : devise_id,
            
        }
        template = loader.get_template("Soluplus/App_Configuration/Devise/taux_add.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)

@transaction.atomic
def post_add_taux(request):
    
    try:
        sid = transaction.savepoint()
        droit = "MODIFIER_DEVISE"
        reponse, modules, menus, module, menu = auth.getAuth(request, droit) 
        if reponse != None:
            return reponse
        
        
        devise_id = request.POST['devise_id']
        tj = float(request.POST['taux'])

        print("REQUEST %s" % request.POST)
        employe = auth.getEmploye(request)
        
        tx = Model_Taux_du_jour.objects.filter(devise_id = devise_id)
        if tx:
            for it in tx:
                it.est_actif = False
                it.save()


        taux = Model_Taux_du_jour()
        taux.taux = tj
        taux.devise_id = devise_id
        taux.est_actif = True
        taux.auteur_id = employe.id
        taux.save()

        transaction.savepoint_commit(sid)
        return HttpResponseRedirect(reverse("app_configuration_list_devise"))
    except Exception as e:
        print("ERREUR")
        print(e)
        transaction.savepoint_rollback(sid)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentative de création")
        return HttpResponseRedirect(reverse("app_configuration_add_devise"))
