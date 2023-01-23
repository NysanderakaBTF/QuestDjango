from django.urls import path
from .views import *

urlpatterns = [
    path('', SolvedTestsListAPIView.as_view()),
    path('<int:test_pk>/', GenTestAPIView.as_view()),
    path('<int:test_pk>/<int:res_id>', GenTestAPIView.as_view())
]