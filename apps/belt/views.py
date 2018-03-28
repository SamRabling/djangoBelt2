from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.contrib import messages
from django.db.models import Count


## ---------------- LOGIN AND REGISTRATION --------
def create(request):
    print "create engaged"
    errors = User.objects.regis_basic_validator(request.POST)
    print "create processing"
    if len(errors):
        for tag, errors in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
            return redirect('/')
    print "create processing..."
    passworD = request.POST['Password']
    hashed = bcrypt.hashpw(passworD.encode(),bcrypt.gensalt())
    if request.method == "POST":
        user = User.objects.create(first_name=request.POST['first_name'], last_name=request.POST['last_name'], email=request.POST['email'], birthday=request.POST['birthday'], password=hashed)
        print "new id created"
        request.session['id'] = user.id
        return redirect('/home')

def process(request):
    print "process engaged"
    errors = User.objects.log_basic_validator(request.POST)
    if len(errors):
        for tag, errors in errors.iteritems():
            messages.error(request, errors, extra_tags=tag)
            print "validation in process"
            return redirect('/')
    email = request.POST['email']
    request.session['id'] = User.objects.get(email=email).id
    print User.objects.get(email=email).id
    print "validation in process"
    return redirect('/home')
## -------- ACCESS TO PAGES ----------

def index(request):
    print "index engaged"
    return render(request,"belt/index.html")

def home(request):
    print "home engaged"
    if 'id' not in request.session:
        return redirect('/')
    else:

        user = User.objects.get(id = request.session['id'])
        myquotes = user.shared_quote.all()
        others = Quote.objects.exclude(owner_id = request.session['id'])
       
        context={
            'user':user,
            # 'quotes':quotes,
            'others':others,
            'myquotes':myquotes,
        }
    return render(request,"belt/home.html", context)

def user_quotes(request, id):
    print "user_quotes engaged"
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id = id)
        quotes = Quote.objects.filter(owner_id= id)
        count = user.user_list.count()
        context={
            'user':user,
            'quotes':quotes,
            'count': count,
        }
    return render(request,"belt/user_quotes.html", context)

def logout(request):
    print "logout engaged"
    if 'id' not in request.session:
        return redirect('/')
    request.session.clear()
    return redirect("/")

## --------- ACTIONS FOR QUOTES -------

def add_quote(request):
    print "add_quote engaged"
    if 'id' not in request.session:
        return redirect('/')
    else:
        errors = Quote.objects.quote_basic_validator(request.POST)  
        if len(errors):
            for tag, errors in errors.iteritems():
                messages.error(request, errors,  extra_tags=tag)
                return redirect('/home')
        user = User.objects.get(id = request.session['id'])
        print "user saved"
        Quote.objects.create(quoted_by=request.POST['quoted_by'], text=request.POST['text'], owner= user)
        quote = Quote.objects.last()
        print "quote saved"
        quote.quotelist.add(user)
        print "quote added"
        return redirect('/home')

def add_to_my_faves(request, id):
    print "add_to_my_faves engaged"
    if 'id' not in request.session:
        return redirect('/')
    else:
        user_list= User.objects.get(id = request.session['id'])
        print "user saved"
        quote = Quote.objects.get(id=id)
        print "quote saved" 
        quote.quotelist.add(user_list)
        quote.save()
        print "quote added"
        return redirect("/home")

def remove_from_faves(request, id):
    print "remove_from_my_faves engaged"
    if 'id' not in request.session:
        return redirect('/')
    else:
        user = User.objects.get(id=request.session['id'])
        print "user saved"
        quote = Quote.objects.get(id=id)
        print "quote saved" 
        quote.quotelist.remove(user)
        return redirect("/home")
