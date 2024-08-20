from django.shortcuts import render
from product.models import Product, Comment
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
# def product_list(request):
#     products=Product.objects.all()
#     comment_r=Comment.objects.all()
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

#         'comment_r':comment_r,
#         'products':page_obj,
#     }

#     return render(request, 'product/product_list.html', context)

def product_list(request):
    products = Product.objects.all()
    comment_r = Comment.objects.filter(product__in=products)  # Assuming there's a relation
    page_num = request.GET.get('page', 1)
    paginator = Paginator(products, 2)

    try:
        page_obj = paginator.page(page_num)
    except PageNotAnInteger:
        page_obj = paginator.page(1)
    except EmptyPage:
        page_obj = paginator.page(paginator.num_pages)

    context = {
        'comment_r': comment_r,
        'products': page_obj,
    }

    return render(request, 'product/product_list.html', context)
