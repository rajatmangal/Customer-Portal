from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from .models import *
from .forms import OrderForm
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


def createOrder(request, id):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product','status'),extra = 10)
    customer = Customer.objects.get(id=id)
    #form = OrderForm(initial={'customer': customer})
    formSet = OrderFormSet(queryset=Order.objects.none(), instance = customer)
    if request.method == 'POST':
        #form = OrderForm(request.POST)
        formSet = OrderFormSet(request.POST, instance=customer)
        if formSet.is_valid():
            formSet.save()
            return redirect('/accounts')

    context = {'form': formSet}
    return render(request, 'accounts/orders_form.html', context)


def updateOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        form = OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/accounts')
    form = OrderForm(instance=order)
    context = {'form': form}
    return render(request, 'accounts/orders_form.html', context)


def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/accounts')
    context = {'order':order}
    return render(request, 'accounts/delete.html', context)