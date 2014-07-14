# -*- coding: utf-8 -*-

from django.http import HttpResponse
#from blog.models import  Users
from model.user import User
from db import user
from django.shortcuts import render_to_response
#from mongo import session


def check_session(func):
    '''
     check user session
    '''
    def wrapper(req, *args, **kv):
        check = False
        session_key = req.session.session_key
        if session_key:
            item = user.find_session({'session_key': session_key})
            if item:
                uid = req.session.get('uid')
                if uid:
                    check = True
        if check:
            return func(req, *args, **kv)
        else:
            return render_to_response('index.html')
    return wrapper


@check_session
def index(req):
    return HttpResponse('<h1>no problem</h1>')


#@check_session
def login(req):
    name = req.POST.get('username')
    password = req.POST.get('userpwd')
    # username='vin' pss='123'
    instance = user.find_one_user({'user_name': name, 'password': password})
    if instance:
        req.session["uid"] = instance['_id']

        return HttpResponse(req.session["uid"])
    else:
        return HttpResponse('<h1>faile</h1>')


def regist(req):
    name = req.POST.get('username')
    password = req.POST.get('userpwd')
    user = Users.objects.create(username=name, password=password)
    user.save()

    return HttpResponse('<h1>regist ok</h1>')


def showreg(req):
    return render_to_response('reg.html')
