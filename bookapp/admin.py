from django.contrib import admin
from .models import Book,Author,UserProfile,loginTable
#register your models here.


admin.site.register(Book)
admin.site.register(Author)
admin.site.register(UserProfile)
admin.site.register(loginTable)
