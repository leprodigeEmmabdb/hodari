from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    #url(r'^', admin.site.urls),
    
    url(r'^$', views.get_site_index, name="website_index"),
    url(r'^apropos/$', views.get_site_about, name="website_about"),
    url(r'^valeurs/$', views.get_site_valeur, name="website_valeur"),
    url(r'^mission/$', views.get_site_mission, name="website_mission"),
    url(r'^contact/$', views.get_site_contact, name="website_contact"),
    
    
    #RECRUTEMENT
    url(r'^recrutement/$', views.get_site_recrutement, name="website_recrutement"),
    
    #DEPOT CV
    url(r'^apply_depot/$', views.get_page_depot_apply, name='website_apply_depot'),
    url(r'^post_apply_depot/$', views.post_apply_depot, name='website_post_apply_depot'),
    url(r'^ajax/get/poste_recrutement/$', views.ajax_get_poste_recrutement, name="ajax_get_poste_recrutement"),
    url(r'^confirmation/cv/(?P<ref>[0-9]+)/$', views.get_confirmation_depot_cv, name='website_get_confirmation_cv'),
    url(r'^apply_offre/(?P<ref>[0-9]+)/$', views.get_page_offre_apply, name='website_apply_offre'),
    
    
    #OFFRE
    url(r'^list_offre/$', views.get_page_offre_view, name='website_list_offres'),
    url(r'^detail_offre/(?P<ref>[0-9]+)/$', views.get_page_offre_item, name='website_item_offre'),
    
    url(r'^post_apply_offre/$', views.post_apply_offre, name='website_post_apply_offre'),
    url(r'^searching_offre/$', views.post_search_offre_view, name='website_post_search_offre_view'),
    url(r'^confirmation/(?P<ref>[0-9]+)/$', views.get_confirmation, name='website_get_confirmation'),   
]
