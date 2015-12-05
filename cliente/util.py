# -*- coding: utf-8 -*-
import mandrill

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

send_mail('template-1', ["sendto@email.com"], context={'Name': "Bob Marley"})