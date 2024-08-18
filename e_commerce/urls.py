from django.contrib import admin
from django.urls import path
from e_commerce.views import views, auth

urlpatterns=[
    path('customer-list/', views.customer_list, name='customer_list'),
    path('customer-detail/<slug:customer_slug>/', views.customer_detail, name='customer_detail'),
    path('add-customer/', views.add_customer, name="add_customer"),
    path('delete-customer/<slug:customer_slug>/',views.delete_customer, name='delete_customer'),
    path('edit-customer/<slug:customer_slug>/', views.edit_customer, name='edit_customer'),
    

]