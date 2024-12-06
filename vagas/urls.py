from django.urls import path

from vagas import views

urlpatterns = [
    path('cadastrar_vagas/', views.cadastrar_vagas, name='cadastrar_vagas'),
]