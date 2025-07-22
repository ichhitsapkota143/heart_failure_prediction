from django.urls import path
from . import views

app_name = 'bluetooth_data'
urlpatterns = [
    path('get_bluetooth_data/', views.get_bluetooth_data, name='get_bluetooth_data'),
    path('dashboard/', views.dashboard, name='dashboard'),
]
