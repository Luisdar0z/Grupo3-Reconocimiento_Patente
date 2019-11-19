# patentes/urls.py

from django.conf.urls import url, re_path
from django.urls import path, include
from patentes import views

from .views import AnaliticaDatos_Tiempo, AnaliticaDatos_Cantidad_al_Dia, AnaliticaDatos_Horarios

urlpatterns = [
	url(r'^$', views.HomePageView.as_view(), name="index"),
	re_path(r'^patentes/$', views.HomeVehiculosView.as_view(), name="vehiculos"),
	re_path(r'^patentes/(?P<rut>[0-9kK]{8,9})/$', views.DetalleVehiculoView.as_view(), name="detalle"),
	url(r'^patentes/create/$', views.VehiculoCreate.as_view(success_url='/patentes/'), name="vehiculo_create"),
	url(r'^patentes/(?P<pk>\d+)/update/$', views.VehiculoUpdate.as_view(success_url='/patentes/'), name="vehiculo_update"),
	url(r'^patentes/(?P<pk>\d+)/delete/$', views.VehiculoDelete.as_view(success_url='/patentes/'), name="vehiculo_delete"),
	url(r'^patentes/search/$', views.VehiculoSearch.as_view(), name="vehiculo_search"),
	url(r'^patentes/search/results/$', views.VehiculoSearchView.as_view(), name="vehiculo_search_view"),
	url(r'^patentes/reconocimiento/$', views.VehiculoReconocimiento.as_view(), name="vehiculo_reconocimiento"),
	url(r'^patentes/registros/$', views.ReportesForm.as_view(), name="registro_vehiculos"),
	url(r'^patentes/registros/results/$', views.ReportesView.as_view(), name="registro_vehiculos_view"),
	url(r'^patentes/analitica/$', views.AnaliticaView.as_view(), name="analitica_view"),
	url(r'^api/analitica/datos/tiempopromedio/$', AnaliticaDatos_Tiempo, name="analitica_datos_tiempos"),
	url(r'^api/analitica/datos/cantidad/$', AnaliticaDatos_Cantidad_al_Dia, name="analitica_datos_cantidad"),
	url(r'^api/analitica/datos/horarios/$', AnaliticaDatos_Horarios, name="analitica_datos_horarios"),
	path('accounts/', include('accounts.urls')),
	path('accounts/', include('django.contrib.auth.urls'))
]