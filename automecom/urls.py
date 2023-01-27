from django.urls import path
from . import views

app_name = "automecom"
urlpatterns = [
    path('', views.home_view, name="Home")]
