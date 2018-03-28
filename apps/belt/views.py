from __future__ import unicode_literals
from django.shortcuts import render, redirect
from models import *
import bcrypt
from django.contrib import messages

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

def index(request):
    print "index engaged"
    return render(request,"belt/index.html")

def home(request):

    return render(request,"belt/home.html")