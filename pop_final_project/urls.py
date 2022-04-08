from django.conf import settings
from django.conf.urls.static import static

"""pop_final_project URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import include, path
from ninja import NinjaAPI

from card.apis.v1.card_router import router as card_router

api = NinjaAPI()
api.add_router("/card/", card_router)

urlpatterns = [
    path("admin/", admin.site.urls),
    path("", include("user.urls")),
    path("", include("post.urls")),
    path("card/", include("card.urls")),
    path("api/v1/", api.urls),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
