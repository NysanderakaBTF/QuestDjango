import random
from datetime import datetime

import mongoengine
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.generics import ListAPIView, get_object_or_404
from rest_framework.exceptions import NotAcceptable

from testcreater.models import Test, Question
from testcreater.serializers import QuestionAnswerSerializer
from testgen.serializers import TestsListSerializer
from rest_framework.permissions import IsAuthenticated

from .permissions import ViewSolveTestPermisson
from .models import *
import os
import mongoengine

a = mongoengine.connect(db=os.getenv('MONGODB_NAME'),
                    host=os.getenv('MONGO_HOST'),
                    port=int(os.getenv('MONGO_PORT'))

                    )
class SolvedTestsListAPIView(ListAPIView):
    serializer_class = TestsListSerializer
    permission_classes = (IsAuthenticated,)

    def get_queryset(self):
        return GeneratedTest.objects(user_id=self.request.user.id)


def gen_ans_to_question(selected_q: Question):
    result = []
    cur_ans = list(selected_q.answers.all())
    # put 1 correct answer
    for l in cur_ans:
        if l.is_correct:
            # result.append(AnswerVariantSerializer(instance=l).data)
            result.append(l)
            cur_ans.remove(l)
            break
    for j in range(1, selected_q.answer_var_n):
        f = cur_ans[random.randint(0, len(cur_ans) - 1)]
        # result.append(AnswerVariantSerializer(instance=f).data)
        result.append(f)
        cur_ans.remove(f)
    return result


def generate_random_questions(test_for: Test):
    test_q = list(test_for.questions.all())
    res = []
    for i in range(0, test_for.n_quest):
        pos = random.randint(0, len(test_q) - 1)
        selected_q = test_q[pos]
        temp = GeneratedQuestion()

        temp.question_id = selected_q.pk
        test_q.remove(selected_q)
        answers = gen_ans_to_question(selected_q)
        temp.answers = QuestionAnswerSerializer(answers, many=True)
        res.append(temp)
    return res


def generate_positional_questions(test_for: Test):
    test_q = list(test_for.questions.all())
    res = []
    for i in range(0, test_for.n_quest):
        q_var = [ques for ques in test_q if ques.position_in_test == i]
        selected_q = q_var[random.randint(0, len(q_var) - 1)]
        temp = GeneratedQuestion()
        temp.question_id = selected_q.pk
        test_q.remove(selected_q)
        answers = gen_ans_to_question(selected_q)
        # temp.answers = QuestionAnswerSerializer(answers, many=True)
        temp.answers = list(answers)
        res.append(temp)
    return list(res)


def check_question(user_ans, question: GeneratedQuestion):
    score_per_answ = question.max_score / len(question.answers)
    score = 0
    for i in question.answers:
        if i['is_correct'] and i['id'] in user_ans:
            score += score_per_answ
        elif not i['is_correct'] and i['id'] not in user_ans:
            score += score_per_answ
    question.user_score = score
    question.given_answer = user_ans
    return score


class GenTestAPIView(APIView):
    permission_classes = (ViewSolveTestPermisson,)
    def get(self, request, test_pk):
        test_base = get_object_or_404(Test, pk=test_pk)
        g_test = GeneratedTest(
            test_id=test_base.pk,
            user_id=request.user.id,
        )
        if test_base.is_positional:
            all_q = generate_positional_questions(test_base)
        else:
            all_q = generate_random_questions(test_base)
        print(isinstance(all_q, list))
        print(all_q)
        g_test.questions = list(all_q)
        g_test.start_time = datetime.now()
        g_test.end_time = datetime.now() + test_base.duration
        g_test.save('gen_connect')
        return Response(g_test.to_json())

    def put(self, request, test_pk, res_id):
        upd_res = GeneratedTest.objects(id=res_id)
        '''
        request data template:
        {
            end_time:
            questions:[
            {
                id:int
                answers:[
                    id
                ]
            },
            ...
            ]
        }
        '''
        user_res = request.data.get('questions', None)
        score = 0
        for i in upd_res.questions:
            res = next(filter(lambda x: x['id']==i.question_id, user_res))
            score += check_question(res, i)
        upd_res.end_time = datetime.strptime(request['end_time'], "%Y-%m-%d %H:%M:%S.%f")
        upd_res.result = score
        upd_res.save('gen_connect')

        return Response(upd_res.to_json)
