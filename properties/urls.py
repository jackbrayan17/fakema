# my_real_estate_site/properties/urls.py
from django.urls import path
from . import views

app_name = 'properties' # Namespace for URLs

urlpatterns = [
    path('', views.home_view, name='home'),
    path('properties/', views.property_list_view, name='property_list'),
    path('properties/<slug:slug>/', views.property_detail_view, name='property_detail'),
    path('services/', views.service_list_view, name='service_list'),
    path('projects/', views.project_list_view, name='project_list'),
    path('projects/<slug:slug>/', views.project_detail_view, name='project_detail'),
    path('contact/', views.contact_view, name='contact'),
    path('about/', views.about_view, name='about'),
]