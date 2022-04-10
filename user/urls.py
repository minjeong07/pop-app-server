from django.conf import settings
from django.conf.urls.static import static
from django.urls import path

from . import views
app_name = 'user'
urlpatterns = [
    path("mypage/", views.mypage, name="mypage"),
    path('sign-up/', views.sign_up_view, name='sign-up'),
    path('sign-in/', views.sign_in_view, name='sign-in'),
    path('logout', views.logout, name='logout'),
]
