from django.contrib import auth, messages
from django.shortcuts import render, redirect
from django.core.paginator import Paginator, EmptyPage
from django.db.models import Q
from django.contrib.auth.models import User
from bookapp.models import UserProfile, loginTable
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib import messages
from bookapp.models import loginTable

def userRegistration(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')

        if password != password2:
            messages.error(request, 'Passwords do not match.')
            return redirect('register')

        if loginTable.objects.filter(username=username).exists():
            messages.error(request, 'Username already exists.')
            return redirect('register')

        
        userprofile = UserProfile(username=username, password=password)
        login_table = loginTable(username=username, password=password, type='user')

        userprofile.save()
        login_table.save()

        messages.success(request, 'Registration successful.')
        return redirect('login') 

    return render(request, 'accounts/register.html')




def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')

        user = authenticate(request, username=username, password=password)

        if user is not None:
            if user.is_superuser:
                login(request, user)
                return redirect('admin_view')

        try:
            user_details = loginTable.objects.get(username=username, password=password)
            user_name = user_details.username
            user_type = user_details.type

            request.session['username'] = user_name

            if user_type == 'user':
                return redirect('user_view')
            elif user_type == 'admin':
                return redirect('admin_view')

        except loginTable.DoesNotExist:
            messages.error(request, 'This user does not exist.')
            return redirect('login')

        messages.error(request, 'Invalid username or password.')
        return redirect('login')

    return render(request, 'accounts/login.html')



def admin_view(request):
    user_name = request.user.username
    return render(request, 'admin_view.html', {'user_name': user_name})


def user_view(request):
    user_name = request.user.username
    return render(request, 'user_view.html', {'user_name': user_name})

