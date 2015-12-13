# -*- coding: utf-8 -*-
import mandrill
import suds
import json

import servicio

API_KEY='JWzaMw9XBGppg4t4HrO5Sg'

def send_mail(template_name, email_to, context):
    mandrill_client = mandrill.Mandrill(API_KEY)
    message = {
        'to': [],
        'global_merge_vars': []
    }
    for em in email_to:
        message['to'].append({'email': em})

    for k, v in context.iteritems():
        message['global_merge_vars'].append(
            {'name': k, 'content': v}
        )
    mandrill_client.messages.send_template(template_name, [], message)

#send_mail('template-1', ["sendto@email.com"], context={'Name': "Bob Marley"})


def Complejos(idCiudad):
    webService = suds.client.Client(servicio.URL_COMPLEJO_WS)
    respuesta = "" + webService.service.listarPorCiudad(idCiudad)
    respuesta = respuesta.replace(" ", "_")
    return json.loads(respuesta)

def Cartelera(idComplejo, fecha):
    webService = suds.client.Client(servicio.URL_CARTELERA_WS)
    respuesta = webService.service.listar(idComplejo, fecha)
    return json.loads(respuesta)

