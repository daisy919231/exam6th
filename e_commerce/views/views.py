from django.shortcuts import render, get_object_or_404, redirect
from e_commerce.models import Customer
from django.db.models import Q
from e_commerce.forms import CustomerForm
from typing import Optional
from django.core.paginator import Paginator, EmptyPage, PageNotAnInteger
# Create your views here.
def customer_list(request):
    customers=Customer.objects.all()
    joined_date = request.GET.get('joined_date')
    address = request.GET.get('address')
    search = request.GET.get('q')
    # p=Paginator(customers,1)
    # page_number=request.GET.get('page')
    # try:
    #     page_obj=p.get_page(page_number)
    # except PageNotAnInteger:
    #     page_obj=p.page(1)
    # except EmptyPage:
    #     page_obj=p.page(p.num_pages)

    if joined_date:
        customers = customers.filter(created_at__date=joined_date)


    if address:
        customers = customers.filter(bill_address__icontains=address)


    if search:
        customers = customers.filter(Q(first_name__icontains=search) |Q(last_name__icontains=search) |Q(bill_address__icontains=search)).distinct()

    context = {
        'customers': customers,
        'joined_date': joined_date,
        'address': address,
        'search': search,
        # 'page_obj':page_obj,
    }
    
    return render(request, 'e_commerce/customer_list.html', context)


def customer_detail(request,customer_slug:Optional[str]=None):
    customer=Customer.objects.get(slug=customer_slug)
    context={
        'customer':customer
    }
    return render(request, 'e_commerce/customer_detail.html', context)

def add_customer(request):
    form=CustomerForm()
    if request.method == 'POST':
        form = CustomerForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('customer_list')

    context = {
        'form': form
    }

    return render(request, 'e_commerce/add_customer.html', context)

def edit_customer(request, customer_slug:Optional[str]=None):
    customer=get_object_or_404(Customer, slug=customer_slug)
    form=CustomerForm(instance=customer)# instance gets the already created and filled form, not an empty form
    if request.method=='POST':
        form=CustomerForm(request.POST, request.FILES, instance=customer)
        if form.is_valid():
            form.save()
            return redirect('customer_detail', customer_slug)
    context={
        'form': form
        }
    return render(request,'e_commerce/edit_customer.html', context)
    

def delete_customer(request, customer_slug:Optional[str]=None):
    customer=get_object_or_404(Customer, slug=customer_slug)
    if customer:
        customer.delete()
        return redirect('customer_list')
    
 