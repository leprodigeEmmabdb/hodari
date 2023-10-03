from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
        
    url(r'^$', views.get_index, name="app_support_tableau"),

    url(r'^reclamation/list', views.get_lister_reclamation, name='app_support_list_reclamations'),
    url(r'^reclamation/attente/$', views.get_lister_reclamation_attente, name='app_support_list_reclamations_attente'),
    url(r'^reclamation/item/(?P<ref>[0-9]+)/$', views.get_details_reclamation, name='app_support_details_reclamation'),
    url(r'^reclamation/commentaire/(?P<ref>[0-9]+)/$', views.get_commentaire, name='app_support_commentaire'),
	url(r'^reclamation/commentaire/post_add/', views.post_commentaire, name='app_support_post_commentaire'),
    
]
