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
