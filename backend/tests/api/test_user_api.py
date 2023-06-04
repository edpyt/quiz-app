from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework.test import APITestCase
from rest_framework_simplejwt.tokens import RefreshToken

from quiz.models import Quiz, QuizAnswers


class UserAPITest(APITestCase):
    def setUp(self):
        self.user = get_user_model()
        
        self.quiz = Quiz.objects.create(title='testquiz',
                                        question='1+1?',
                                        answer='2')
        list(QuizAnswers.objects.create(answer=str(i), quiz_fk=self.quiz)
             for i in range(4))
        
        quiz_user = self.user.objects.create_user(name='quiz_uiser',
                                                  password='testpass123')
        self.token = RefreshToken.for_user(user=quiz_user)
        self.client.credentials(HTTP_AUTHORIZATION='Bearer ' + \
            str(self.token.access_token))
        
        
    def test_user_can_sign_up(self):
        User = self.user
        user_data = {'name': 'testUsername',
                    'password1': 'testpassword123',
                    'password2': 'testpassword123'}
        url = reverse('signup')
        response = self.client.post(url, user_data, format='json')

        self.assertEqual(response.data, {'message': 'success'})
        self.assertEqual(User.objects.count(), 2)
        self.assertEqual(User.objects.latest('id').name, 'testUsername')
        
        
    def test_user_can_login(self):
        User = self.user
        
        User.objects.create_user(name='testuser', password='testpass123')
        
        url = reverse('token_obtain')
        response = self.client.post(url, {'name': 'testuser',
                                          'password': 'testpass123'},
                                    format='json')
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'refresh')
        self.assertContains(response, 'access')
        
    def test_user_can_answer_quiz_correct(self):
        url = reverse('quiz_answer')
        correct_response = self.client.post(url, {'answer_id': 3},
                                            format='json')
                
        self.assertEqual(correct_response.status_code, 200)
        self.assertEqual(correct_response.data, {'message': 'Correct'})
        
    def test_user_can_answer_quiz_wrong(self):
        url = reverse('quiz_answer')
        wrong_response = self.client.post(url, {'answer_id': 1},
                                    format='json')
        
        self.assertEqual(wrong_response.status_code, 200)
        self.assertEqual(wrong_response.data, {'message': 'Wrong'})
        
    def test_user_answer_exception(self):
        url = reverse('quiz_answer')
        error_response = self.client.post(url, {'answer_id': 231321},
                            format='json')
        
        self.assertEqual(error_response.status_code, 404)