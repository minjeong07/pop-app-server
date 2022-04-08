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
    # path("signin/", views.LoginView.as_view(), name="signin"),
    # path("signup/", views.SignUpView.as_view(), name="signup"),
    # path("is_id/", views.is_id, name="isid"),
    # path("is_email/", views.is_email, name="isemail"),
    # path('kakao/', views.to_kakao, name='kakao'),
    # path('kakao/callback/', views.from_kakao, name='kakako_login'),
    # path('logout/', views.log_out, name='logout'),
]
