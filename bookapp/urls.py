from django.urls import path,include
from bookapp import views


urlpatterns = [

    path('logout/',views.logOut,name='logout'),

    path('home/',views.HomePage,name='home'),

    path("create-book", views.createBook,name='createbook'),

    path("author/",views.Create_Author,name='author'),

    path('listbook/', views.listBook,name='listbook'),

    path('detailsview/<int:book_id>/', views.detailsView,name='details'),

    path('updateview/<int:book_id>/', views.updateBook,name='update'),

    path('deleteview/<int:book_id>/', views.deleteView,name='delete'),

    path('searchbook/',views.Search_Book,name='searchbook'),
    
    path('',views.index)
]
