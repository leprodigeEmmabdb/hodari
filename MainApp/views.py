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

# LOGINS
@never_cache
def get_login(request):
    context = {
        'title' : 'Identifiez-vous au système !',
    }
    template = loader.get_template("Soluplus/MainApp/Utilisateur/login.html")
    return HttpResponse(template.render(context, request))

def post_login(request):

    try:

        username = request.POST.get('username', False)
        password = request.POST.get('password', False)
        user = authenticate(username=username, password=password)
        if user is not None and user.is_active:
            login(request, user)

            return HttpResponseRedirect(reverse("index"))
        else:
            messages.add_message(request, messages.ERROR, "Nous ne reconnaissons pas ces identifiants !")
            return HttpResponseRedirect(reverse("login"))
    except Exception as e:
        print("ERREUR")
        print(e)
        messages.add_message(request, messages.ERROR, "Une erreur est survenue lors de la tentive de connexion")
        return HttpResponseRedirect(reverse("login"))

def get_logout(request):
    #is_connect = identite.est_connecte(request)
    #if is_connect == False: return HttpResponseRedirect(reverse("login"))

    logout(request)

    return HttpResponseRedirect(reverse("login"))

# HOME
def get_index(request):
    try:

        droit = "VOIR_TABLEAU_DE_BORD"
        reponse, modules= auth.getAuthModule(request)
        if reponse != None:
            return reponse


        context = {
            'title' : 'Accueil',
            'modules' : modules,
        }

        template = loader.get_template("Soluplus/MainApp/index.html")
        return HttpResponse(template.render(context, request))
    except Exception as e:
        print("Erreur Index")
        print(e)


#WEBSITE

@never_cache
def get_site_index(request):
    context = {
        'title' : 'Hodari : Services RH et Juridique',
    }
    template = loader.get_template("Soluplus/Website/index.html")
    return HttpResponse(template.render(context, request))
