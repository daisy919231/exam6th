from django import forms
from e_commerce.models import Customer
from django.contrib.auth.models import User

class CustomerForm(forms.ModelForm):
    class Meta:
        model = Customer
        fields = ['first_name', 'last_name', 'email', 'phone_num', 'bill_address', 'image']

    def clean_phone_num(self):
        phone_num = self.cleaned_data.get('phone_num')
        if Customer.objects.filter(phone_num=phone_num).exists():
            raise forms.ValidationError('The customer has already been defined.')
        return phone_num

    
class LoginForm(forms.Form):
    username=forms.CharField()
    password=forms.CharField()

    def clean_username(self):
        username=self.data.get('username')
        if not User.objects.filter(username=username).exists():
            raise forms.ValidationError(f'The user has not been found')
        return username


class RegisterForm(forms.ModelForm):
    confirm_password = forms.CharField(max_length=255, label='Confirm Password')

    class Meta:
        model = User
        fields = ('username', 'password', 'email')

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if User.objects.filter(username=username).exists():
            raise forms.ValidationError('This username already exists')
        return username
    
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

