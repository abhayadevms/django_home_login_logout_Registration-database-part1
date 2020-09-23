from django.shortcuts import render, redirect
from django.http import HttpResponse
from .models import Product, Order, Customer
from .forms import OrderForm, CreateUserForm
from django.forms import inlineformset_factory
from .filters import orderfiter
#flash message
from django.contrib import messages

from django.contrib.auth import authenticate, login,logout
from django.contrib.auth import authenticate, login as dj_login
from django.contrib.auth.forms import UserCreationForm

from django.contrib.auth.decorators import login_required

# Create your views here.
def registration(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:

        form = CreateUserForm()
        #flash message


        if request.method =="POST":
            form = CreateUserForm(request.POST)
            print(form)
            if form.is_valid():
                form.save()
                user = form.cleaned_data.get('username')
                messages.success(request, 'Account was created for ' + user)
                return redirect('accounts:login')

    context={
        'form':form,
    }
    return render(request,'accounts/registration.html', context)

def login(request):
    if request.user.is_authenticated:
        return redirect('accounts:home')
    else:


        if request.method == 'POST':
            username = request.POST.get('username')
            password = request.POST.get('password')
            user = authenticate(request, username=username, password=password)

            if user is not None:
                dj_login(request, user)
                return redirect('accounts:home')
            else:
                messages.info(request, 'Username or Password is incorrect')


        return render(request,'accounts/login_page.html')


def logoutUser(request):
    logout(request)
    return redirect('accounts:login')


@login_required(login_url='accounts:login')
def home(request):
    orders =Order.objects.all()
    customers = Customer.objects.all()

    total_customers = customers.count()
    total_orders =orders.count()
    delivered =orders.filter(status ='Delivered').count()
    pending =orders.filter(status ='pending').count()

    context ={
        'orders': orders,
        'customers': customers,
        'total_customers':total_customers,
        'total_orders':total_orders,
        'delivered':delivered,
        'pending':pending,

    }



    return render(request, 'accounts/dasboard.html',context)

@login_required(login_url='accounts:login')
def product(request):
    product = Product.objects.all()

    return render(request, 'accounts/products.html', {'products': product})
@login_required(login_url='accounts:login')
def customer(request, pk_test):
    customer = Customer.objects.get(id = pk_test)
    orders = customer.order_set.all()
    orders_count =orders.count()

    #filter
    myfilter = orderfiter(request.GET, queryset=orders)
    orders = myfilter.qs
    context ={
        'customer':customer,
        'orders':orders,
        'orders_count':orders_count,
        'myfilter':myfilter,
    }
    return render(request, 'accounts/customer.html', context)

@login_required(login_url='accounts:login')
def createOrder(request, pk_test):
    OrderFormSet = inlineformset_factory(Customer, Order, fields=('product', 'status'),extra=10)

    customer = Customer.objects.get(id=pk_test)
    formset = OrderFormSet(instance=customer)

    # if not want refrence below uncomment above comment

    #formset = OrderFormSet(queryset =Order.objects.none() ,instance=customer)
    # form=OrderForm(initial ={'customer':customer})


    if request.method == 'POST':
        # print('Printing Post', request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context = {
        'formset': formset

    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='accounts:login')
def updateOrder(request, pk_test):
    order =Order.objects.get(id=pk_test)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        #print('Printing Post', request.POST)
        form=OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context ={
        'form':form

    }
    return render(request, 'accounts/order_form.html', context)
@login_required(login_url='accounts:login')
def deleteOrder(request, pk_test):
    order =Order.objects.get(id=pk_test)
    if request.method == 'POST':
        order.delete()
        return redirect('/')

    context={'item':order}
    return render(request, 'accounts/delete.html', context)