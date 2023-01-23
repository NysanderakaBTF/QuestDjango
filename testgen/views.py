import json
import random
from datetime import datetime

from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.exceptions import NotAcceptable

from testcreater.models import Test
from testcreater.serializers import AnswerVariantSerializer, TestSerializer
from testgen.serializers import TestsListSerializer, GeneratedTestserialize
from rest_framework.permissions import IsAuthenticated

from .generator_permissions import ViewSolveTestPermisson
from .models import *


class SolvedTestsListAPIView(ListAPIView):
    serializer_class = TestsListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return GeneratedTest.objects.filter(user_id=self.request.user.id)


class GenTestAPIView(APIView):
    # permission_classes = (ViewSolveTestPermisson,)

    def get(self, request, test_pk):
        test_base = get_object_or_404(Test, pk=test_pk)
        test_q = list(test_base.questions.all())
        g_test = GeneratedTest(
            test_id=test_base.pk,
            user_id=request.user.id,
        )
        for i in range(0, test_base.n_quest):
            if not test_base.is_positional:
                pos = random.randint(0, len(test_q))
                selected_q = test_q[pos]
                temp = GeneratedQuestion(
                    question_id=selected_q.pk
                )
                # g_test.questions.base_type.append(GeneratedQuestion(
                #     question_id=selected_q.pk
                # ))
                test_q.remove(selected_q)
            else:
                q_var = [ques for ques in test_q if ques.position_in_test == i]
                selected_q = q_var[random.randint(0, len(q_var))]
                # g_test.questions.base_type.append(GeneratedQuestion(
                #     question_id=selected_q.pk
                # ))
                temp = GeneratedQuestion(
                    question_id=selected_q.pk
                )
                test_q.remove(selected_q)

            cur_ans = list(selected_q.answers.all())
            # put 1 correct answer
            for l in cur_ans:
                if l.is_correct:
                    temp.answers.append(AnswerVariantSerializer(instance=l).data)

                    cur_ans.remove(l)
                    break

            for j in range(1, selected_q.answer_var_n):
                f = cur_ans[random.randint(0, len(cur_ans))]
                temp.answers.append(AnswerVariantSerializer(instance=f).data)
                cur_ans.remove(f)
            g_test.questions.base_type.append(temp)
        g_test.start_time = datetime.now()
        g_test.end_time = datetime.now() + test_base.duration
        g_test.save()
        return Response(GeneratedTestserialize(instance=g_test).data)

    def patch(self, request, test_pk, res_id):
        upd_res = GeneratedTest.objects.get(_id=res_id)
        print(request.data, GeneratedTestserialize(instance=upd_res).data)
