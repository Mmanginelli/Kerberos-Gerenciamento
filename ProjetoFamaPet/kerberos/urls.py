from django.urls import path
from . import views
 
urlpatterns = [
    path('', views.home, name='home'),
 
    # Usuário
    path('clientes/', views.listar_clientes, name='listar_clientes'),
    path('clientes/novo/', views.usuario_criar, name='usuario_criar'),
    path('clientes/<int:pk>/editar/', views.usuario_editar, name='usuario_editar'),
    path('clientes/<int:pk>/excluir/', views.usuario_excluir, name='usuario_excluir'),
 
    # Pet
    path('pets/', views.listar_pets, name='listar_pets'),
    path('pets/novo/<int:usuario_id>/', views.pet_criar, name='pet_criar'),
    path('pets/<int:pk>/editar/', views.pet_editar, name='pet_editar'),
    path('pets/<int:pk>/excluir/', views.pet_excluir, name='pet_excluir'),
 
    # Endereço
    path('enderecos/', views.listar_enderecos, name='listar_enderecos'),
    path('enderecos/novo/', views.endereco_criar, name='endereco_criar'),
    path('enderecos/<int:pk>/editar/', views.endereco_editar, name='endereco_editar'),
    path('enderecos/<int:pk>/excluir/', views.endereco_excluir, name='endereco_excluir'),
 
    # Serviço
    path('servicos/', views.listar_servicos, name='listar_servicos'),
    path('servicos/novo/', views.servico_criar, name='servico_criar'),
    path('servicos/<int:pk>/editar/', views.servico_editar, name='servico_editar'),
    path('servicos/<int:pk>/excluir/', views.servico_excluir, name='servico_excluir'),
 
    # Agendamento
    path('agendamentos/', views.agendamentos, name='agendamentos'),
    path('agendamentos/novo/<int:usuario_id>/', views.agendamento_criar, name='agendamento_criar'),
    path('agendamentos/<int:pk>/editar/', views.agendamento_editar, name='agendamento_editar'),
    path('agendamentos/<int:pk>/excluir/', views.agendamento_excluir, name='agendamento_excluir'),
 
    # Relatório
    path('relatorio/', views.relatorio, name='relatorio'),
]
 
