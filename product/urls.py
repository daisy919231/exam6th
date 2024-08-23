from django.urls import path
from product import views
urlpatterns = [
    path('product-list/', views.product_list, name='product_list'),#ProductListView.as_view(), name='product_list'),
    path('product-create/', views.ProductCreateView.as_view(), name='create_product'),
    path('product-detail/<int:pk>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product-update/<int:pk>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product-delete/<int:pk>/', views.ProductDetailView.as_view(), name='delete_product'),
]