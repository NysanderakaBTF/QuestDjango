from django.urls import path, include
from testcreater.views import *

urlpatterns = [
    path('', TestListAPIView.as_view(), name='list_of_tests'),
    path('create/', TestAPIView.as_view(), name='create_test'),
    path('<int:pk>/udpate/', TestAPIView.as_view(), name='update_test'),
    path('<int:pk>/delete/', TestAPIView.as_view(), name='delete_test'),
    path('<int:pk>/', TestAPIView.as_view(), name='test_detail'),
    path('<int:test_pk>/<int:quest_pk>/',QuestionAPIView.as_view(), name='question_detail'),

    path('category/', CategoryApiView.as_view()),
    path('category/<int:pk>/', CategoryApiView.as_view())


]