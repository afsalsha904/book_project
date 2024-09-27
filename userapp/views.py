
from django.conf import settings
from django.contrib import auth
from pyexpat.errors import messages
from django.shortcuts import render,redirect, get_object_or_404
from django.contrib.auth.decorators import login_required
from .models import Book, Cart, CartItem
from django.urls import reverse
import stripe
from bookapp.models import Book
from userapp.models import Cart,CartItem
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
# Create your views here.



def userlistBook(request):
    books = Book.objects.all()

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)

    except EmptyPage:
        page = paginator.page(page_number.num_pages)


    return render(request, 'user/userlistbook.html', {'books': books, 'page': page})


def userdetailsView(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'user/userdetailsview.html', {'book': book})


def index(request):
    return render(request,'home.html')


def userSearch_Book(request):

    query=None
    books=None

    if 'q' in request.GET:
        query=request.GET.get('q')
        books=Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))

    else:
        books=[]

    context={'books':books,'query':query}

    return render(request,'user/usersearch.html',context)




def add_to_cart(request, book_id):
    book = Book.objects.get(id=book_id)
    try:
        if request.user.is_authenticated:
            if book.quantity > 0:
                cart, created = Cart.objects.get_or_create(user=request.user)
                cart_item, item_created = CartItem.objects.get_or_create(cart=cart, book=book)

                if item_created:
                    cart_item.quantity = 1  
                else:
                    cart_item.quantity += 1 

                cart_item.save()

            return redirect('viewcart')
    except:
        messages.error(request, "please login")


def view_cart(request):
    try:
        if request.user.is_authenticated:
            cart, created = Cart.objects.get_or_create(user=request.user)
            cart_items = cart.cartitem_set.all()
            total_price = sum(item.book.price * item.quantity for item in cart_items)
            total_items = cart_items.count()

            context = {
                'cart_items': cart_items,
                'total_price': total_price,
                'total_items': total_items
            }

            return render(request, 'user/cart.html', context)
        else:
            messages.error(request, 'Please login first')
    except Cart.DoesNotExist:
        messages.error(request, 'Error retrieving the cart')

    # Default context in case of an exception or user not authenticated
    context = {
        'cart_items': [],
        'total_price': 0,
        'total_items': 0
    }

    return render(request, 'user/cart.html', context)



def increase_quantity(request,item_id):

    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity < cart_item.book.quantity:

        cart_item.quantity +=1
        cart_item.save()
    
    return redirect('viewcart')


def decrease_quantity(request,item_id):
    
    cart_item = CartItem.objects.get(id=item_id)

    if cart_item.quantity > 1:

        cart_item.quantity -=1
        cart_item.save()
    
    return redirect('viewcart')

def remove_from_cart(request,item_id):

    try:

        cart_item=CartItem.objects.get(id=item_id)
        cart_item.delete()
    
    except cart_item.DoesNotExist:
        pass

    return redirect('viewcart')


def create_checkout_session(request):
    cart_items = CartItem.objects.all()

    if cart_items:
        stripe.api_key = settings.STRIPE_SECRET_KEY

        if request.method == 'POST':
            line_items = []
            for cart_item in cart_items:
                if cart_item.book:
                    line_item = {
                        'price_data': {
                            'currency': 'INR',
                            'unit_amount': int(cart_item.book.price * 100),
                            'product_data': {
                                'name': cart_item.book.title
                            },
                        },
                        'quantity':cart_item.quantity
                    }
                    line_items.append(line_item)
                    
            if line_items:

                checkout_session = stripe.checkout.Session.create(
                    payment_method_types=['card'],
                    line_items=line_items,
                    mode='payment',
                    success_url=request.build_absolute_uri(reverse('success')),
                    cancel_url=request.build_absolute_uri(reverse('cancel'))
                )

                return redirect(checkout_session.url,code=302)
    
    return redirect(reverse('viewcart'))



def success(request):
    cart_items=CartItem.objects.all()

    for cart_item in cart_items:
        product=cart_item.book
        if product.quantity >= cart_item.quantity:
            product.quantity -= cart_item.quantity
            product.save()

    
    cart_items.delete()

    return render(request,'user/success.html')


def cancel(request):
    return render(request,'user/userlistbook.html')




