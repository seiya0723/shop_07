from django.contrib.auth.forms import UserCreationForm

from django import forms
from .models import CustomUser, CustomUserAddress

class SignupForm(UserCreationForm):
    class Meta(UserCreationForm.Meta):
        model = CustomUser
        fields = ['username', "email", 'name', 'name_kana']

class NameEditForm(forms.ModelForm):
    class Meta:
        model = CustomUser
        fields = ['username', 'name', 'name_kana']

class AddressForm(forms.ModelForm):
    class Meta:
        model = CustomUserAddress
        fields = ['user_id', 'name', 'prefcode', 'address1', 'address2', 'address3', 'main']

# ↑と↓で内容が重複しているので、編集時にも流用してもよいのでは？

class AddressEditForm(forms.ModelForm):
    class Meta:
        model = CustomUserAddress
        fields = ['user_id', 'name', 'prefcode', 'address1', 'address2', 'address3', 'main']




