from django.core.mail import send_mail
from django.conf import settings
from django.template.loader import render_to_string
from django.utils.html import strip_tags


def send_email_verify(email, token):
    subject = 'FLE - Verify your email'
    message = f'Click to verify your email: http://localhost:5173/verify-email/{token}/'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    send_mail(subject, message, email_from, recipient_list)
    return True


def send_event_approve_mail(user, event):

    message = f' Hi {user.first_name}, Your event "{event.event_name}" has been approved by the admin and is now published.'
    event_url = f'http://localhost:5173/events/eventdetail/{event.id}'
    email = user.email

    subject = 'Your Event Has Been Approved'
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]
    print(email, message)
    print(event_url, 'event url')

    html_message = render_to_string(
        'event_approve.html', {'event_name': event.event_name, 'event_url': event_url})

    send_mail(subject, message, email_from,
              recipient_list, html_message=html_message)
    print('true inside function')
    return True


def send_contribution_email(user, event):

    email = user.email
    subject = 'Thank you for contributing to the event!'
    html_message = render_to_string('comtribution_mail.html', {'user': user, 'event': event})
    plain_message = strip_tags(html_message)
    email_from = settings.EMAIL_HOST_USER
    recipient_list = [email]

    send_mail(subject, plain_message, email_from,
              recipient_list, html_message=html_message)
