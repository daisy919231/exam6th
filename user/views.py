import datetime
import csv
import json
import pandas as pd

from user.tokens import account_activation_token
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


from django.contrib.sites.shortcuts import get_current_site
from django.utils.encoding import force_bytes, force_str
from django.utils.http import urlsafe_base64_encode, urlsafe_base64_decode
from django.template.loader import render_to_string

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
        user.is_active = False
        user.is_superuser = True 
        user.is_staff = True 
        user.set_password(form.cleaned_data.get('password'))     
        user.save()
        current_site = get_current_site(self.request)
        mail_subject = 'Activate your blog account.'
        message = render_to_string('user/acc_active_email.html', {
            'user': user,
            'domain': current_site.domain,
            'uid':urlsafe_base64_encode(force_bytes(user.pk)),
            # 'uid':urlsafe_base64_encode(force_bytes(user.pk)).decode(),
            'token':account_activation_token.make_token(user),
        })
        send_mail(
            mail_subject,
            message,
            EMAIL_DEFAULT_SENDER,
            [user.email],
            fail_silently=False
            )
       
        response = super().form_valid(form)

       
        return HttpResponse('Please confirm your email address to complete the registration.')
    

    # user = request.user
    #         email = request.user.email
    #         subject = "Verify Email"
    #         message = render_to_string('user/verify_email_message.html', {
    #             'request': request,
    #             'user': user,
    #             'domain': current_site.domain,
    #             'uid':urlsafe_base64_encode(force_bytes(user.pk)),
    #             'token':account_activation_token.make_token(user),
    #         })
    #         email = EmailMessage(
    #             subject, message, to=[email]
    #         )
    #         email.content_subtype = 'html'
    #         email.send()
    # I could do the code above using EmailMessage class, could give a content_subtype='html', but you could just not write and doc html things and be not writing this piece of code!    # 

def activate(request, uidb64, token):
    try:
        uid = force_str(urlsafe_base64_decode(uidb64))
        user = CustomUser.objects.get(pk=uid)
    except(TypeError, ValueError, OverflowError, CustomUser.DoesNotExist):
        user = None
    if user is not None and account_activation_token.check_token(user, token):
        user.is_active = True
        user.save()
        login(request, user, backend='django.contrib.auth.backends.ModelBackend')
        # return redirect('home')
        return HttpResponse('Thank you for your email confirmation. Now you can login your account.')
    else:
        return HttpResponse('Activation link is invalid!')
    
        
        # login(self.request,user, backend='django.contrib.auth.backends.ModelBackend') ###userbackend='django.contrib.auth.backends.ModelBackend') #Look, we don't need the userbackend here, because it is already config.settings: AUTHENTICATION_BACKENDS = (
#     'social_core.backends.google.GoogleOAuth2',
#     'django.contrib.auth.backends.ModelBackend',
# ) So hopefully, it will not return  an error again!

        
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
    
# class DatetimeEncoder(json.JSONEncoder):
#     def default(self, obj):
#         try:
#             return super().default(obj)
#         except TypeError:
#             return str(obj)

def default(o):
    if isinstance(o, (datetime.date, datetime.datetime)):
        return o.isoformat()

    

def export_format_data(request):
    date=datetime.datetime.now().strftime("%m/%d/%Y")
    format=request.GET.get('format')
    if format=='csv':
        meta=CustomUser._meta
        field_names=[field.name for field in meta.fields]
        response=HttpResponse(content_type='text/csv')
        response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.csv'
        writer=csv.writer(response)
        writer.writerow(field_names)
        for obj in CustomUser.objects.all():
            writer.writerow([getattr(obj,field)for field in field_names])
    
    elif format=='json':
        response=HttpResponse(content_type='application/json')
        data=list(CustomUser.objects.all().values())
        # response.write(json.dumps(data, indent=4, sort_keys=True, default=str)) FIRST  VERSION
        # response.write(json.dumps(data, cls=DatetimeEncoder))
        response.write(json.dumps(data, indent=4, default=default))
        response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.json'
        
    elif format=='xlsx':
        users=CustomUser.objects.all().values()
        df=pd.DataFrame(list(users))
        response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
        response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.xlsx'
        df.assign(**{col: df[col].dt.tz_localize(None) for col in df.columns if hasattr(df[col], "dt")}).to_excel(response, index=False, engine='openpyxl')
        # df.to_excel(response, index=False, engine='openpyxl')

    return response

class ExportFormatData(View):
    
    
    def get(self, request, *args, **kwargs):
        date=datetime.datetime.now().strftime("%m/%d/%Y")
        format=request.GET.get('format')


        if format=='csv':
            meta=CustomUser._meta
            field_names=[field.name for field in meta.fields]
            response=HttpResponse(content_type='text/csv')
            response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.csv'
            writer=csv.writer(response)
            writer.writerow(field_names)
            for obj in CustomUser.objects.all():
                writer.writerow([getattr(obj,field)for field in field_names])
    
        elif format=='json':
            response=HttpResponse(content_type='application/json')
            data=list(CustomUser.objects.all().values())
            # response.write(json.dumps(data, indent=4, sort_keys=True, default=str)) FIRST  VERSION
            # response.write(json.dumps(data, cls=DatetimeEncoder))
            response.write(json.dumps(data, indent=4, default=default))
            response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.json'
            
        elif format=='xlsx':
            users=CustomUser.objects.all().values()
            df=pd.DataFrame(list(users))
            response=HttpResponse(content_type='application/vnd.openxmlformats-officedocument.spreadsheetml.sheet')
            response['Content-Disposition']=f'attachment; filename={CustomUser._meta.object_name}-{date}.xlsx'
            df.assign(**{col: df[col].dt.tz_localize(None) for col in df.columns if hasattr(df[col], "dt")}).to_excel(response, index=False, engine='openpyxl')
            # df.to_excel(response, index=False, engine='openpyxl')

        return response

