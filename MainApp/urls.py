from django.conf.urls import include, url
from django.contrib import admin
from django.conf import settings
from django.conf.urls.static import static
from . import views

urlpatterns = [
    
    #url(r'^', admin.site.urls),
    url(r'^login/$', views.get_login, name="login"),
    url(r'^post_login/$', views.post_login, name="post_login"),
    url(r'^user/logout/$', views.get_logout, name='logout'),
    url(r'^$', views.get_index, name="index"),
    
]
