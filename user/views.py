from django.shortcuts import render

# Create your views here.
from user.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect

def login_page(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            email=form.cleaned_data.get('email')
            password=form.cleaned_data.get('password')
            user=authenticate(request, email=email, password=password)
            if user:
                login(request, user)
                return redirect('customer_list')
            else:
                messages.error(request, 'Invalid email or password')

    return render(request,'e_commerce/login.html', {'form': 'form'})

def logout_page(request):
    logout(request)
    return redirect('customer_list')

def register_page(request):
    if request.method == 'POST':
        form = RegisterForm(request.POST)
        if form.is_valid():
            user = form.save(commit=False)
            user.is_active = True
            user.is_superuser = True 
            user.is_staff = True 
            # user.set_password(form.cleaned_data.get('password'))     
            user.save()
            login(request,user)
            return redirect('customer_list')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'e_commerce/register.html', context)