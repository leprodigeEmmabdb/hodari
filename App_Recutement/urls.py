from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    url(r'dashboard/$', views.get_index, name="app_tableau_recrutement"),
    
    #ADMIN LINK
    url(r'^list_offre_admin/$', views.get_list_offres_admin, name='app_recrutement_list_offre_admin'),
    url(r'^add_offre_admin/$', views.get_add_offres_admin, name='app_recrutement_add_offre_admin'),
    url(r'^post_offre_admin/$', views.post_add_offre_admin, name='app_recrutement_post_add_offre_admin'),
    url(r'^detail_offre_admin/(?P<ref>[0-9]+)/$', views.get_detail_offre_admin, name = 'app_recrutement_detail_offre_admin'),
    url(r'^update_offre_admin/(?P<ref>[0-9]+)/$', views.get_update_offres_admin, name='app_recrutement_update_offre_admin'),
    url(r'^post_update_offre_admin/$', views.post_update_offre_admin, name='app_recrutement_post_update_offre_admin'),
    
    
    
    
    url(r'^list_candidats/$', views.get_list_of_candidat_admin, name='app_recrutement_list_candidats'),
    url(r'^detail_candidat/(?P<ref>[0-9]+)/$', views.get_detail_of_candidat_admin, name = 'app_recrutement_detail_candidat_admin'),

    url(r'^list_candidatures/$', views.get_list_of_candidature_admin, name='app_recrutement_list_candidatures'),
    url(r'^detail_candidature/(?P<ref>[0-9]+)/$', views.get_detail_of_candidature_admin, name='app_recrutement_detail_candidature'),
    url(r'^traitement_candidature/(?P<ref>[0-9]+)/$', views.get_traitement_candidature_admin, name='app_recrutement_get_traitement_candidature'),
    url(r'^traitement/get_data', views.get_json_get_statut_change, name='app_recrutement_traite_candidature_json'),
    url(r'^traitement/decline', views.traitement_decline_offre, name='app_recrutement_traitement_decline_offre'),
    url(r'^cloturer/dossier', views.get_json_cloturer_dossier, name='app_recrutement_cloturer_cloutrer_json'),
    url(r'^genereted/rapport/(?P<ref>[0-9]+)/$', views.printing_dossier_candidature, name='app_recrutement_printing_dossier_candidature'),


]

