from django.urls import path
from user import views
from django.contrib.auth.views import LogoutView
urlpatterns = [
    path('login-page/', views.MyLoginView.as_view(), name='login_page' ),
    path('logout-page/', LogoutView.as_view(next_page='customer_list'), name='logout_page' ),
    path('register-page/', views.RegisterPage.as_view(), name='register_page' ),
    path('send_email/', views.SendMail.as_view(), name='send_email'),

]