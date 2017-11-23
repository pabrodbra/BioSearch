from django.conf.urls import url
from django.conf import settings
from django.conf.urls.static import static

from SparqlBS import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^pathway$', views.search_pathways, name='pathway'),
    url(r'^reaction$', views.index, name='reaction'),
    url(r'^controllers$', views.index, name='controllers'),
    url(r'^protein$', views.index, name='protein'),
]
