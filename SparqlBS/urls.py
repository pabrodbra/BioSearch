from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from SparqlBS import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^about$', views.about, name='about'),
    url(r'^services$', views.services, name='services'),
    url(r'^contact$', views.contact, name='contact'),
    url(r'^pathway$', views.search_pathways, name='pathway'),
    url(r'^reaction$', views.search_reactions, name='reaction'),
    url(r'^controller$', views.search_controllers, name='controller'),
    url(r'^reactant_product$', views.search_reactant_product, name='reactant_product'),
    url(r'^component_info$', views.search_component_info, name='controller_info'),
]
