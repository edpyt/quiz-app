from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class SignUpForm(UserCreationForm):
    class Meta:
        model = get_user_model()
        fields = ('name', 'password1', 'password2')