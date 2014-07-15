# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, HttpResponseRedirect
#from blog.models import  Users
from model.user import User
from db import user
from django.shortcuts import render_to_response
from decorator import check_session
from utils import json


#@check_session
def index(req):
    # return HttpResponse('<h1>no problem</h1>')
    return render_to_response('index.html')


#@check_session
def login(req):
    name = req.POST.get('username')
    password = req.POST.get('userpwd')
    u = user.find_one_user({'user_name': name, 'password': password})
    if u:
        req.session["uid"] = u['_id']
        # get left navigation data
        return json.json_response_ok(name, 'ok')
    else:
        return json.json_response_error(1, {}, 'authetic error')

#@check_session


def logout(req):
    session_key = req.session.session_key
    req.session.delete()
    return HttpResponseRedirect('/blog/index/')


def change_password(req):
    old_pwd = req.POST.get('old_pwd')
    new_pwd = req.POST.get('new_pwd')
    uid = req.session.get('uid')
    u = user.find_one_user({'_id': uid})
    pwd = u['password']
    if old_pwd == pwd:
        u['password'] = new_pwd
        user.save_user(u)
        return json.json_response_ok('ok', 'password has changed')
    else:
        return json.json_response_error(1, {}, 'old password is not match')


def user_list(req):
    users = user.find_users()
    return users

#def user_detail_modify(req):
 #   if req.method=='GET':



def add_user(req):
    user_name = req.POST['username']
    u = User.new(user_name)
    u.password = req.POST['password']
    u.email = req.POST['email']
    u.is_active = req.POST['is_active']
    u.is_superuser = req.POST['is_superuser']
    u.group_id = req.POST['group_id']
    u.permission_list = req.POST['permission_list']
    instance = user.save_user(u)
    if instance:
    return json.json_response_ok('ok', 'password has changed')


def regist(req):
    name = req.POST.get('username')
    password = req.POST.get('userpwd')
    user = Users.objects.create(username=name, password=password)
    user.save()

    return HttpResponse('<h1>regist ok</h1>')


def showreg(req):
    return render_to_response('reg.html')
