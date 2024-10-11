from django.urls import path
from core.usuario.views import CustomLoginView
from django.contrib.auth.views import LogoutView
from core.usuario import views


urlpatterns = [
    path('register_candidato/', views.register_candidato, name='register_candidato'),
    path('register_empresa/', views.register_empresa, name='register_empresa'),
    path('', CustomLoginView.as_view(), name='login'),
    path('logout/', LogoutView.as_view(next_page='login'), name='logout')
]
