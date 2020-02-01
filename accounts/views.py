from django.shortcuts import render
from django.http import HttpResponse
from .models import *
# Create your views here.


def home(request):
    order = Order.objects.all();
    customers = Customer.objects.all();
    totalOrders = len(Order.objects.all())
    ordersDeivered = len(Order.objects.filter(status='Delivered'))
    ordersPending = len(Order.objects.filter(status='Pending'))
    context = {
        'order': order,
        'customers': customers,
        'totalOrders': totalOrders,
        'ordersDelivered': ordersDeivered,
        'ordersPending': ordersPending
    }
    return render(request, 'accounts/dashboard.html', context)


def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


def customers(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all();
    totalOrders = orders.count();
    context = {
        'customer': customer,
        'orders': orders,
        'totalOrders': totalOrders
    }
    return render(request, 'accounts/customer.html', context)
