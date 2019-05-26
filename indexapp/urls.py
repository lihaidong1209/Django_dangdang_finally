from django.contrib import admin
from django.urls import path
from indexapp import views

app_name = 'indexapp'

urlpatterns = [
    path('admin/', admin.site.urls),
    path('index/', views.index, name='index'),
    path('book_list/', views.book_list, name='book_list'),
    path('book_details/', views.book_details, name='book_details'),
]