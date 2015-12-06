# -*- coding: utf-8 -*-
from django.conf.urls import patterns, include, url
from .views import PaginaInicio, Logear, RegistrarCliente, Salir, PaginaCartelera, ComplejosPorCiudad

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
                       url(r'salir/$', Salir),
                       url(r'cartelera/$', PaginaCartelera),

                       url(r'^complejosPorCiudad/$', ComplejosPorCiudad),
                       )
