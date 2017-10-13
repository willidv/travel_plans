# -*- coding: utf-8 -*-
from __future__ import unicode_literals

from django.shortcuts import render, redirect, HttpResponse

from models import * 

from django.contrib import messages

from datetime import datetime

# Create your views here.
def index(request):
    return render(request, "examination/register.html")

def register(request):
    
    errors = User.objects.basic_validator(request.POST)
   
    if len(errors):
        for error in errors:
            messages.error(request, error)
        return redirect(index)
    
    if request.method == "POST":
        name = request.POST['name']
        username = request.POST['username']
        password = request.POST['password']
        confirm_password = request.POST['confirm_password']

        user = User.objects.create(name = request.POST['name'], username= username, password = password)
        user.save()

        request.session['id'] = user.id
        users = User.objects.all()

        context = {
            "users" : users,  
        }
        return redirect("/home")


def login(request):
    error = User.objects.login_validator(request.POST)
    
    if type(error) == list:
        for e in error:
            messages.error(request, e)
        return redirect(index)
    else:
        username = request.POST['username']
        user = User.objects.get(username = username)
        if id not in  request.session:
            request.session['id'] = user.id
        else:
            return redirect("/index")
        users = User.objects.all()
        context = {
            "users" : users  
        }
        return redirect("/home")

def home(request):
    users = User.objects.all()
    
    thisuser = User.objects.get(id = request.session['id'])
    all_plans = Plan.objects.all()
    t_plans = Plan.objects.filter(travelers = thisuser)

    context = {
            "thisuser" : thisuser,
            "t_plans" : t_plans,
            "all_plans" : all_plans
        }
    return render(request, "examination/home.html", context)

def new(request):
    return render(request, "examination/new.html")

def add(request):
    thisuser = User.objects.get(id = request.session['id']) 
    if request.method == "POST":
        if datetime.strptime(request.POST['t_d_from'], "%Y-%m-%d") >= datetime.strptime(request.POST['t_d_to'], "%Y-%m-%d"):
            return redirect(new)
        elif datetime.strptime(request.POST['t_d_from'],"%Y-%m-%d") < datetime.today():
            return redirect(new)
        elif len(request.POST['destination']) < 1:
            return redirect(new)
        elif len(request.POST['description']) < 1:
            return redirect(new)
        else:
            destination = request.POST['destination']
            description = request.POST['description']
            t_d_from = request.POST['t_d_from']
            t_d_to = request.POST['t_d_to']
            t_plan = Plan.objects.create(destination = destination, description = description, t_d_from = t_d_from, t_d_to = t_d_to)
            t_plan.travelers.add(thisuser)
            t_plan.save()   
    return redirect('/home')

def plan(request, id):
    thisplan = Plan.objects.get(id = id)
    users = User.objects.filter(plans = thisplan)
    for u in users:
        print u

    context = {
        "thisplan" : thisplan,
        "users" :users
    }
    return render(request, 'examination/info.html', context)

def join(request, id):
    thisuser = User.objects.get(id = request.session['id'])
    t_plan = Plan.objects.get(id = id)
    if request.method =="POST":
        t_plan.travelers.add(thisuser)
        t_plan.save()
    return redirect('/home')

def logout(request):
    request.session['id'] = None
    request.session.clear()
    request.session.modified = True
    return redirect(index)
