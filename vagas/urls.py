from django.urls import path

from vagas import views

urlpatterns = [
    path('cadastrar_vagas/', views.cadastrar_vagas, name='cadastrar_vagas'),
    path('lista_vagas/', views.lista_vagas, name='lista_vagas'),
    path('candidatar_vaga', views.candidatar_vaga, name='candidatar_vaga'),
    path('editar_vaga', views.editar_vaga, name='editar_vaga'),
    path('excluir_vaga', views.excluir_vaga, name='excluir_vaga'),
]