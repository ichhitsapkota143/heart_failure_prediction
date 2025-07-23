"""
URL configuration for heart_failure_prediction project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path
from django.urls import path, include
from . import views


urlpatterns = [
    path('admin/', admin.site.urls),
    path('', views.Home, name='Home'),
    path('register/', views.Register, name='Register'),
    path('login/', views.Log_in, name='Log_in'),
    path('Dashboard/', views.Dashboard, name='Dashboard'),
    path('predict/', views.predict, name='predict'),
    path('result/', views.result, name='result'),
    path('heart-failure/', views.Heart_failure_problem, name='Heart_failure_problem'),
    path('ecg-diagram/', views.ECG_diagram, name='ECG_diagram'),
    path('get_bluetooth_data/', views.get_bluetooth_data, name='get_bluetooth_data'),
    path('contact-us/', views.Contact_us, name='Contact_us'),
    path('bluetooth/', include('bluetooth_data.urls')), 
]

