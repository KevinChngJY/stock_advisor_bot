from django.urls import path
from django.conf.urls import url, include
from .import views

urlpatterns = [
    path('option3_add/', views.option3_add, name="option3_add"),
    path('option3_delete/', views.option3_delete, name="option3_delete"),
    path('option6_login/', views.option6_login, name="option6_login")
]