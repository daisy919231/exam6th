from django.shortcuts import render
from config.settings import EMAIL_DEFAULT_SENDER
from django.views import View
from user.forms import SendEmailForm, RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic

# Create your views here.
from user.forms import LoginForm, RegisterForm
from django.contrib.auth import authenticate, login, logout
from django.contrib import messages
from django.shortcuts import redirect
from django.core.mail import send_mail
# def login_page(request):
#     if request.method=='POST':
#         form=LoginForm(request.POST)
#         if form.is_valid():
#             email=form.cleaned_data.get('email')
#             password=form.cleaned_data.get('password')
#             user=authenticate(request, email=email, password=password)
#             if user:
#                 login(request, user)
#                 return redirect('customer_list')
#             else:
#                 messages.error(request, 'Invalid email or password')

#     return render(request,'e_commerce/login.html', {'form': 'form'})

class MyLoginView(LoginView):
    redirect_authenticated_user = True

    # def get_success_url(self) -> str:
    #     return super().get_success_url()
    def get_success_url(self):
        return reverse_lazy('customers_list')
    
    def form_invalid(self, form):
        messages.error(self.request,'Invalid username or password')
        return self.render_to_response(self.get_context_data(form=form))






# def logout_page(request):
#     logout(request)
#     return redirect('customer_list')

# def register_page(request):
#     if request.method == 'POST':
#         form = RegisterForm(request.POST)
#         if form.is_valid():
#             user = form.save(commit=False)
#             user.is_active = True
#             user.is_superuser = True 
#             user.is_staff = True 
#             # user.set_password(form.cleaned_data.get('password'))     
#             user.save()
#             send_mail(
#                 'User sucessfully registered',
#                 'Welcome to the website',
#                 EMAIL_DEFAULT_SENDER,
#                 [user.email],
#                 fail_silently=False
#                 )
#             login(request,userbackend='django.contrib.auth.backends.ModelBackend')
#             return redirect('customer_list')
#     else:
#         form = RegisterForm()

#     context = {
#         'form': form
#     }

#     return render(request, 'e_commerce/register.html', context)


class RegisterPage(generic.CreateView):
    form_class = RegisterForm
    success_url = reverse_lazy('login_page')
    template_name = 'register.html'




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
        if form.is_valid():
            subject=form.cleaned_data['subject']
            message=form.cleaned_data['message']
            recipient_list=form.cleaned_data['recipient_list']
            send_mail(subject,message,EMAIL_DEFAULT_SENDER, recipient_list, fail_silently=False)
            self.sucessfully_sent=True
        context={
            'form':form,
            'sucessfully_sent':self.sucessfully_sent
            # Look, we don't have to define sucessfully sent=True in the html file, we should just say succesfully_sent as false in if part and give the form, and 
            # in else part we will give a sucess message!
        }
        return render(request,'user/send_email.html', context)
