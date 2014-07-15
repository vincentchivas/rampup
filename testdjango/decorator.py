# -*- coding: utf-8 -*-
import datetime
from django.http import HttpResponse
from db import user
from django.shortcuts import render_to_response

#可以加上对view的权限
def check_session(func):
    '''
     check user session
    '''
    def wrapper(req, *args, **kv):
        check = False
        session_key = req.session.session_key
        if session_key:
            item = user.find_session(
                {'session_key': session_key,
                 'expire_date': {
                     '$gt': datetime.datetime.now()
                 }
                 }
            )
            if item:
                uid = req.session.get('uid')
                if uid:
                    check = True
        if check:
            return func(req, *args, **kv)
        else:
            return render_to_response('index.html')
    return wrapper