from django.urls import path,include
from accounts import views


urlpatterns = [
    
    path('register',views.userRegistration,name='register'),

    path('login/',views.loginPage,name='login'),

    path('admin_view/',views.admin_view,name='admin_view'),

    path('user_view/',views.user_view,name='user_view'),
    
]
