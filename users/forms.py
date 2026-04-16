from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from .models import User  # Или твоя кастомная модель пользователя

class CustomUserCreationForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = User
        fields = ('username', 'email', 'phone', 'city', 'avatar')

class UserProfileForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'avatar', 'phone']

