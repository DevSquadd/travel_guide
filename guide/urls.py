from django.urls import path
from . import views

urlpatterns = [
    path('register/', views.register, name='register'),
    path('', views.home, name='home'),
    path('accounts/profile/', views.profile, name='profile'),
    path('plan_trip/', views.plan_trip, name='plan_trip'),
    path('generate_pdf/<int:trip_id>/', views.generate_pdf, name='generate_pdf'),
]