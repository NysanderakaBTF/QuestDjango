from djongo import models

class GeneratedQuestion(models.Model):
    user_score = models.IntegerField(blank=True)
    question_id = models.IntegerField()
    answers = models.JSONField(default=dict())
    given_answer = models.JSONField(blank=True)

    class Meta:
        abstract = True


class GeneratedQuestionNonAbstract(models.Model):
    user_score = models.IntegerField(blank=True)
    question_id = models.IntegerField()
    answers = models.JSONField(default=dict())
    given_answer = models.JSONField(blank=True)



class GeneratedTest(models.Model):
    user_id = models.IntegerField(blank=True, db_index=True)
    test_id = models.IntegerField(db_index=True)
    _id = models.UUIDField()
    questions = models.ArrayField(model_container=GeneratedQuestion)
    result = models.IntegerField(blank=True, null=True)
    start_time = models.DateTimeField(blank=True)
    end_time = models.DateTimeField(blank=True)