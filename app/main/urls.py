from django.contrib import admin
from django.urls import path
from . import views
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('export_requests/', views.export_to_excel, name='export_requests_excel'),
    path('', views.index, name='index'),
    path('about/', views.about, name='about'),
    path('service/', views.service, name='service'),
    path('project/', views.project, name='project'),
    path('terms/', views.terms, name='terms'),
    path('contact/', views.contact, name='contact'),


    # Authentication
    path('login/', views.login, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('forgot-password/', views.forgot_password, name='forgot'),
    path('verify-otp/', views.verify_otp, name='verify_otp'),
    path('reset-password/', views.reset_password, name='reset_password'),

    # Dashboard and Admin Pages
    path('upload/', views.upload_project, name='upload_project'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('solar_requests/', views.solar_requests_details, name='solar_requests_details'),
    path('cctv_requests/', views.cctv_requests_details, name='cctv_requests_details'),
    path('delete_solar_request/<int:enquiry_id>/', views.delete_solar_request, name='delete_solar_request'),
    path('delete_cctv_request/<int:enquiry_id>/', views.delete_cctv_request, name='delete_cctv_request'),
    path('Project-Editor/' , views.project_backend, name="project-be"),
    path('storage_usage/', views.storage_usage_view, name='storage_usage'),

    # Admin Features
    path('profile/', views.profile, name='profile'),
    path('delete_project/<int:id>/', views.delete_project, name='delete_project'),

] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)

