from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),
    path('edit/<int:pk>/', views.edit_contact, name='edit_contact'),
    path('delete/<int:pk>/', views.delete_contact, name='delete_contact'),
    path('load-doctors/', views.load_doctors, name='load_doctors'),
    path('recommend/', views.recommend_doctors, name='recommend_doctors'),
    path('doctor/<int:pk>/', views.doctor_detail, name='doctor_detail'),
     path('favorites/', views.favorite_list, name='favorite_list'),
     path('favorite/<int:pk>/toggle/', views.toggle_favorite, name='toggle_favorite'),
     path('health-hub/', views.health_hub, name='health_hub'),
    path('chatbot/', views.chatbot, name='chatbot'),  # this line
]
