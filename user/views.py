from django.shortcuts import render
from config.settings import EMAIL_DEFAULT_SENDER
from django.views import View
from user.forms import SendEmailForm
from django.core.mail import send_mail

# Create your views here.
from user.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
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
            send_mail(
                'User sucessfully registered',
                'Welcome to the website',
                EMAIL_DEFAULT_SENDER,
                [user.email],
                fail_silently=False
                )
            login(request,user)
            return redirect('customer_list')
    else:
        form = RegisterForm()

    context = {
        'form': form
    }

    return render(request, 'e_commerce/register.html', context)

class SendMail(View):
    sucessfully_sent=False
    def get(self,request,*args,**kwargs):
        form=SendEmailForm()
        context={
            'form':form,
            'sucessfully_sent':self.sucessfully_sent
        }
        return render(request,'user/send_email.html', context)

    def post(self, request,*args, **kwargs):
        form=SendEmailForm(request.POST)
        subject=form.cleaned_data['subject']
        message=form.cleaned_data['message']
        recipient_list=form.cleaned_data['recipient_list']
        send_mail(subject,message,EMAIL_DEFAULT_SENDER,[recipient_list], fail_silently=False)
        sucessfully_sent=True
        context={
            'form':form,
            'sucessfully_sent':sucessfully_sent
        }
        return render(request,'user/send_email.html', context)
