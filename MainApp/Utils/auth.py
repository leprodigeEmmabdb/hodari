from MainApp.models import *
from App_Configuration.models import *
from django.shortcuts import render, redirect
from django.http import HttpResponse, HttpRequest, HttpResponseRedirect, JsonResponse
from django.urls import reverse_lazy, reverse

class auth(object):

    """@staticmethod
    def getAuth(request, droit):

        if request.user.is_authenticated == False :
            return HttpResponseRedirect(reverse("login")), None
        else:
            user = request.user
            menus = Model_Menu.objects.all().order_by("groupe__ordre")

            if user.username == 'admin':
                return None, menus

            user = Model_Employe.objects.get(user_id = user.id)
            profil = user.profil.designation

            liste_menu = []

            for item in menus:
                droit_menu = Model_Droit.objects.filter(menu_id = item.id)

                for item2 in droit_menu:
                    res_droit = item2.profils.find(profil+',')
                    if res_droit == -1:
                        pass
                    else:
                        liste_menu.append(item)
                        break


            droit = Model_Droit.objects.get(droit = droit)
            droit = droit.profils.find(profil+',')
            if droit == -1:
                return HttpResponseRedirect(reverse("not_authorized")), liste_menu
            else :
                return None, liste_menu
    """

    @staticmethod
    def getAuth(request, droit):

        if request.user.is_authenticated == False :
            return HttpResponseRedirect(reverse("login")), None, None, None, None
        else:
            user = request.user
            droit = Model_Droit.objects.filter(droit = droit).first()

            modules = Model_Module.objects.filter(est_actif = True).order_by('order')
            menus = Model_Menu.objects.filter(module_id = droit.menu.module.id).order_by("groupe__ordre","ordre")
            mod = droit.menu.module.order
            mnu = droit.menu.ordre

            if user.username == 'chanyadmin':
                return None, modules, menus, mod, mnu

            user = Model_Employe.objects.get(user_id = user.id)
            profil = user.profil.designation

            liste_menu = []
            liste_module = []

            print("MENUSSSSSSSSSSSSS %s" % menus)
            for item in menus:
                print("OKAYYYYYYYYYYYYYy %s" % item.designation)
                droit_menu = Model_Droit.objects.filter(menu_id = item.id)

                for item2 in droit_menu:
                    res_droit = item2.profils.find(profil+',')
                    if res_droit == -1:
                        pass
                    else:
                        liste_menu.append(item)
                        module = Model_Module.objects.get(pk = item.module.id)
                        exist = False

                        for it in liste_module:
                            if it.id == module.id:
                                exist = True
                                break

                        break


            for item in modules :
                droit_menu = Model_Droit.objects.filter(menu__module_id = item.id)
                for item2 in droit_menu:
                    res_droit = item2.profils.find(profil+',')
                    if res_droit == -1:
                        pass
                    else:
                        liste_module.append(item)
                        break



            droit = droit.profils.find(profil+',')
            if droit == -1:
                return HttpResponseRedirect(reverse("not_authorized")), liste_module, liste_menu, mod, mnu
            else :
                return None, liste_module ,liste_menu, mod, mnu

    @staticmethod
    def getAuthModule(request):

        if request.user.is_authenticated == False :
            return HttpResponseRedirect(reverse("login")), None
        else:
            user = request.user

            modules = Model_Module.objects.filter(est_actif = True).order_by('order')

            if user.username == 'chanyadmin':
                return None, modules

            user = Model_Employe.objects.get(user_id = user.id)
            profil = user.profil.designation

            liste_module = []

            for item in modules :
                droit_menu = Model_Droit.objects.filter(menu__module_id = item.id)
                for item2 in droit_menu:
                    res_droit = item2.profils.find(profil+',')
                    if res_droit == -1:
                        pass
                    else:
                        liste_module.append(item)
                        break

            if liste_module == []:
                return HttpResponseRedirect(reverse("not_authorized")), liste_module
            else :
                return None, liste_module

    @staticmethod
    def getProfilUser(request):

        user = request.user

        if user.username == 'admin':
            return "admin"

        user = Model_Employe.objects.get(user_id = user.id)
        profil = user.profil

        return profil


    @staticmethod
    def getEmploye(request):

        user = request.user

        user = Model_Employe.objects.get(user_id = user.id)

        return user

    @staticmethod
    def getEmployeFromId(id):

        user = Model_Employe.objects.get(user_id = id)

        return user