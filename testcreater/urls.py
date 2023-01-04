from django.urls import path, include
from views import *

urlpatterns = [
    path('all/', TestListAPIView.as_view(), name='list_of_tests'),
    path('create/', TestAPIView.as_view(), name='create_test'),
    path('<int:pk>/udpate/', TestAPIView.as_view(), name='update_test'),
    path('<int:pk>/delete/', TestAPIView.as_view(), name='delete_test'),
    path('<int:pk>/', TestAPIView.as_view(), name='test_detail')


]