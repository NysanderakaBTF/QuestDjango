"""quest URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/4.1/topics/http/urls/
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
from django.conf.urls.static import static
from django.contrib import admin
from django.urls import path, include, re_path
from rest_framework_simplejwt.views import *

from quest import settings

urlpatterns = [
    re_path(r'^auth/', include('djoser.urls')),
    re_path(r'^auth/', include('djoser.urls.authtoken')), #почему не работвет????
    path('api/token/', TokenObtainPairView.as_view(), name='token_obtain_view'),
    path('api/token/refresh', TokenRefreshView.as_view(), name='token_refresh_view'),
    path('admin/', admin.site.urls),

    path('', include('testcreater.urls')),
    path('users/', include('usercontrol.urls')),
    path('tests/', include('testcreater.urls')),
    path('generate/', include('testgen.urls'))
]
if settings.DEBUG:
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
