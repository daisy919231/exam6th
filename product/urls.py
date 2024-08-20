from django.urls import path
from product import views
urlpatterns = [
    path('product-list/', views.ProductListView.as_view(), name='product_list'),
    path('product-create/', views.ProductCreateView.as_view(), name='create_product'),
    path('product-detail/<int:product_id>/', views.ProductDetailView.as_view(), name='product_detail'),
    path('product-update/<int:product_id>/', views.ProductUpdateView.as_view(), name='update_product'),
    path('product-delete/<int:product_id>/', views.ProductDetailView.as_view(), name='delete_product_'),
]