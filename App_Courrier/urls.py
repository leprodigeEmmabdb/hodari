from django.conf.urls import include, url
from App_Courrier import views 

urlpatterns = [
    # TABLEAU DE BORD URLS
	url(r'^$', views.get_home, name='app_courrier_tableau'),

	#client
	url(r'^exped/list', views.get_lister_exped, name='app_courrier_list_exped'),
	url(r'^exped/add', views.get_creer_exped, name='app_courrier_add_exped'),
	url(r'^exped/post_add', views.post_creer_exped, name='app_courrier_post_add_exped'),
	url(r'^exped/item/(?P<ref>[0-9]+)/$', views.get_details_exped, name='app_courrier_details_exped'),

	#courrier arrivee
	url(r'^arrivee/date/list/$', views.get_lister_date_arrivee, name="app_courrier_list_date_arrivee"),
	url(r'^arrivee/list', views.get_lister_arrivee, name='app_courrier_list_arrivee'),
	url(r'^arrivee/add', views.get_creer_arrivee, name='app_courrier_add_arrivee'),
	url(r'^arrivee/post_add', views.post_creer_arrivee, name='app_courrier_post_add_arrivee'),
	url(r'^arrivee/item/(?P<ref>[0-9]+)/$', views.get_details_arrivee, name='app_courrier_details_arrivee'),
	url(r'^arrivee/traiter/(?P<ref>[0-9]+)/$', views.get_traiter_arrivee, name='app_courrier_arrivee_traiter'),
	url(r'^arrivee/post_traiter', views.post_traiter_arrivee, name='app_courrier_arrivee_post_traiter'),

	#courrier départ
	url(r'^depart/date/list/$', views.get_lister_date_depart, name="app_courrier_list_date_depart"),
	url(r'^depart/list', views.get_lister_depart, name='app_courrier_list_depart'),
	url(r'^depart/add', views.get_creer_depart, name='app_courrier_add_depart'),
	url(r'^depart/post_add', views.post_creer_depart, name='app_courrier_post_add_depart'),
	url(r'^depart/item/(?P<ref>[0-9]+)/$', views.get_details_depart, name='app_courrier_details_depart'),

	#filtrage courrier arrivee
	url(r'^arrivee/filtre/', views.get_rapport_recu_filter, name="app_courrier_rapport_recu_filter"),
    url(r'^arrivee/rapport/', views.get_rapport_recu_rapport, name="app_courrier_rapport_recu"),

	#filtrage courrier départ
	url(r'^depart/filtre/', views.get_rapport_envoye_filter, name="app_courrier_rapport_envoye_filter"),
    url(r'^depart/rapport/', views.get_rapport_envoye_rapport, name="app_courrier_rapport_envoye"),
]
