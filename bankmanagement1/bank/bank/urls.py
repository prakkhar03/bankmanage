from django.urls import path
from django.contrib import admin
from management import views

urlpatterns = [
    path('', views.user_login, name='login'),
    path('register/', views.register, name='register'),
    path('deposit/', views.deposit, name='deposit'),
    path('withdrawal/', views.withdrawal, name='withdrawal'),
    path('balance/', views.balance, name='balance'),
    path('transfer/', views.transfer, name='transfer'),
    path('history/', views.history, name='history'),
    path('mainpage/', views.mainpage, name='mainpage'),
    path('exit/', views.exit, name='exit'),
    path('admin/', admin.site.urls),
]
