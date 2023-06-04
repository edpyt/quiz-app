from django.contrib import admin
from quiz.models import Quiz, QuizAnswers


class QuizUsersPerformInLine(admin.TabularInline):
    model = QuizAnswers
    extra = 1
    max_num = 4
    
    

class QuizAdmin(admin.ModelAdmin):
    list_display = ('id', 'question')
    
    inlines = (QuizUsersPerformInLine,)
    
    def get_answers(self, obj):
        return list(obj.quiz_answers.all())
    
    
class QuizAnswerAdmin(admin.ModelAdmin):
    list_display = ('id', 'answer', 'quiz_fk')

admin.site.register(Quiz, QuizAdmin)
admin.site.register(QuizAnswers, QuizAnswerAdmin)