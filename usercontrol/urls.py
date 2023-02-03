from django.urls import path, include
from usercontrol.views import *

urlpatterns = [
    path('', UserListAPIView.as_view()),
    path('create/', CreateUserAPIView.as_view()),
    path('<int:pk>/update/', UpdateUserAPIView.as_view()),
    path('<int:pk>/', RetriveUserAPIView.as_view()),
    path('<int:pk>/delete/', DeleteUserAPIView.as_view()),

    path('groups/', ListGroupAPIView.as_view()),
    path('groups/create/', CreateGroupAPIView.as_view()),
    path('groups/<int:pk>/', RetriveGroupAPIView.as_view()),
    path('groups/<int:pk>/delete/', UpdateDeleteGroupAPIView.as_view()),
    path('groups/<int:pk>/update/', UpdateDeleteGroupAPIView.as_view()),

]
