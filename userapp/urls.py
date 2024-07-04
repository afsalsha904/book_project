from django.urls import path,include
from userapp import views


urlpatterns = [
    # path('register',views.userRegistration,name='register'),

    # path('login/',views.loginPage,name='login'),

    # path('user_view/',views.user_view,name='user_view'),

    # path('logout/',views.logOut,name='logout'),

    # path('home/',views.HomePage,name='home'),

    path('userlistbook/', views.userlistBook,name='userlistbook'),

    path('detailsview/<int:book_id>/', views.userdetailsView,name='userbookdetails'),

    path('searchbook/',views.userSearch_Book,name='usersearchbook'),

    path('add_to_cart/<int:book_id>/',views.add_to_cart,name='addtocart'),

    path('view-cart/',views.view_cart,name='viewcart'),

    path('increase/<int:item_id>/',views.increase_quantity,name='increase_quantity'),

    path('decrease/<int:item_id>/',views.decrease_quantity,name='decrease_quantity'),

    path('remove-from-cart,<int:item_id>/',views.remove_from_cart,name='remove_cart'),

    path('create-checkout-session/',views.create_checkout_session,name='create-checkout-session'),

    path('success/',views.success,name='success'),

    path('cancel/',views.cancel,name='cancel'),

    path('',views.index)
]
