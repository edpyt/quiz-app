from django.test import TestCase

from quiz.models import Quiz


class QuizAnswerTest(TestCase):
    def setUp(self):
        self.quiz = Quiz.objects.create(title='testquiz',
                                        answer='')