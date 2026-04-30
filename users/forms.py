from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User
from django import forms
from .models import User


class CustomUserCreationForm(UserCreationForm):
    # тут мы просто передаем код из UserProfileForm в поля fields
    class Meta(UserCreationForm.Meta):
        model = User

        fields = ('username', 'email', 'phone', 'city', 'avatar')


class UserProfileForm(forms.ModelForm):
    # это клас который генерирует html код к примеру в html написал {{ form.as_p }} потом django генирирует
    # огромный код и саподставляет код который написан в AbstractUser
    class Meta:
        model = User

        fields = ['username', 'avatar', 'phone']
