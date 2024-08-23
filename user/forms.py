from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from django import forms
from user.models import CustomUser
from config.settings import EMAIL_DEFAULT_SENDER
from django.core.validators import validate_email


class CustomUserCreationForm(UserCreationForm):

    class Meta:
        model = CustomUser
        fields = ('email',)

class CustomUserChangeForm(UserChangeForm):

    class Meta:
        model = CustomUser
        fields = ('email',)


class LoginForm(forms.Form):
    email=forms.EmailField()
    password=forms.CharField()

    def clean_email(self):
        email=self.data.get('email')
        if not CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError(f'The user has not been found')
        return email


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, label='Confirm Password')

    class Meta:
        model = CustomUser
        fields = ('email', 'password', 'username')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if CustomUser.objects.filter(email=email).exists():
            raise forms.ValidationError('This email already exists')
        return email
    
    def clean(self):
        cleaned_data = super().clean()  # Call the parent's clean method
        password = cleaned_data.get('password')
        confirm_password = cleaned_data.get('confirm_password')
    
        if password and confirm_password and password != confirm_password:
            self.add_error('confirm_password', 'Passwords do not match')
    
        return cleaned_data  # Return all cleaned data


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password'])  # Use set_password to hash the password
        if commit:
            user.save()
        return user

class SendEmailForm(forms.Form):
    subject=forms.CharField(max_length=110)
    message=forms.CharField(widget=forms.Textarea)
    # sender=forms.EmailField()#EMAIL_DEFAULT_SENDER
    recipient_list=forms.EmailField()

class MultiEmailField(forms.Field):
    def to_python(self, value):
        """Normalize data to a list of strings."""
        # Return an empty list if no input was given.
        if not value:
            return []
        return value.split(",")

    def validate(self, value):
        """Check if value consists only of valid emails."""
        # Use the parent's handling of required fields, etc.
        super().validate(value)
        for email in value:
            validate_email(email)

class SendEmailForm(forms.Form):
    subject=forms.CharField(max_length=110)
    message=forms.CharField(widget=forms.Textarea)
    # sender=forms.EmailField()#EMAIL_DEFAULT_SENDER
    recipient_list=MultiEmailField(widget=forms.Textarea)