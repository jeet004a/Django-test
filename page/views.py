from django.shortcuts import render,redirect

from django.contrib.auth.models import Group
from django.http import HttpResponse
from .models import *

from django.forms import inlineformset_factory
from .filters import OrderFilter
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required

from .decoraters import unauthenticated_user, allowed_user,admin_only
from .forms import OrderForm,Customercreate,CreateUserForm,CustomerForm
# Create your views here.
 
@unauthenticated_user
def register(request):
    form=CreateUserForm()
    if request.method=='POST':
        form=CreateUserForm(request.POST)
        if form.is_valid():
            user=form.save()
            username=form.cleaned_data.get('username')

            # group=Group.objects.get(name='customer')
            # user.groups.add(group)
            # Customer.objects.create(
            #     name=user,
            # )

            messages.success(request,'Account was created for '+username)
            return redirect('login')
    context={"form":form}
    return render(request,'register.html',context)

@unauthenticated_user
def loginPage(request):
    if request.method=='POST':
        username=request.POST.get('username')
        password=request.POST.get('password')

        user=authenticate(request,username=username,password=password)
        if user is not None:
            login(request,user)
            # return render(request,'dashboard.html')
            return redirect('index')

        else:
            messages.info(request,"Username or Password is incorrect")

    context={}
    return render(request,'login.html',context)

def logoutUser(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
@admin_only
def home(request):
    
    customers=Customer.objects.all()
    orders=Order.objects.all()
    total_orders=orders.count()
    delivered=orders.filter(name='Delivered').count()
    pending=orders.filter(name='Pending').count()
    context={'customers':customers,'orders':orders,'total_orders':total_orders,'delivered': delivered,
             'pending': pending}
    return render(request,'dashboard.html',context)


@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
# @admin_only
def userPage(request):
    orders=request.user.customer.order_set.all()
    
    total_orders=orders.count()
    delivered=orders.filter(name='Delivered').count()
    pending=orders.filter(name='Pending').count()
    print('Orders:-',orders)
    context={'orders':orders,'total_orders':total_orders,'delivered': delivered,
             'pending': pending}
    # context={}
    
    return render(request,'user.html',context)

@login_required(login_url='login')
@allowed_user(allowed_roles=['customer'])
def accountSettings(request):
    customer=request.user.customer
    form=CustomerForm(instance=customer)

    if request.method=='POST':
        form=CustomerForm(request.POST,request.FILES,instance=customer)
        if form.is_valid():
            form.save()
    context={'form':form}
    return render(request,'account_settings.html',context)



@login_required(login_url='login')
def products(request):
    products=Product.objects.all()
    return render(request,'products.html',{'products': products})

@login_required(login_url='login')
def customers(request,pk_test):
    customer=Customer.objects.get(id=pk_test)
    Order=customer.order_set.all()
    count=Order.count()
    myFilter=OrderFilter(request.GET,queryset=Order)
    Order=myFilter.qs
    context={'myFilter':myFilter,'customer':customer,'Order': Order,'count':count}
    return render(request,'customer.html',context)

# @login_required(login_url='login')
def createOrder(request,pk):
    OrderFormSet=inlineformset_factory(Customer,Order, fields=('product','name'))
    customer=Customer.objects.get(id=pk)
    formset=OrderFormSet(queryset=Order.objects.none(),instance=customer)
    # form=OrderForm(initial={'customer':customer})
    if request.method=='POST':
        # form=OrderForm(request.POST)
        formset=OrderFormSet(request.POST,instance=customer)
        if formset.is_valid():
            formset.save()
            return redirect('/')

    context={'formset':formset}

    return render(request,'order_form.html',context)

# @login_required(login_url='login')
def updateOrder(request, pk):
    order=Order.objects.get(id=pk)
    form=OrderForm(instance=order)
    if request.method=='POST':
        form=OrderForm(request.POST,instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')
    context={'form':form}
    return render(request,'order_form.html',context)

# @login_required(login_url='login')
def deleteOrder(request,pk):
    order=Order.objects.get(id=pk)
    if request.method=='POST':
        order.delete()
        return redirect('/')
    context={'item':order}
    return render(request,'delete.html',context)


def createCustomer(request):
    form=Customercreate(request.POST)
    if request.method=='POST':
        form=Customercreate(request.POST)
        if form.is_valid():
            form.save()
            return redirect('/')

    context={'form':form}

    return render(request,'create_customer.html',context)



