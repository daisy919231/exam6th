from django.contrib import admin
from django.urls import path
from user import views
urlpatterns = [
    path('admin/', admin.site.urls),
    path('login-page/', views.login_page, name='login_page' ),
    path('logout-page/', views.logout_page, name='logout_page' ),
    path('register-page/', views.register_page, name='register_page' ),

]