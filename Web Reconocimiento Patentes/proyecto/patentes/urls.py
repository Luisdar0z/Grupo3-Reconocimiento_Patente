# patentes/urls.py

from django.conf.urls import url, re_path
from django.urls import path, include
from patentes import views

urlpatterns = [
	url(r'^$', views.HomePageView.as_view(), name="index"),
	re_path(r'^patentes/$', views.HomeVehiculosView.as_view(), name="vehiculos"),
	re_path(r'^patentes/(?P<rut>[0-9kK]{8,9})/$', views.DetalleVehiculoView.as_view(), name="detalle"),
	url(r'^patentes/create/$', views.VehiculoCreate.as_view(success_url='/patentes/'), name="vehiculo_create"),
	url(r'^patentes/search/$', views.VehiculoSearch.as_view(), name="vehiculo_search"),
	url(r'^patentes/search/results/$', views.VehiculoSearchView.as_view(), name="vehiculo_search_view"),
	url(r'^patentes/(?P<pk>\d+)/update/$', views.VehiculoUpdate.as_view(success_url='/patentes/'), name="vehiculo_update"),
	url(r'^patentes/(?P<pk>\d+)/delete/$', views.VehiculoDelete.as_view(success_url='/patentes/'), name="vehiculo_delete"),
	path('accounts/', include('accounts.urls')),
	path('accounts/', include('django.contrib.auth.urls'))
]