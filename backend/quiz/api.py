from django.http import Http404

from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from .models import Quiz, QuizAnswers
from .serializers import QuizSerializer


@api_view(['GET'])
def quiz_detail(request, pk):
    try:
        quiz_model = Quiz.objects.get(pk=pk)
        quiz_data = QuizSerializer(quiz_model).data 
    except Quiz.DoesNotExist:
        quiz_data = {'error': 'Quiz with id "%s" does not exist' % pk}
    
    return Response(quiz_data)


@api_view(['GET'])
@authentication_classes([])
@permission_classes([])
def quiz_list(request):
    quiz_model = Quiz.objects.prefetch_related('quiz_answers', 'users_perform',
                                               'users_completed').all()
    quiz_data = QuizSerializer(quiz_model, many=True).data
    return Response(quiz_data)

# Logic with quiz
@api_view(['POST'])
def quiz_answer(request):
    message = 'Correct'  # start value
    answer_id = request.data.get('answer_id')
    try:
        answer_obj = QuizAnswers.objects.get(id=answer_id)
    except QuizAnswers.DoesNotExist:
        raise Http404 # if something went wrong...
    else:
        quiz = answer_obj.quiz_fk
        
        if request.user in (users_completed:=quiz.users_completed).all():
            return Response({'message': 'Quiz already done!'})  # if user
                                                                # quiz
                                                                # completed
        if request.user not in (users_perform:=quiz.users_perform).all():
            users_perform.add(request.user)
        
        if answer_obj.answer != quiz.answer:
            message = 'Wrong'  # if quiz_answer is not right
        else:
            users_perform.remove(request.user)
            users_completed.add(request.user)    
    return Response({'message': message})
