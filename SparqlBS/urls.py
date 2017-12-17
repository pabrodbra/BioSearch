from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from SparqlBS import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pathway$', views.search_pathways, name='pathway'),
    url(r'^reaction$', views.search_reactions, name='reaction'),
    url(r'^controller$', views.search_controllers, name='controllers'),
    url(r'^controller_info$', views.search_info_controllers, name='controller_info'),
]
