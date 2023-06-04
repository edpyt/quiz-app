from django.contrib import admin
from custom_user.models import User
from quiz.models import Quiz


class QuizCompletedInLine(admin.TabularInline):
    model = Quiz.users_completed.through
    extra = 1
    verbose_name = 'Quiz Complete'
    verbose_name_plural = 'Quiz Completed'
    
    
class QuizPerformInLine(admin.TabularInline):
    model = Quiz.users_perform.through
    extra = 1
    verbose_name = 'Quiz Perform'
    verbose_name_plural = 'Quiz Performs'


class UserAdmin(admin.ModelAdmin):
    inlines = (QuizPerformInLine, QuizCompletedInLine,)


admin.site.register(User, UserAdmin)