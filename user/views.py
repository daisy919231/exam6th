from django.http import HttpResponse
from django.shortcuts import render
from config.settings import EMAIL_DEFAULT_SENDER
from django.views import View
from user.forms import SendEmailForm, RegisterForm
from django.core.mail import send_mail
from django.contrib.auth.views import LoginView
from django.contrib import messages
from django.urls import reverse_lazy
from django.views import generic
from user.models import CustomUser

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
    template_name='e_commerce/login.html'
    form_class=LoginForm

    # def get_success_url(self) -> str:
    #     return super().get_success_url()
    def get_success_url(self):
        return reverse_lazy('customer_list')
    
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
            # user = form.save(commit=False)
            # user.is_active = True
            # user.is_superuser = True 
            # user.is_staff = True 
            # # user.set_password(form.cleaned_data.get('password'))     
            # user.save()
            # send_mail(
            #     'User sucessfully registered',
            #     'Welcome to the website',
            #     EMAIL_DEFAULT_SENDER,
            #     [user.email],
            #     fail_silently=False
            #     )
            # login(request,userbackend='django.contrib.auth.backends.ModelBackend')
            # return redirect('customer_list')
#     else:
#         form = RegisterForm()

#     context = {
#         'form': form
#     }

#     return render(request, 'e_commerce/register.html', context)


# class RegisterPage(generic.CreateView):
#     # form_class = RegisterForm  ###CreateView does not need any modelFORM unlike FormView, so it is quite convenient, BUT not safe, cause it does not ask for confirm_password, is that okay?
#     #Yees, it is okay, because you can add #required to your frontend code, that is a nice alternative!
#     model=CustomUser
#     fields=('email', 'password')
#     success_url = reverse_lazy('login_page')
#     template_name = 'e_commerce/register.html'

class RegisterPage(generic.FormView):
    form_class=RegisterForm
    success_url=reverse_lazy('login_page')
    template_name='e_commerce/register.html'

    def form_valid(self, form):
        user = form.save(commit=False)
        user.is_active = True
        user.is_superuser = True 
        user.is_staff = True 
        user.set_password(form.cleaned_data.get('password'))     
        user.save()
        send_mail(
            'User sucessfully registered',
            'Welcome to the website',
            EMAIL_DEFAULT_SENDER,
            [user.email],
            fail_silently=False
            )
        login(self.request,user, backend='django.contrib.auth.backends.ModelBackend')#,userbackend='django.contrib.auth.backends.ModelBackend') #Look, we don't need the userbackend here, because it is already config.settings: AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# ) So hopeffully, it will not an error again!
        return super().form_valid(form)
    
    # I did not include the login(user) but it was still working, but here is the explanation: If you didn't include the user parameter in the login function and it still seemed to work, and there are a few explanations:

# 1. **Default User Behavior**: If you're using a custom authentication backend or middleware that automatically handles user sessions, it might be managing user authentication in a way that doesn't require you to explicitly call login.

# 2. **Session Management**: If you're accessing a session where the user was already logged in, the session might still be valid. In this case, your application could appear to behave normally even without calling login.

# 3. **Error Handling**: If your code is structured in a way that handles errors gracefully or has fallback mechanisms, it might not show any immediate issues.

# 4. **Testing Environment**: If you were testing in a development environment where sessions persist, you might not have noticed the absence of the login call.

# 5. **Cascading Effects**: Some frameworks or libraries might have additional logic that automatically handles user states, making it seem like your code is functioning correctly.

# To ensure proper behavior and avoid any potential issues down the line, it's generally a good practice to include the user parameter when calling login. This makes your intentions clear and aligns with Django's authentication flow. If you have specific scenarios or configurations in mind, feel free to share them for more tailored insights! 


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
