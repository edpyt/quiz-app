from uuid import uuid4
from django.core.validators import MinLengthValidator
from django.db import models

from custom_user.models import User


class Quiz(models.Model):
    id = models.UUIDField(primary_key=True, default=uuid4, editable=False)
    
    question = models.CharField(max_length=255, blank=False)
    answer = models.CharField(max_length=255, blank=False)
    
    users_perform = models.ManyToManyField(User,
                                        related_name='quiz_users_perform')
    users_completed = models.ManyToManyField(User, blank=True,
                                        related_name='quiz_users_completed')
    
    date_created = models.DateTimeField(auto_now_add=True)
    
    def __str__(self) -> str:
        return self.question
    
    class Meta:
        ordering = ('-date_created',)
    
    
    
class QuizAnswers(models.Model):
    answer = models.CharField(max_length=255) 
    quiz_fk = models.ForeignKey('Quiz', on_delete=models.CASCADE, related_name='quiz_answers')
    
    def __str__(self) -> str:
        return self.answer