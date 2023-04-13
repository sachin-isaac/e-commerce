from django.shortcuts import render,redirect
from .models import *
from shop.forms import UserForm
from django.contrib import messages
from django.contrib.auth import authenticate,login,logout
from django.http import JsonResponse
import json,random

def home(request):
    try:
        products=Product.objects.filter(trending=1)
        return render(request,"products/home.html",{"products":products})
    except Exception as e:
        print(e)

def login_page(request):
    try:
        if request.user.is_authenticated:
            return redirect('home')
        else:
            if request.method=='POST':
                usr=request.POST.get('username')
                pwd=request.POST.get('password')
                user=authenticate(request,password=pwd,username=usr)
                if user is not None:
                    login(request,user)
                    messages.success(request,'Logged in successfully')
                    return redirect("home")
                else:
                    messages.error(request,'Invalid email or password')
                    return redirect('login')    
            return render(request,'user/login.html')
    except Exception as e:
        print(e) 
        return redirect('home')

def logout_page(request):
    try:
        if request.user.is_authenticated:
            logout(request)
            messages.success(request,'Logout Successfully')
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')

def register(request): 
    try:
        form=UserForm()
        if request.method=='POST':
            form=UserForm(request.POST)
            if form.is_valid():
                form.save()
                messages.success(request,"Registration Success You can Login Now ...!")
                return redirect('login')
        return render(request,"user/register.html",{"form":form})    
    except Exception as e:
        print(e)
        return redirect('home')

def collections(request):
    try:
        category=Category.objects.filter(status=0)
        return render(request,"products/collections.html",{"category":category}) 
    except Exception as e:
        print(e) 
        return redirect('home')
     
def view(request,name):
    try:
        if(Category.objects.filter(name=name,status=0)):
            products=Product.objects.filter(category__name=name)
            return render(request,"products/products.html",{"products":products,"category_name":name})  
        else:
            messages.warning(request,"No such category Found")
            return redirect('collections')
    except Exception as e:
        print(e)   
        return redirect('home') 

def details(request,cname,pname):
    try:
        if(Category.objects.filter(name=cname,status=0)):
            if(Product.objects.filter(name=pname,status=0)): 
                products=Product.objects.filter(name=pname,status=0).first()
                return render(request,'products/details.html',{"products":products,})
            else:
                messages.error(request,'No Such Product Found')
                return redirect('collections')
        else:
            messages.error(request,'No Such Category Found')
            return redirect("collections")    
    except Exception as e:
        print(e) 
        return redirect('home')   
    
def addto_cart(request):    
    try:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            if request.user.is_authenticated:
                data=json.load(request)
                product_qty=data['product_qty']
                product_id=data['pid']
                product_status=Product.objects.get(id=product_id)
                if product_status:
                    if Cart.objects.filter(user=request.user.id,product_id=product_id):
                        return JsonResponse({'status':'Product already in cart'}, status=200)
                    else:
                        if product_status.quantity>=product_qty:
                            Cart.objects.create(user=request.user,product_id=product_id,product_qty=product_qty)
                            return JsonResponse({'status':'Product added to the cart'},status=200)
                        else:
                            return JsonResponse({'status':'Product Stock Not available'},status=200)
                        
                return JsonResponse({"status":"Product Added to cart"},status=200)
            else:
                return JsonResponse({'status':'Login to Add Cart'},status=200)

        else:
            return JsonResponse({'status':'Invalid Access'}, status=200)
    except Exception as e:
        print(e) 
        return redirect('home')   
    
def cart_page(request):
    try:
        if request.user.is_authenticated:
            cart=Cart.objects.filter(user=request.user)
            total_price=0
            for item in cart:
                total_price += item.total_cost
            return render(request,'cart/cart.html',{"cart":cart,"total_price":total_price})
        else:
            return redirect("home")
    except Exception as e:
        print(e)   
        return redirect('home') 
    
def remove_cart(request,cid):
    try:
        citem=Cart.objects.get(id=cid)
        citem.delete()
        return redirect('cart')
    except Exception as e:
        print(e)
        return redirect('home')

def fav(request):    
    try:
        if request.headers.get('x-requested-with')=='XMLHttpRequest':
            if request.user.is_authenticated:
                data=json.load(request)
                product_id=data['pid']
                product_status=Product.objects.get(id=product_id)
                if product_status:
                    if Favourite.objects.filter(user=request.user.id,product_id=product_id):
                        return JsonResponse({'status':'Product already in Favourite'}, status=200)
                    else:
                        Favourite.objects.create(user=request.user,product_id=product_id)
                        return JsonResponse({'status':'Product added to Favourite'},status=200)
            else:
                return JsonResponse({'status':'Login to Add Favourite'},status=200)

        else:
            return JsonResponse({'status':'Invalid Access'}, status=200)
    except Exception as e:
        print(e) 
        return redirect('home')   

def fav_page(request):
    try:
        if request.user.is_authenticated:
            fav=Favourite.objects.filter(user=request.user)
            return render(request,'cart/fav.html',{"fav":fav})
        else:
            return redirect("home")
    except Exception as e:
        print(e)    
        return redirect('home')

def remove_fav(request,fid):
    try:
        fitem=Favourite.objects.get(id=fid)
        fitem.delete()
        return redirect('fav_page')    
    except Exception as e:
        print(e)
        return redirect('home')
    
def checkout(request):
    try:
        rawcart=Cart.objects.filter(user=request.user)
        for item in rawcart:
            if item.product_qty > item.product.quantity:
                Cart.Objects.delete(id=item.id)
                return JsonResponse({'status':'Product Stock Not available'},status=200)
        cartitems=Cart.objects.filter(user=request.user)
        total_price=0
        for item in cartitems:
            total_price += item.total_cost

        pf = Profile.objects.filter(user=request.user).first()
    
        return render(request,'cart/checkout.html',{"cartitems":cartitems,"total_price":total_price,"pf":pf})
    except Exception as e:
        print(e)
        return redirect('home')

def remove_checkout(request,cid):
    try:
        citem=Cart.objects.get(id=cid)
        citem.delete()
        return redirect('checkout')
    except Exception as e:
        print(e) 
        return redirect('home')       

def placeorder(request):
    try:
        if request.method == 'POST':
            if not Profile.objects.filter(user=request.user):
                pf = Profile()
                pf.user = request.user
                pf.fname = request.POST.get('fname')
                pf.lname = request.POST.get('lname')
                pf.email = request.POST.get('email')
                pf.phone = request.POST.get('phone')
                pf.address = request.POST.get('address')
                pf.country = request.POST.get('country')
                pf.state = request.POST.get('state')
                pf.city = request.POST.get('city')
                pf.pincode = request.POST.get('pincode')
                pf.save()
            
            neworder=Order()
            neworder.user = request.user
            neworder.fname = request.POST.get('fname')
            neworder.lname = request.POST.get('lname')
            neworder.email = request.POST.get('email')
            neworder.phone = request.POST.get('phone')
            neworder.address = request.POST.get('address')
            neworder.country = request.POST.get('country')
            neworder.state = request.POST.get('state')
            neworder.city = request.POST.get('city')
            neworder.pincode = request.POST.get('pincode')
            
            neworder.payment_mode=request.POST.get('payment_mode')
            
            cartitems=Cart.objects.filter(user=request.user)
            total=0
            for item in cartitems:
                total += item.total_cost
            neworder.total_price=total
            
            trackno='amaz'+str(random.randint(11111,99999))
            while Order.objects.filter(tracking_no=trackno) is None:
                trackno='amaz'+str(random.randint(11111,99999))
            neworder.tracking_no=trackno
            neworder.save()

            neworderitems = Cart.objects.filter(user=request.user)
            for item in neworderitems:
                OrderItem.objects.create(
                    order=neworder,
                    product=item.product,
                    price=item.product.selling_price,
                    quantity=item.product_qty
                )

                orderproduct = Product.objects.filter(id=item.product_id).first()
                orderproduct.quantity=orderproduct.quantity-item.product_qty
                orderproduct.save()
            
            Cart.objects.filter(user=request.user).delete()   

            messages.success(request,"Your Order has been placed sucessfully") 
            
        return redirect('home')
    except Exception as e:
        print(e)
        return redirect('home')

def my_orders(request):
    try:
        orders=Order.objects.filter(user=request.user)
        return render(request,'cart/orders.html',{"orders":orders})
    except Exception as e:
        print(e)   
        return redirect('home') 
    
def view_order(request,tid):
    try:
        order= Order.objects.filter(tracking_no=tid).filter(user=request.user).first()
        orderitems=OrderItem.objects.filter(order=order)
        return render(request,'cart/vieworder.html',{"order":order,"orderitems":orderitems})
    except Exception as e:
        print(e)   
        return redirect('home') 