from django.conf.urls import url
from . import views

urlpatterns = [
    url(r'^$', views.index, name='index'),
    url(r'^graph/*$', views.graph, name='graph'),
    url(r'^subgraph/*$', views.subgraph, name='subgraph'),
]
