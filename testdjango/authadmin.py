from mongoengine  import *
from mongoengine.django.auth  import *
connect('test')

def adduser(username,password):
    user=MongoEngineBackend()
    tag=user.authenticate(username,password)
    if not tag :
        User.create_user(username,password)
        return  'success'
    else :
        return  'fail'


