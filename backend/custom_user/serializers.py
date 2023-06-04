from rest_framework import serializers
from django.contrib.auth import get_user_model


class UserSerializer(serializers.ModelSerializer):
    answered = serializers.SerializerMethodField()
    
    def get_answered(self, obj):
        return list(quiz.id for quiz in obj.quiz_users_completed.all())
    
    class Meta:
        model = get_user_model()
        fields = ('id', 'name', 'photo', 'answered')