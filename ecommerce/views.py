from django.shortcuts import render,redirect
from django.contrib.auth.models import User
from django.contrib.auth import  authenticate,login, logout
from django.contrib.auth.decorators import login_required
from .models import *

# Create your views here.

def index(request):
     products = Product.objects.all()
     
     return render(request, 'frontend/index.html', {'products' : products } )

def signIn(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        # Authenticate user
        print("++++++++++++++++++++++")
        user = authenticate(request, username= username, password=password)
        print(user)

        if user is not None:
            # If user is authenticated, log them in
            login(request, user)
            return redirect('/')
        else:
            # If authentication fails, show error message
            error_message = 'Invalid login credentials. Please try again.'
            return render(request, 'auth/login.html', {'error_message': error_message})

    # If request method is not POST (e.g., GET), render the login page
    return render(request, 'auth/login.html')


def register(request):
    if request.method =='POST':
        username = request.POST.get('username')
        email = request.POST.get('email')        
        password = request.POST.get('password')
        password_confirmation = request.POST.get('password_confirmation')

        if password ==password_confirmation:
            if User.objects.filter(username=username).exists():
                return render(request,'auth/register.html',{'error_message' : 'Username is  already exists.'}  )
            
            if User.objects.filter(email=email).exists():
                return render(request,'auth/register.html',{'error_message' : 'Email is already exists.'} )
            
            user = User.objects.create_user(username=username, email=email, password=password )
            return redirect('/')
        
        else :
            error_message ='Passwords did not match.'
            return render(request,'auth/register.html',{'error_message' : error_message})
        


    return render(request, 'auth/register.html')


def shop(request):
    products = Product.objects.all()
    return render(request, 'frontend/shop.html', {'products': products } )


def productDetails(request,id):
    product = Product.objects.get(pk=id)
    return render(request, 'frontend/productDetails.html', {'product' : product }  )


def cart(request):
    user = request.user
    if user.is_authenticated:
        carts = Cart.objects.filter(user=user)

        total_price = 0
        for cart_item in carts:
            total_price += int(cart_item.product.price * int(cart_item.quantity)
    )
    else:
        carts= None
        total_price = None
    return render(request, 'frontend/cart.html', {'carts' : carts, 'total_price': total_price  } )


def user_logout(request):
    logout(request)
    return redirect('/')

@login_required(login_url='/login')
def addToCart(request,product_id):
    product = Product.objects.get(pk=product_id)
    user = request.user
    quantity = request.POST.get('quantity')
    cart_item, created =  Cart.objects.get_or_create(user=user, product=product)

    if not created:
        cart_item.quantity += int(quantity)
        cart_item.save()
    else:
        cart_item.quantity = int(quantity)
        cart_item.save()

    return redirect('/cart/')


def removeFromCart(request,cart_id):
    cart_item = Cart.objects.get(pk=cart_id)
    cart_item.delete()
    return redirect('/cart/',  )





@login_required(login_url='/login/')
def checkout(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        address = request.POST.get('address')
        phone_number = request.POST.get('phone_number')

        if not (name and address and phone_number):
            return render(request, 'checkout.html', {'error_message': 'Invalid form data'})

        user = request.user

        new_order = Order.objects.create(user=user,name=name,address=address,phone_number=phone_number)
        new_order.save()
        carts = Cart.objects.filter(user=user)

        for cart_item in carts:
            new_cart_item = OrderDetail.objects.create(order=new_order,product=cart_item.product,quantity=cart_item.quantity,unit_price=cart_item.product.price)
            new_cart_item.save()
            cart_item.delete()

        return redirect('/')


    else:
        user = request.user
        if user.is_authenticated:
            carts = Cart.objects.filter(user=user)

            total_price = 0
            for cart_item in carts:
                total_price += int(cart_item.product.price) * int(cart_item.quantity)

        else:
            carts = None
            total_price = None

        return  render(request,'frontend/checkout.html',{'carts':carts,'total_price':total_price})



def orders(request):
    user = request.user
    if user.is_authenticated:
        orders = Order.objects.filter(user=user)
    
    else:
        orders = None
    return render(request,'frontend/orders.html', {'orders' : orders} )


def add_to_wishlist(request, product_id):
    user = request.user
    if user.is_authenticated:
        product = Product.objects.get(pk= product_id)
        wishlist_item, created =  WishList.objects.get_or_create(user=user, Product=product)


        if created:
            wishlist_item.save()
    return redirect('/wishlist')


def remove_from_wishlist(request, wishlist_id):
    wishlist_item = WishList.objects.get(pk=wishlist_id)
    wishlist_item.delete()
    return redirect('/wishlist')
        
        
def wishlist(request):
    user = request.user
    if user.is_authenticated:
        wishlists = WishList.objects.filter(user=user)
    
    else : 
        wishlists = None
    return render(request, 'frontend/wishlist.html', {'wishlists': wishlists})
