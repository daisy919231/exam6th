from django.urls import path
from books import views

urlpatterns=[
    path('sample/', views.sample, name='sample'),
]