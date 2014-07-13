# Create your views here.

#coding=utf-8

from django.http import  HttpResponse
from blog.models import  Users
from django.shortcuts import render_to_response
#from mongo import session

def index(req):
    return  render_to_response('index.html')

def login(req):
    name=req.POST.get('username')
    password=req.POST.get('userpwd')

    user=Users.objects.all().filter(username=name).filter(password=password)
    if user:
        req.session["username"]=name
        return HttpResponse(req.session["username"])
    else:
        return HttpResponse('<h1>faile</h1>')

def  regist(req):
    name=req.POST.get('username')
    password=req.POST.get('userpwd')
    user=Users.objects.create(username=name,password=password)
    user.save()

    return  HttpResponse('<h1>regist ok</h1>')

def  showreg(req):
   return  render_to_response('reg.html')

