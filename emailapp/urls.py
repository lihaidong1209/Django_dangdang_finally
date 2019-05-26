from django.contrib import admin
from django.urls import path
from emailapp import views

app_name = 'emailapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('register_verify/', views.register_verify, name='register_verify'),
    path('changeCaptcha_phone/', views.changeCaptcha_phone, name='changeCaptcha_phone'),

]