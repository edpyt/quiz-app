import uuid
from django.forms.models import model_to_dict
from django.urls import reverse
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken
from quiz.models import Quiz
from custom_user.models import User


class QuizTestCase(APITestCase):
    def setUp(self):
        user = User.objects.create_user(name='testuser1',
                                        password='testpass123')
        self.token = RefreshToken.for_user(user=user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + \
            str(self.token.access_token))
        
        self.quiz1 = Quiz.objects.create(title='testquiz1',
                                         question='testquiz_question1',
                                         answer='testquiz_answer1')
        
        self.quiz2 = Quiz.objects.create(title='testquiz2',
                                         question='testquiz_question2',
                                         answer='testquiz_answer2') 
    
    @staticmethod
    def response_data_formatter(response):
        result = []
        for data in response.data:
            data = dict(data)
            data['id'] = uuid.UUID(data['id'])
            result.append(data)
        return result
    
    def test_user_have_access_token(self):
        # just testing if len > 1 xD
        self.assertGreater(len(str(self.token.access_token)), 1)
    
    def test_quiz_list_view(self):
        url = reverse('quiz_list')
        response = self.client.get(url)
        response_data = self.response_data_formatter(response)
        
        expected_data = []  # !%$@
        for col in list(Quiz.objects.values(
            'id', 'quiz_answers', 'title', 'question'
        )):
            col['quiz_answers'] = []
            expected_data.append(col)
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response_data, expected_data)
    
    def test_quiz_detail_view(self):
        url_quiz2 = reverse('quiz_detail', kwargs={'pk':self.quiz2.pk})
        
        response = self.client.get(url_quiz2)
        
        response_data = {'id': str(self.quiz2.id),
                         'quiz_answers': [],
                         'title': self.quiz2.title,
                         'question': self.quiz2.question}
        
        self.assertEqual(response.status_code, 200)
        self.assertEqual(response.data, response_data)