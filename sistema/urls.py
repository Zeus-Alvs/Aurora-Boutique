from django.contrib.auth import views as auth_views
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('criar-conta/', views.criar_conta, name='criar_conta'),
    path('quem-somos/', views.quem_somos, name='quem_somos'),
    path('add-contato/', views.adicionar_contato, name='add_contato'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('contatos/', views.listar_contatos, name='listar_contatos'),
    path('categorias/', views.listar_categorias, name='listar_categorias'),
    path('add-categoria/', views.adicionar_categoria, name='add_categoria'),
    path('edit-categoria/<int:id>/', views.editar_categoria, name='editar_categoria'),
    path('del-categoria/<int:id>/', views.excluir_categoria, name='excluir_categoria'),
    path('produtos/', views.listar_produtos, name='listar_produtos'),
    path('add-produto/', views.adicionar_produto, name='add_produto'),
    path('edit-produto/<int:id>/', views.editar_produto, name='editar_produto'),
    path('del-produto/<int:id>/', views.excluir_produto, name='excluir_produto'),
    path('usuarios/', views.listar_usuarios, name='listar_usuarios'),
    path('edit-usuario/<int:id>/', views.editar_usuario, name='editar_usuario'),
    path('del-usuario/<int:id>/', views.excluir_usuario, name='excluir_usuario'),
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(), name='logout'),
    path('perfil/', views.perfil, name='perfil'),
    path('alterar-senha/', views.alterar_senha, name='alterar_senha'),
    path('comprar/<int:id>/', views.comprar_produto, name='comprar_produto'),
    path('nossos-produtos/', views.vitrine_produtos, name='vitrine_produtos'),
    path('compras/', views.listar_compras, name='listar_compras'),
    path('del-compra/<int:id>/', views.excluir_compra, name='excluir_compra'),
    path('avaliar/<int:compra_id>/', views.avaliar_compra, name='avaliar_compra'),
    path('avaliacoes/', views.listar_avaliacoes, name='listar_avaliacoes'),
    path('del-avaliacao/<str:id>/', views.excluir_avaliacao, name='excluir_avaliacao'),
    path('sincronizar-api/', views.sincronizar_api, name='sincronizar_api'),
    path('add-usuario/', views.adicionar_usuario, name='adicionar_usuario'),
    path('del-contato/<int:id>/', views.excluir_contato, name='excluir_contato'),
    path('relatorio-vendas/', views.relatorio_vendas, name='relatorio_vendas'),
    path('api/dados-vendas/', views.api_dados_vendas, name='api_dados_vendas')
]
