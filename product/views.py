from django.shortcuts import render, redirect, get_object_or_404
from product.models import Product, Comment, Attribute
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
from django.views import View
from product.forms import ProductForm
from django.views.generic import ListView, DeleteView, DetailView, UpdateView, CreateView
from django.urls import reverse
# Create your views here.
# def product_list(request):
#     products=Product.objects.all()
#     star_list=Comment.objects.all()
#     page_num=request.GET.get('page', 1)
#     paginator=Paginator(products,2)
#     try:
#         page_obj = paginator.page(page_num)
#     except PageNotAnInteger:
#         # if page is not an integer, deliver the first page
#         page_obj = paginator.page(1)
#     except EmptyPage:
#         # if the page is out of range, deliver the last page
#         page_obj = paginator.page(paginator.num_pages)
        
#     context={

#         'star_list':star_list,
#         'products':page_obj,
#     }

#     return render(request, 'product/product_list.html', context)

def product_list(request):
    products = Product.objects.all()
    # star_list = Comment.objects.filter(product__in=products)  # Assuming there's a relation
    page_num = request.GET.get('page', 1)
    paginator = Paginator(products, 2)
    star_list=[1,2,3,4,5]

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'star_list': star_list,
        'products': page_obj,
    }

    return render(request, 'product/product_list.html', context)

# class ProductListView(View):
#     def get(self,request, *args, **kwargs):
#         products = Product.objects.all()
#         star_list = Comment.objects.filter(product__in=products)  # Assuming there's a relation
#         page_num = request.GET.get('page', 1)
#         paginator = Paginator(products, 2)

#         try:
#             page_obj = paginator.page(page_num)
#         except PageNotAnInteger:
#             page_obj = paginator.page(1)
#         except EmptyPage:
#             page_obj = paginator.page(paginator.num_pages)

#         context = {
#             'star_list': star_list,
#             'products': page_obj,
#         }
#         return render (request, 'product/product_list.html', context)
    
# class ProductCreateView(View):
#     def get(self,request, *args, **kwargs):
#         form=ProductForm()
#         context={
#             'form':form,
#         }
#         return render(request,'product/add_product.html',context)
#     def post(self, request, *args, **kwargs):
#         form=ProductForm(data=request.POST)
#         if form.is_valid():
#             product=form.save()
#             return redirect('product_detail', id=product.id)
        
#         return self.get(request)
    
# class ProductDetailView(View):
#     def get(self, request, product_id, *args, **kwargs):
#         product=get_object_or_404(Product, id=product_id)
#         context={
#             'product':product
#         }
#         return render(request, 'product/product_detail.html', context)
    
# class ProductUpdateView(View):
#     def get(self,request, product_id, *args, **kwargs):
#         product=get_object_or_404(Product,id=product_id)
#         context={
#             'product':product,
#             'form':ProductForm(instance=product)
#         }
#         return render (request, 'product/edit_product.html', context)
#     def post(self, request, product_id, *args, **kwargs ):
#         product=get_object_or_404(Product, id=product_id)
#         form = ProductForm(instance=product, data=request.POST)
#         if form.is_valid():
#             form.save()
#             return redirect('product_detail',id=product.id)

#         return self.get(request,product_id)

# class ProductDeleteView(View):
#     def get(self, request, product_id, *args, **kwargs):
#         product = get_object_or_404(Product, id=product_id)
#         if product:
#             product.delete()
#             return redirect('product_list')
    
#         return render(request, 'product/product_list.html', {'product':product})
    
# class ProductListView(ListView):
#     model=Product
#     context_object_name='products'

class ProductCreateView(CreateView):
    model=Product
    context_object_name='product'
    fields=('name','description', 'price', 'category', 'discount','quantity','slug')
    template_name='product/add_product.html'

class ProductDetailView(DetailView):
    model=Product
    context_object_name='product'

class ProductUpdateView(UpdateView):
    model=Product
    context_object_name='product'
    fields=('name','description', 'price', 'category', 'discount','quantity','slug')
    template_name='product/edit_product.html'
    def get_success_url(self):
        return reverse('product_detail', kwargs={'pk': self.object.pk})

class ProductDeleteView(DeleteView):
    model=Product
    context_object_name='product'
    success_url='/'