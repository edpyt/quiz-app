from rest_framework.decorators import (api_view, authentication_classes,
                                       permission_classes)
from rest_framework.response import Response

from rest_framework.permissions import IsAuthenticated
from django.utils.translation import gettext
from .forms import SignUpForm

from .serializers import UserSerializer


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def me(request):
    user = request.user
    user_data = UserSerializer(user).data
    return Response(user_data)


@api_view(['POST'])
@authentication_classes([])
@permission_classes([])
def signup(request):
    data = request.data
    message = 'success'
    
    form = SignUpForm({
        'name': data.get('name'),
        'password1': data.get('password1'),
        'password2': data.get('password2')
    })
    
    if form.is_valid():
        user = form.save()
        user.save()
    else:
        message = 'Пользователь с таким именем уже существует!'
        
    return Response({'message': message})