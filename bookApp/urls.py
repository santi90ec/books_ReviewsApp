from django.contrib import admin
from django.urls import path
from django.urls.conf import include
from . import views
urlpatterns = [
    path('',views.indexLogin),
    path('register',views.createUser),
    path('login',views.logIn),
    path('logout',views.logout),
    path('user',views.indexUser),
    path('user/<int:userId>',views.userIndex),
    path('book/addBook',views.addBookIndex),
    path('book/addBook/add',views.addBook),
    path('book/<int:bookId>',views.indexBook),
    path('book/<int:bookId>/addReview',views.addBookReview)
]
