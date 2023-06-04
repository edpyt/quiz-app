from django.test import TestCase
from quiz.models import Quiz
from custom_user.models import User


class QuizTestCase(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(name='testuser')
        self.quiz1 = Quiz.objects.create(title='test1', question='test1')
        self.quiz2 = Quiz.objects.create(title='test2', question='test2')
    
    def test_user_can_take_a_quiz(self):
        self.user.quiz_users_perform.add(self.quiz1)
        self.user.quiz_users_perform.add(self.quiz2)
        
        self.assertEqual(list(self.user.quiz_users_perform.all()),
                         [self.quiz1, self.quiz2])
    
    def test_quiz_can_be_a_done(self):
        self.quiz1.users_completed.add(self.user)
        
        self.assertEqual(self.quiz1.users_completed.last(),
                         self.user)