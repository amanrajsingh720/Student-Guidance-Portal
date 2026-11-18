from django import forms
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError
from .models import StudentQuery


class StudentRegistrationForm(forms.ModelForm):
    """Simple student registration form: name, username, email, password, confirm password."""
    first_name = forms.CharField(
        max_length=50,
        required=True,
        label='Full Name',
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter your full name',
            'autofocus': True,
        })
    )
    username = forms.CharField(
        max_length=150,
        required=True,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Choose a username',
        })
    )
    email = forms.EmailField(
        required=True,
        label='Email Address',
        widget=forms.EmailInput(attrs={
            'class': 'form-control',
            'placeholder': 'name@example.com',
        })
    )
    password = forms.CharField(
        required=True,
        min_length=6,
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Enter password (min 6 characters)',
        })
    )
    confirm_password = forms.CharField(
        required=True,
        label='Confirm Password',
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Re-enter your password',
        })
    )

    class Meta:
        model = User
        fields = ['first_name', 'username', 'email']

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username__iexact=username).exists():
            raise ValidationError('This username is already taken. Please pick another one.')
        return username

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email__iexact=email).exists():
            raise ValidationError('An account with this email address already exists.')
        return email

    def clean(self):
        cleaned_data = super().clean()
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')

        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match. Please re-enter.')
        return cleaned_data

    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])
        if commit:
            user.save()
        return user


class StudentQueryForm(forms.ModelForm):
    """Simple form for a logged-in student to submit an Academic or Career question."""
    class Meta:
        model = StudentQuery
        fields = ['category', 'question']
        widgets = {
            'category': forms.Select(attrs={
                'class': 'form-select',
            }),
            'question': forms.Textarea(attrs={
                'class': 'form-control',
                'rows': 4,
                'placeholder': 'Type your question clearly here (e.g. How do I start preparing for GATE in 3rd year?)...',
            }),
        }

    def clean_question(self):
        question = (self.cleaned_data.get('question') or '').strip()
        if not question:
            raise ValidationError('Question cannot be empty. Please enter your question.')
        if len(question) < 10:
            raise ValidationError('Please provide a little more detail (at least 10 characters).')
        return question
