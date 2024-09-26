from django.contrib import auth
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from . import forms
from .models import Book,Author
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from . models import UserProfile,loginTable
# Create your views here.




# def createBook(request):
#     books = Book.objects.all()
#     if request.method == 'POST':

#         title = request.POST.get('title')
#         price = request.POST.get('price')

#         book = Book(title=title, price=price)

#         book.save()

#     return render(request, 'book.html', {'books': books})


def listBook(request):
    books = Book.objects.all()

    paginator = Paginator(books, 4)
    page_number = request.GET.get('page')

    try:
        page = paginator.get_page(page_number)

    except EmptyPage:
        page = paginator.page(page_number.num_pages)


    return render(request, 'admin/listBook.html', {'books': books, 'page': page})


def detailsView(request,book_id):
    book = Book.objects.get(id=book_id)
    return render(request, 'admin/detailsview.html', {'book': book})


# def updateBook(request,book_id):
#
#     book = Book.objects.get(id=book_id)
#
#     if request.method == 'POST':
#
#         title = request.POST.get('title')
#         price = request.POST.get('price')
#
#         book.title = title
#         book.price = price
#
#         book.save()
#
#         return redirect('/')
#
#
#     return render(request,'updateview.html', {'book':book})
#

def deleteView(request, book_id):

    book = Book.objects.get(id=book_id)

    if request.method == 'POST':

        book.delete()

        return render(request,'admin_view.html')

    return render(request, 'admin/deleteview.html', {'book':book})

def createBook(request):

    books = Book.objects.all()

    if request.method=='POST':
        form =forms.BookForm(request.POST, request.FILES)

        if form.is_valid():
            form.save()

            return render(request,'admin_view.html')

    else:
        form =forms.BookForm()

    return render(request,'admin/book.html',{'form':form,'books':books})


def Create_Author(request):
    if request.method=='POST':

        form=forms.AuthorForm(request.POST)

        if form.is_valid():
            form.save()

            return render(request,'admin_view.html')

    else:
        form=forms.AuthorForm()
    return render(request, 'admin/author.html',{'form':form})


def updateBook(request,book_id):

    book = Book.objects.get(id=book_id)
    if request.method=='POST':
         form=forms.BookForm(request.POST, request.FILES, instance=book)

         if form.is_valid():
             form.save()

             return render(request,'admin_view.html')

    else:
        form=forms.BookForm(instance=book)

    return render(request,'admin/updateview.html',{'form':form})


def index(request):
    return render(request,'home.html')




def Search_Book(request):
    query = None
    books = None

    if 'q' in request.GET:
        query = request.GET.get('q')
        # Assuming 'author' is a ForeignKey and 'name' is the field in the related Author model
        books = Book.objects.filter(Q(title__icontains=query) | Q(author__name__icontains=query))
    else:
        books = []

    context = {'books': books, 'query': query}
    return render(request, 'admin/search_book.html', context)





# def Register_user(request):

#     if request.method=='POST':

#         username=request.POST.get('username')
#         first_name=request.POST.get('first_name')
#         last_name=request.POST.get('last_name')
#         email=request.POST.get('email')
#         password=request.POST.get('password')
#         cpassword=request.POST.get('password1')

#         if password==cpassword:

#             if User.objects.filter(username=username).exists():
#                 messages.info(request,'This username is already taken')
#                 return redirect('register')
#             elif User.objects.filter(email=email).exists():
#                 messages.info(request,'This email is already exists')
#                 return redirect('register')
#             else:
#                 user=User.objects.create_user(username=username,first_name=first_name,last_name=last_name,email=email,password=password)
#                 user.save()
#             return redirect('login')

#         else:
#             messages.info(request,'This password not matching')
#             return redirect('register')

#     return render(request,'register.html')


# def loginUser(request):

#     if request.method=='POST':
#         username=request.POST.get('username')
#         password=request.POST.get('password')
#         user=auth.authenticate(username=username,password=password)

#         if user is not None:
#             auth.login(request,user)
#             return redirect('home')

#         else:
#             messages.info(request,'please provide correct details')
#             return redirect('login')

#     return render(request,'login.html')


def logOut(request):
    auth.logout(request)
    return redirect('login')


def HomePage(request):

    return render(request,'home.html')


# def userRegistration(request):

#     login_table=loginTable()
#     userprofile=UserProfile()

#     if request.method=='POST':

#         userprofile.username=request.POST.get('username')
#         userprofile.password=request.POST.get('password')
#         userprofile.password2=request.POST.get('password2')

#         login_table.username=request.POST.get('username')
#         login_table.password=request.POST.get('password')
#         login_table.password2=request.POST.get('password2')
#         login_table.type='user'

#         if request.POST.get('password')== request.POST.get('password2'):
#             userprofile.save()
#             login_table.save()

#            # messages.info(request, 'Registration success')
#             return render(request,'accounts/login.html')
#         else:
#             #messages.info(request, 'password not matching')
#             return redirect('register')

#     return render(request,'accounts/register.html')


# def loginPage(request):
#     if request.method == 'POST':
#         username = request.POST.get('username')
#         password = request.POST.get('password')
#         user = loginTable.objects.filter(username=username, password=password, type='user').exists()

#         try:
#             if user:
#                 user_details = loginTable.objects.get(username=username, password=password)
#                 user_name = user_details.username
#                 user_type = user_details.type
#                 if user_type == 'user':
#                     request.session['username'] = user_name
#                     return render(request, 'user_view.html')
#                 elif user_type == 'admin':
#                     request.session['username'] = user_name
#                     return render(request, 'admin_view.html')
#             else:
#                 #messages.error(request, 'Invalid username or password')
#                 print("invalid password")
#                 return render(request, 'accounts/login.html')  # Return HttpResponse here
#         except loginTable.DoesNotExist:
#             #messages.error(request, 'Invalid role')
#             print("invalid role")
#             return render(request, 'accounts/login.html')  # Return HttpResponse here

#     return render(request, 'accounts/login.html')  # This handles GET requests and any other cases


# def admin_view(request):
#     user_name=request.session['username']

#     return render(request,'admin_view.html',{'user_name':user_name})

# def user_view(request):
#     user_name=request.session['username']

#     return render(request,'user_view.html',{'user_name':user_name})





