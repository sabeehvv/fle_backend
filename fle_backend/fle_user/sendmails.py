from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags






def send_email_verify(email, token):
    email = 'sabeehelv@gmail.com'
    subject = 'FLE - Verify your email'
    message = f'Click to verify your email: http://localhost:5173/verify-email/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True



def send_event_approve_mail(email,message,event_name,event_url):
    email = 'sabeehelv@gmail.com'
    print(email,message)
    subject = 'Your Event Has Been Approved'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    print(event_url,'event url')

    html_message = render_to_string('event_approve.html', {'event_name': event_name ,'event_url': event_url})


    send_mail(subject, message, email_from, recipient_list,html_message=html_message)
    print('true inside function')
    return True