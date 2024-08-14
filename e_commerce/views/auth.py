from django.shortcuts import render
from e_commerce.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect

def login_page(request):
    if request.method=='POST':
        form=LoginForm(request.POST)
        if form.is_valid():
            username=form.cleaned_data.get('username')
            password=form.cleaned_data.get('password')
            user=authenticate(request, username=username, password=password)
            if user:
                login(request, user)
                return redirect('customer_list')
            else:
                messages.error(request, 'Invalid username or password')

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