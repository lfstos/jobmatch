from django.urls import path
from core.vaga import views


urlpatterns = [
    path('', views.lista_vagas, name='lista_vagas'),
    path('<int:vaga_id>/', views.detalhe_vaga, name='detalhe_vaga'),
    path('criar/', views.criar_vaga, name='criar_vaga'),
    path('<int:vaga_id>/editar/', views.editar_vaga, name='editar_vaga'),
    path('<int:vaga_id>/deletar/', views.deletar_vaga, name='deletar_vaga'),
    path('relatorio/', views.relatorio, name='relatorio'),
]
