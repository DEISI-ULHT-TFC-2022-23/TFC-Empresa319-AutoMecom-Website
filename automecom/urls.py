from django.urls import path
from . import views

app_name = "automecom"
urlpatterns = [
    path('home.html', views.home_view, name="Home"),
    path('servico.html', views.servico_view, name="Servico"),
    path('create.html', views.servico_create, name="Create"),
    path('edit/<int:post_id>', views.servico_edit, name='editar'),
    path('delete/<int:post_id>', views.servico_delete, name='apagar'),
]
