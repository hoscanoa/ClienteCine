# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import PaginaInicio, Logear, RegistrarCliente, \
    Salir, PaginaCartelera, ComplejosPorCiudad, PaginaButacas, \
    PaginaReservacion, PaginaConfirmacion, PaginaProfile, ActualizarCliente, PaginaHistorial

urlpatterns = patterns('',
                       # Examples:
                       # url(r'^$', 'ClientePython.views.home', name='home'),
                       # url(r'^ClientePython/', include('ClientePython.foo.urls')),

                       # Uncomment the admin/doc line below to enable admin documentation:
                       # url(r'^admin/doc/', include('django.contrib.admindocs.urls')),

                       # Uncomment the next line to enable the admin:
                       # url(r'^admin/', include(admin.site.urls)),

                       url(r'^$', PaginaInicio),
                       url(r'logear/$', Logear.as_view()),
                       url(r'registrarCliente/$', RegistrarCliente.as_view()),
                       url(r'actualizarCliente/$', ActualizarCliente.as_view()),

                       url(r'salir/$', Salir),
                       url(r'^cartelera/(\d{1,6})/(\d{1,6})/(\d{2}/\d{2}/\d{4})/$', PaginaCartelera),

                       url(r'^complejosPorCiudad/$', ComplejosPorCiudad),

                       url(r'^cartelera/butacas/(\d{2}/\d{2}/\d{4})/(\d{1,6})/(\d{2}:\d{2})/(\d{1,6})/$', PaginaButacas),
                       url(r'^cartelera/butacas/reservacion/(\S+)/(\d{1,2})/(\d{1,4})/$', PaginaReservacion),
                       url(r'cartelera/butacas/reservacion/confirmacion/(\S+)/(\S+)/$', PaginaConfirmacion),

                       url(r'profile/$', PaginaProfile),

                       url(r'historial/$', PaginaHistorial),

                       )
