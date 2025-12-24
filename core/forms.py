from django import forms
from django.contrib.auth.forms import UserCreationForm,AuthenticationForm
from django.contrib.auth.models import User
from .models import SellerRating



class LoginForm(AuthenticationForm):

    username = forms.CharField(widget=forms.TextInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl', "placeholder": 'Enter Username'}))
    password = forms.CharField(widget=forms.PasswordInput(attrs={
        'class': 'w-full py-4 px-6 rounded-xl', "placeholder": 'Enter your password'}))
    
    
class SignupForm(UserCreationForm):
    email = forms.EmailField(
        widget=forms.EmailInput(attrs={
            'class': 'w-full py-4 px-6 rounded-xl',
            'placeholder': 'Enter your email address'  # Correction de "adress"
        })
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Personnalisation des placeholders et classes CSS
        self.fields['username'].widget.attrs.update({
            'class': 'w-full py-4 px-6 rounded-xl',
            'placeholder': 'Enter Username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'w-full py-4 px-6 rounded-xl',
            'placeholder': 'Enter your password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'w-full py-4 px-6 rounded-xl',
            'placeholder': 'Repeat your password'
        })

from .models import Profile
class ProfileForm(forms.ModelForm):
    class Meta:
        model = Profile
        fields = ['langue']





class SellerRatingForm(forms.ModelForm):
    class Meta:
        model = SellerRating
        fields = ['note', 'commentaire']
