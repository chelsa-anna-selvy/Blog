from django.template import Context
from django.template.loader import render_to_string
from django.core.mail import EmailMessage
from django.conf import settings



def send_otp(email,otp,name,template_name):
      
    context = {        
        'email': email,
        'otp':otp,
        'name':name
    }

    email_subject = 'Reset Password'
    email_body = render_to_string(template_name, context)
    
    my_email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )   
    my_email.content_subtype = 'html'
    return my_email.send(fail_silently=False)

def send_welcome_mail(email,firstname,lastname):
    context ={
        
        'firstname':firstname,
        'lastname':lastname
    }
    email_subject = 'Welcome to Blogger'
    email_body = render_to_string('sitevisitor/welcome.html',context)
    my_email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    my_email.content_subtype = 'html'
    return my_email.send(fail_silently=False)

def update_status_mail(email,firstname,lastname,username,status):
    context ={
        
        'firstname':firstname,
        'lastname':lastname,
        'username':username,
        'status':status
    }
    if status == 'activated':
        email_subject = 'Blogger Account Reactivated'
    else:
        email_subject = 'Blogger Account Temporarily blocked'

    
    email_body = render_to_string('adminpanel/status_user.html',context)
    my_email = EmailMessage(
        email_subject,
        email_body,
        settings.DEFAULT_FROM_EMAIL,
        [email]
    )
    my_email.content_subtype = 'html'
    return my_email.send(fail_silently=False)
