from django.urls import path
from . import views

app_name = "automecom"
urlpatterns = [
    path('', views.home_view, name="Dashboard"),
    path('home.html', views.home_view, name="Home"),
    path('servico.html', views.servico_view, name="Servico"),
    path('create.html', views.servico_create, name="Create"),
    path('edit/<int:post_id>', views.servico_edit, name='editar'),
    path('delete/<int:post_id>', views.servico_delete, name='apagar'),
    path('conselhos.html', views.conselho_view, name="Conselho"),
    path('contactos.html', views.contacto_view, name="Contacto"),
    path('sobre.html', views.sobre_view, name="Sobre"),
    path('marcacao', views.marcacao_view, name="Marcação"),
    path('login.html', views.view_login, name='login'),
    path('logout', views.view_logout, name='logout'),
    path('register.html', views.register_view, name='register'),
    path('perfil.html', views.perfil_view, name="perfil"),
    path('marcacoes', views.marcacoes_view, name="marcacoes"),
    path('editmarc/<int:post_id>', views.marcacao_edit, name='editarmarc'),
    path('deletemarc/<int:post_id>', views.marcacao_delete, name='apagarmarc'),
    path('garantia.html', views.garantia_view, name='garantia'),
    path('privacidade.html', views.privacidade_view, name='privacidade'),
    path('obras.html', views.obras_view, name='obras'),
]
