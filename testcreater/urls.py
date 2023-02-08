from django.urls import path, include

from testcreater.views import *

urlpatterns = [
    path('', TestListAPIView.as_view(), name='list_of_tests'),
    # path('', TestAPIView.as_view(), name='list_of_tests'),
    path('create/', TestCreateAPIView.as_view(), name='create_test'),
    path('<int:pk>/update/', TestUpdateAPIView.as_view(), name='update_test'),
    path('<int:pk>/delete/', TestAPIView.as_view(), name='delete_test'),
    path('<int:pk>/', TestAPIView.as_view(), name='test_detail'),
    path('<int:pk>/start/', include('testgen.urls')),


    path('<int:test_pk>/<int:pk>/', QuestionAPIView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"}), name='question_detail'),
    path('<int:test_pk>/quesions/', QuesionListAPIView.as_view()),
    path('<int:pk>/create_quesiton/', CreateQuestionAPIView.as_view()),
    # path('<int:test_pk>/<int:quest_pk>/new_ans/', ),
    # path('my/', MyTestListAPIView.as_view(), name='my_tests_list'),


    path('<int:test_pk>/<int:quest_pk>/<int:pk>/',QuestionAnswerAPIView.as_view({"get": "retrieve", "patch": "partial_update", "delete": "destroy"})),
    path('<int:test_pk>/<int:quest_pk>/new_ans/', QuestionAnswerAPIView.as_view({"post":"create"})),

    path('category/', CategoryListAPIView.as_view()),
    path('category/<int:pk>/', CategoryApiView.as_view())

]
