from django.db import models


class Survey(models.Model):
    objects = models.Manager()
    title = models.CharField(max_length=128)
    start_date = models.DateField(auto_now_add=True)
    end_date = models.DateField()
    description = models.CharField(max_length=2048, default="No description")


class Question(models.Model):
    objects = models.Manager()
    survey = models.ForeignKey(Survey, related_name="questions", on_delete=models.CASCADE)
    text = models.CharField(max_length=256)

    QUESTION_TYPE_CHOICES = [
        ("PT", "Plain text"),
        ("SC", "Single choice"),
        ("MC", "Multiply choice"),
    ]

    question_type = models.CharField(max_length=2, choices=QUESTION_TYPE_CHOICES)


class QuestionAnswer(models.Model):
    objects = models.Manager()
    question = models.ForeignKey(Question, related_name="question_answers", on_delete=models.CASCADE)
    text = models.CharField(max_length=128)


class UserAnswersHolder(models.Model):
    objects = models.Manager()
    survey = models.ForeignKey(Survey, on_delete=models.CASCADE)
    user_ID = models.PositiveIntegerField()


class UserAnswer(models.Model):
    objects = models.Manager()
    user_answers_holder = models.ForeignKey(UserAnswersHolder, related_name="answers", on_delete=models.CASCADE)
    question = models.ForeignKey(Question, on_delete=models.CASCADE)
    answer = models.CharField(max_length=1024)
