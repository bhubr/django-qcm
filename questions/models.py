# Create your models here.
from django.db import models
from django.contrib.auth.models import User

class Question(models.Model):
    question = models.TextField(default='')

    def __str__(self):
        return self.question

class Answer(models.Model):
    question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, default=1)
    text = models.TextField(default='')
    correct = models.NullBooleanField()

    def __str__(self):
        return self.text
#     question = models.ForeignKey(Question, related_name='answers', on_delete=models.CASCADE, default=1)
#     answer = models.TextField(default='')

