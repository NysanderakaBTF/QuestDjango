from django.db import models


class QuestionAnswer(models.Model):
    text_ans = models.CharField(verbose_name='Answers', max_length=255)
    img_ans = models.ImageField(upload_to='img/%Y/%m/d/ans', blank=True, verbose_name='image')
    is_correct = models.BooleanField(default=False)
    question = models.ForeignKey('Question', on_delete=models.CASCADE)

    def __str__(self):
        return self.text_ans + str(self.is_correct)


class Question(models.Model):
    text_ques = models.TextField(verbose_name='Question')
    img_ques = models.ImageField(upload_to='img/%Y/%m/d/ques', blank=True, verbose_name='Image')
    test = models.ForeignKey('Test', on_delete=models.CASCADE)

    def __str__(self):
        return self.text_ques


class Test(models.Model):
    title = models.CharField(max_length=100, db_index=True)
    info = models.TextField(blank=True)

    def __str__(self):
        return self.title



