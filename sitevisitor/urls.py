from django.urls import path
from .views import home, registration, user_login, forgot_password, otp_generation, reset_password, unauthorized_access

app_name = 'sitevisitor'
urlpatterns=[
    path('', home, name='home'),
    path('sign_up/', registration , name='sign_up'),
    path('sign_in/',user_login , name='sign_in'),
    path('forgot_password/', forgot_password, name='forgot_password'),
    path('otp/<int:otp>/', otp_generation , name='otp'),
    path('reset_password/', reset_password , name='change_password'),
    path('404/', unauthorized_access , name='404'),

]