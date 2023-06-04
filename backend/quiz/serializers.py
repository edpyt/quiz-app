from rest_framework import serializers

from quiz.models import Quiz, QuizAnswers


class QuizAnswerSerializer(serializers.ModelSerializer):
    class Meta:
        model = QuizAnswers
        fields = ('id', 'answer',)


class QuizSerializer(serializers.ModelSerializer):
    quiz_answers = QuizAnswerSerializer(read_only=True, many=True)
     
    class Meta:
        model = Quiz
        fields = ('id', 'question', 'quiz_answers')