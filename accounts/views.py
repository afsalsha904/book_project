
from django.contrib import auth
from pyexpat.errors import messages
from django.shortcuts import render,redirect
from django.core.paginator import Paginator,EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from bookapp. models import UserProfile,loginTable
# Create your views here.


def userRegistration(request):

    login_table=loginTable()
    userprofile=UserProfile()

    if request.method=='POST':

        userprofile.username=request.POST.get('username')
        userprofile.password=request.POST.get('password')
        userprofile.password2=request.POST.get('password2')

        login_table.username=request.POST.get('username')
        login_table.password=request.POST.get('password')
        login_table.password2=request.POST.get('password2')
        login_table.type='user'

        if request.POST.get('password')== request.POST.get('password2'):
            userprofile.save()
            login_table.save()

           # messages.info(request, 'Registration success')
            return render(request,'login.html')
        else:
            #messages.info(request, 'password not matching')
            return redirect('register')

    return render(request,'register.html')


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = loginTable.objects.filter(username=username, password=password, type='user').exists()

        try:
            if user:
                user_details = loginTable.objects.get(username=username, password=password)
                user_name = user_details.username
                user_type = user_details.type
                if user_type == 'user':
                    request.session['username'] = user_name
                    return render(request, 'user_view.html')
                elif user_type == 'admin':
                    request.session['username'] = user_name
                    return render(request, 'admin_view.html')
            else:
                #messages.error(request, 'Invalid username or password')
                print("invalid password")
                return render(request, 'login.html')  # Return HttpResponse here
        except loginTable.DoesNotExist:
            #messages.error(request, 'Invalid role')
            print("invalid role")
            return render(request, 'login.html')  # Return HttpResponse here

    return render(request, 'login.html')  # This handles GET requests and any other cases


def admin_view(request):
    user_name=request.session['username']

    return render(request,'admin_view.html',{'user_name':user_name})

def user_view(request):
    user_name=request.session['username']

    return render(request,'user_view.html',{'user_name':user_name})

