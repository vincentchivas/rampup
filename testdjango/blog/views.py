# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse, HttpResponseRedirect
#from blog.models import  Users
from model.user import User,Group
from db import user,group
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
    if u.is_active:
        req.session["uid"] = u['_id']
        if u.is_superuser:
            permissions=user.find_permissions()
            #get all permissions
            # get left navigation data
        else:
                
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
    return json.json_response_ok(users,'user list')

def user_detail_modify(req,userid):
    u=user.find_one_user({'_id':userid})
    if u:
        if req.method=='GET':
            return json.json_response_ok(u,'one user detail')
        if req.method == 'POST':
            u.password = req.POST['password']
            u.email = req.POST['email']
            u.is_active = req.POST['is_active']
            u.is_superuser = req.POST['is_superuser']
            u.group_id = req.POST['group_id']
            u.permission_list = req.POST['permission_list']
            instance = user.save_user(u)
            return json.json_response_ok(u,'modify user detail')

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
       return json.json_response_ok('ok', 'add user success')

def del_user(req,userid):
    user.del_user(uerid)
    return json.json_response_ok('ok','delete success')



def group_list(req):
    groups=group.find_groups()
    return json.json_response_ok(groups,'get group list')

def group_detail_modify(req,group_id):
    g=group.find_one_group('_id':group_id)
    if g:
        if req.method == 'GET':
            return json.json_response_ok(g,'one group detail')
        if req.method == 'POST':
            g.group_name=req.POST['group_name']
            g.permission_list=req.POST['permission_list']
            group.save_group(g)
            return json.json_response_ok(instance,'modify group permission_list')            

def add_group(req):
    group_name = req.POST['group_name']
    g=Group.new(group_name)
    g.permission_list=req.POST['permission_list']
    group.save_group(g)
    return json.json_response_ok('ok','add group success')

def del_group(req,groupid):
    group.del_group(groupid)
    return json.json_response_ok('ok','delete success')




def perm_list(req):
    permissions=permission.find_permissions()
    return json.json_response_ok(permissions,'get permission list')

def perm_add(req):
    perm_name=req.POST['perm_name']
    p=Permission.new(perm_name)
    p.perm_profile=req.POST['perm_profile']
    p.container=req.POST['container']
    p.app_label=req.POST['app_label']
    p.model_label=req.POST['model_label']
    p.operator=req.POST['operator']
    permission.save_permission(p)
    return json.json_response_ok('ok','add permission success')

def perm_del(req,permid):
    permission.del_permission(permid)
    return json.json_response_error('ok','delete permission success')

def perm_detail_modify(req,permid):
    p=permission.find_one_permission('_id':permid)
    if p:
        if req.method == 'GET':
            return json.json_response_ok(g,'one permission detail')
        if req.method == 'POST':
            p.perm_name=req.POST['perm_name']
            p.perm_profile=req.POST['perm_profile']
            p.container=req.POST['container']
            p.app_label=req.POST['app_label']
            p.model_label=req.POST['model_label']
            p.operator=req.POST['operator']
            permission.save_permission(p)
            return json.json_response_ok(instance,'modify  permission')         














def regist(req):
    name = req.POST.get('username')
    password = req.POST.get('userpwd')
    user = Users.objects.create(username=name, password=password)
    user.save()

    return HttpResponse('<h1>regist ok</h1>')


def showreg(req):
    return render_to_response('reg.html')
