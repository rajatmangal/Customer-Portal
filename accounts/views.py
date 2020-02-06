from django.shortcuts import render,redirect
from django.forms import inlineformset_factory
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.contrib.auth.decorators import login_required


from .models import *
from .forms import OrderForm, CreateUserForm
from .filters import OrderFilter
# Create your views here.


def registerPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        form = CreateUserForm()
        if request.method == 'POST':
            form = CreateUserForm(request.POST)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('login')

        context={'form': form}
        return render(request, 'accounts/register.html', context)


def loginPage(request):
    if request.user.is_authenticated:
        return redirect('home')
    else:
        if request.method == 'POST':
            username = request.POST.get('username') ##getting from names in login page
            password = request.POST.get('password')
            user = authenticate(request, username = username, password=password)
            if user is not None:
                login(request, user)
                return redirect('home')
            else:
                messages.info(request, 'Username or Password is incorrect.')
        context= {}
        return render(request, 'accounts/login.html', context)


def logoutUser(request):
    logout(request)
    return redirect('login')


@login_required(login_url='login')
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


@login_required(login_url='login')
def products(request):
    products = Product.objects.all()
    return render(request, 'accounts/products.html', {'products': products})


@login_required(login_url='login')
def customers(request, id):
    customer = Customer.objects.get(id=id)
    orders = customer.order_set.all();
    totalOrders = orders.count();
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
    context = {
        'customer': customer,
        'orders': orders,
        'totalOrders': totalOrders,
        'myFilter': myFilter
    }
    return render(request, 'accounts/customer.html', context)


@login_required(login_url='login')
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


@login_required(login_url='login')
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


@login_required(login_url='login')
def deleteOrder(request, id):
    order = Order.objects.get(id=id)
    if request.method == 'POST':
        order.delete()
        return redirect('/accounts')
    context = {'order':order}
    return render(request, 'accounts/delete.html', context)