from django.db import models

# Create your models here.


class Author(models.Model):

    name = models.CharField(max_length=200,null=True)

    def __str__(self):

        return '{}'.format(self.name)



class Book(models.Model):
    title = models.CharField(max_length=200)
    price = models.IntegerField()
    image=models.ImageField(upload_to='book_media')  
    quantity=models.IntegerField()

    author = models.ForeignKey(Author,  on_delete=models.CASCADE)  #Assure Referential Integrity

    def __str__(self):

        return '{}'.format(self.title)


class UserProfile(models.Model):

    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)
    


class loginTable(models.Model):

    username=models.CharField(max_length=200)
    password=models.CharField(max_length=200)
    password2=models.CharField(max_length=200)
    type=models.CharField(max_length=200)

    def __str__(self):
        return '{}'.format(self.username)
    


