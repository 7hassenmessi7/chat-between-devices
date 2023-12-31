from django.shortcuts import render, redirect 
from django.http import HttpResponse
from django.template import loader
from django.forms import inlineformset_factory
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import authenticate,login,logout
from django.shortcuts import get_object_or_404, render

from django.contrib import messages 

from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import Group
from django.views import generic
from django.views.generic import TemplateView
from django.urls import reverse_lazy

from .models import *
from .forms import OrderForm,CreateUserForm,BookForm

from .filters import OrderFilter
from .decorators import unauthenticated_user, allowed_users,admin_only
from django.core.files.storage import FileSystemStorage







@unauthenticated_user
def registerPage(request):
      

    form =CreateUserForm()
    if request.method == 'POST':
        form = CreateUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            username = form.cleaned_data.get('username')
            
            group = Group.objects.get(name = 'customer')
            user.groups.add(group)

            Customer.objects.create(
                user=user,
            )


            messages.success(request, 'Account was created for'+ username)
            return redirect('login')
        
  
    context = {'form':form}
    return render(request , 'chat/register.html',context)


@unauthenticated_user
def loginPage(request):
    
  
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            login(request, user)
            return redirect('main')
        else:
             messages.info(request, 'Username OR Password is incorrect')    
    context = {}
    return render(request , 'chat/login.html',context)  


@allowed_users(allowed_roles=['customer'])
@login_required(login_url='login')
def userPage(request):
    orders = request.user.customer.order_set.all()

    total_orders = orders.count()
    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()

    print('ORDERS', orders)
    context = {'orders':orders, 'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

    return render (request, 'chat/user.html',context)




def logoutUser(request):
    logout(request)
    return redirect ('login')      






@login_required(login_url='login')
@admin_only
def main(request):
    orders   = Order.objects.all()
    customers = Customer.objects.all()
    total_customers = customers.count()
    total_orders = orders.count()
    
    delivered = orders.filter(status='Delivered').count()
    pending = orders.filter(status='Pending').count()
    
    context = {'orders':orders, 'customers':customers,
	'total_orders':total_orders,'delivered':delivered,
	'pending':pending }

	
    return render(request, 'chat/dashboard.html', context)
   
        




@login_required(login_url='login')
def index(request):
    return render(request, 'chat/index.html')

@login_required(login_url='login')
def room(request, room_name):
    
 
    username = request.user.username
    print("USERNAME IS : ", username, flush=True)
    messages = Message.objects.filter(room=room_name)[0:25]
    customers=Customer.objects.all()



    return render(request, 'chat/room.html', {'room_name': room_name, 'username': username, 'messages': messages ,'customers':customers}) 




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def products(request):
	products = Product.objects.all()

	return render(request, 'chat/products.html', {'products':products})





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def customer(request, pk_test):
    customer = Customer.objects.get(id=pk_test)
    orders =   customer.order_set.all()
    order_count = orders.count()
     
    myFilter = OrderFilter(request.GET, queryset=orders)
    orders = myFilter.qs
     
    context = {'customer':customer, 'orders':orders ,'order_count':order_count , 'myFilter':myFilter}
    return render(request, 'chat/customer.html',context)





@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def createOrder(request,pk):
    OrderFormSet = inlineformset_factory(Customer, Order,fields=('product','status'), extra =10)
    customer=Customer.objects.get(id=pk)
    formset = OrderFormSet(queryset=Order.objects.none(),instance=customer)
   # form = OrderForm(initial={'customer':customer})
    if request.method == 'POST':
        #print('Printing POST:' , request.POST)
        #form = OrderForm(request.POST)
        formset = OrderFormSet(request,POST,instance=customer)
        if formset.is_valid():
            formset .save()
            return redirect('/')

    context = {'formset':formset}
    
    return render(request, 'chat/order_form.html', context)




@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def updateOrder(request,pk):
    order = Order.objects.get(id=pk)
    form = OrderForm(instance=order)
    if request.method == 'POST':
        
        form = OrderForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/')

    context = {'form':form}

    return render(request, 'chat/order_form.html', context)



@login_required(login_url='login')
@allowed_users(allowed_roles=['admin'])
def deleteOrder(request,pk):
    order = Order.objects.get(id=pk)
    if request.method == "POST":
        order.delete()
        return redirect('/')
    context = {'item':order}
    return render (request,'chat/delete.html',context)




def upload(request):
    context = {}
    if request.method == 'POST':
        uploaded_file = request.FILES['document']
        fs = FileSystemStorage()
        name = fs.save(uploaded_file.name, uploaded_file)
        context['url'] = fs.url(name)
    return render(request, 'chat/upload.html', context) 


def book_list(request):
    books = Book.objects.all()
    return render(request, 'chat/book_list.html', {
        'books': books
    })



def delete_book(request, pk):
    if request.method == 'POST':
        book = Book.objects.get(pk=pk)
        book.delete()
    return redirect('book_list')



def upload_book(request):
    if request.method == 'POST':
        form = BookForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('book_list')
    else:
        form = BookForm()
    return render(request, 'chat/upload_book.html', {
        'form': form
    })



def home(request):
    return render(request, 'chat/home.html')



