from django.urls import path
from captchaapp import views

app_name = "captchaapp"

urlpatterns = [
    path("getcaptcha/", views.getcaptcha, name="getcaptcha")
]
