from django.urls import path

from . import views

urlpatterns = [
    path("", views.main, name="main"),
    path("<int:user_id>", views.id_to_username, name="id_to_username"),
    path("<username>", views.CardList, name="CardList"),
    path("upload", views.upload, name="upload"),
]
