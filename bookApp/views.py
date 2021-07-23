from typing import List
from django.contrib import messages
from django.http import request
from django.shortcuts import redirect, render
import bcrypt
from .models import Author, Review, User , Book
# Create your views here.
def indexLogin(request):
    return render(request,'login.html')
def createUser(request):
    if request.method=='POST':
        errors=User.objects.userValidator(request.POST)
        if len(errors)>0:
            for key,value in errors.items():
                messages.error(request,value)
            return redirect('/')
        hash_pw=  bcrypt.hashpw(request.POST['pass'].encode(), bcrypt.gensalt()).decode()
        new_user=User.objects.create(
            name=request.POST['name'],
            username=request.POST['username'],
            email=request.POST['email'],
            password=hash_pw
        )
        request.session['logged_user']=new_user.id
        return redirect('/user')
    return redirect('/')

def logIn(request):
    if request.method=='POST':
        user=User.objects.filter(email=request.POST['usrEmail'])
        if user:
            log_user=user[0]
            if bcrypt.checkpw(request.POST['usrPass'].encode(), log_user.password.encode()):
                request.session['logged_user']=log_user.id
                return redirect('/user')
            messages.error(request,"Email/Password incorrect")
    return redirect('/')

def indexUser(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    context={
        'user': User.objects.get(id=request.session['logged_user']),
        'books': Book.objects.all(),
        'lastReviews': Review.objects.all().order_by('-createdAt')[:3]
    }
    return render(request,'index.html',context)
def addBookIndex(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    content={
        'autors': Author.objects.all()
    }
    return render(request,'addBook.html',content)
def addBook(request):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    if request.method=='POST':
        bookErrors=Book.objects.bookValidator(request.POST)
        reviewErrors=Review.objects.reviewValidator(request.POST)
        errors=list(bookErrors.values())+list(reviewErrors.values())
        if request.POST['autores']=="-1":
            if request.POST['autor']=="":
                messages.error(request,"please choose an author or create one")
            else:
                authorErrors=Author.objects.authorValidator(request.POST)
                errors += list(authorErrors)
        if errors:
            for error in errors:
                messages.error(request,error)
            return redirect('/book/addBook')
        if request.POST['autores'] == "-1":
            autor=Author.objects.create(authorName=request.POST['autor'])
        else:
            autor=Author.objects.get(id = request.POST['autores'])
        book=Book.objects.create(bookName=request.POST['title'])
        usuario=User.objects.get(id=request.session['logged_user'])
        review=Review.objects.create(
            reviewDesc=request.POST['review'],
            rating=int(request.POST['rating']),
            userReview=usuario,
            bookReview=book
        )
        book.authors.add(autor)
        return redirect('/user')
def indexBook(request, bookId):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    content={
        'book' : Book.objects.get(id=bookId),
        'reviews' : Review.objects.filter(bookReview=bookId)
    }
    return render (request,'indexBook.html', content)
def addBookReview(request, bookId):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    if request.method=='POST':
        errors=Review.objects.reviewValidator(request.POST)
        if errors:
            for error , value in errors.items():
                messages.error(request,value)
            return redirect(f'/book/{bookId}')
        book=Book.objects.get(id=bookId)
        user=User.objects.get(id=request.session['logged_user'])
        new_review=Review.objects.create(
            reviewDesc=request.POST['review'],
            rating=request.POST['rating'],
            userReview=user,
            bookReview=book

        )
        return redirect('/user')
    return redirect(f"/book/{bookId}")
def logout(request):
    request.session.flush()
    return redirect('/')
def userIndex(request, userId):
    if 'logged_user' not in request.session:
        messages.error(request, "Please Register or Log In")
        return redirect("/")
    #books=Book.objects.filter(id__book_reviews=request.session['logged_user'])

    #print(books)
    context={
        'users': User.objects.get(id=userId),
     #   'books': books

    }
    return render(request,'userReview.html',context)