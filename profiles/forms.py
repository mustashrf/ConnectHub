from django import forms
from .models import Profile
from allauth.account.forms import SignupForm
from django.contrib.auth import get_user_model

class ProfileModelForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ('first_name', 'last_name', 'bio', 'avatar')

class CustomSignupForm(SignupForm):
    first_name = forms.CharField(max_length=30, label='First Name')
    last_name = forms.CharField(max_length=30, label='Last Name')

    class Meta:
        field_order = ['email', 'first_name', 'last_name']
        model = get_user_model()
        fields = ['first_name', 'last_name', 'email']

    def save(self, request):
        user = super(CustomSignupForm, self).save(request)
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        user.save()
        return user
