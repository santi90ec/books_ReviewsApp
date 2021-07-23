from django.contrib.messages.api import error
from django.db import models
from datetime import date
import re

EMAIL_REGEX = re.compile(r'^[a-zA-Z0-9.+_-]+@[a-zA-Z0-9.+_-]+\.[a-zA-Z]+$')
class UserManager(models.Manager):
    def userValidator(self,postData):
        errors={}
        if len(postData['name'])<2:
            errors['name']="El campo nombre no puede tener menos de 8 caracteres"
        if len(postData['username'])<2:
            errors['username']="El usuario no puede estar vacio"
        if len(postData['email'])<2:
            errors['email']="Mail no puede ser vacio"
        prev_usr=User.objects.filter(email=postData['email'])
        if len(prev_usr) >=1:
            errors['exists']="Email address already exists" 
        if not EMAIL_REGEX.match(postData['email']):
            errors['emailValido']="Email no valido"
        if (len(postData['pass'])<8 or (postData['pass']!=postData['confirmPass'])):
            errors['pass']="La contraseña es invalido o no coinciden"
        return errors
class BookManager(models.Manager):
    def bookValidator(self,postData):
        errors={}
        if (len(postData['title'])<1):
            errors['titulo']="El nombre no puede estar vacio"
        
        
        return errors
class AuthorManager(models.Manager):
    def authorValidator(self,postData):
        errors={}
        obj=Author.objects.filter(authorName=postData['autor'])
        if len(obj)>=1:
            errors['autor_2']="El autor ya se encuentra en la lista"
        return errors
class ReviewManager(models.Manager):
    def reviewValidator(self,postData):
        errors={}
        if (len(postData['review'])<1):
            errors['review']="El review no puede estar vacio"
        return errors
class User(models.Model):
    name=models.CharField(max_length=40)
    username=models.CharField(max_length=40)
    email=models.EmailField()
    password=models.CharField(max_length=40)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    objects = UserManager()
class Book(models.Model):
    bookName=models.CharField(max_length=45)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    objects=BookManager()
class Author(models.Model):
    authorName=models.CharField(max_length=45)
    books=models.ManyToManyField(Book, related_name="authors")
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    objects=AuthorManager()
class Review(models.Model):
    reviewDesc=models.TextField()
    rating=models.IntegerField()
    userReview=models.ForeignKey(User,related_name="users_review", on_delete=models.CASCADE)
    bookReview=models.ForeignKey(Book,related_name="book_reviews",on_delete=models.CASCADE)
    createdAt=models.DateTimeField(auto_now_add=True)
    updatedAt=models.DateTimeField(auto_now=True)
    objects=ReviewManager()
