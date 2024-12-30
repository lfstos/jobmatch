from django.urls import path

from vagas import views

urlpatterns = [
    path('cadastrar_vaga/', views.cadastrar_vagas, name='cadastrar_vaga'),
    path('listar_vagas/', views.listar_vagas, name='listar_vagas'),
    path('candidatar_vaga/', views.candidatar_vaga, name='candidatar_vaga'),
    path('editar_vaga/', views.editar_vaga, name='editar_vaga'),
    path('excluir_vaga/', views.excluir_vaga, name='excluir_vaga'),
    path('saiba_mais/<int:pk>/', views.saiba_mais, name='saiba_mais'),
]