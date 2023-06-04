from django.contrib import admin
from django.urls import include, path

urlpatterns = [
    path('admin/', admin.site.urls),
    
    path('api/v1/quiz/', include('quiz.urls')),
    path('api/v1/user/', include('custom_user.urls')),
]
