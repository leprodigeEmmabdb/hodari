from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    url(r'^$', views.get_index, name="app_configuration_tableau"),
    
    # UTILISATEURS
    url(r'^user/list/$', views.get_list_user, name="list_user"),
    url(r'^user/add/$', views.get_add_user, name="add_user"),
    url(r'^user/post_add/$', views.post_add_user, name="post_add_user"),
    url(r'^user/detail/(?P<ref>[0-9]+)/$', views.get_detail_user, name = 'detail_user'),
    url(r'^user/post_add_caisse_user/$', views.post_add_caisse_user, name="post_add_caisse_user"),
    url(r'^user/post_add_pos_user/$', views.post_add_pos_user, name="post_add_pos_user"),
    
    # PERMISSIONS
    url(r'^permissions/$', views.get_permissions, name="permissions"),
    url(r'^permission/detail/(?P<ref>[0-9]+)/$', views.get_detail_droit, name = 'detail_profil'),
    url(r'^permission/add/(?P<ref>[0-9]+)/$', views.get_add_permissions, name = 'add_permission'),
    url(r'^permission/post_add/$', views.post_add_permissions, name="post_add_permission"),
    url(r'^permission/remove/(?P<ref>[0-9]+)/$', views.get_remove_permissions, name = 'remove_permission'),
    url(r'^permission/post_remove/$', views.post_remove_permissions, name="post_remove_permission"),
    
    # PROFIL
    url(r'^profil/add/$', views.get_add_prodil, name="add_profil"),
    url(r'^profil/post_add/$', views.post_add_profil, name="post_add_profil"),
     

    
    # DEVISES
    url(r'^devise/list/$', views.get_list_devise, name="app_configuration_list_devise"),
    url(r'^devise/add/$', views.get_add_devise, name="app_configuration_add_devise"),
    url(r'^devise/post_add/$', views.post_add_devise, name="app_configuration_post_add_devise"),
    url(r'^devise/detail/(?P<ref>[0-9]+)/$', views.get_detail_devise, name = 'app_configuration_detail_devise'),
    url(r'^devise/taux/add/(?P<ref>[0-9]+)/$', views.get_add_taux, name="app_configuration_add_taux"),
    url(r'^devise/taux/post_add/$', views.post_add_taux, name="app_configuration_post_add_taux"),
    
    
]
