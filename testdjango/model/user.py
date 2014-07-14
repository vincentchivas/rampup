# -*- coding: utf-8 -*-
from utils.common import md5digest, unix_time
from model.base import ModelBase


class User(ModelBase):
    
    @classmethod
    def new(cls, user_name, password='',email='',is_active=True,is_superuser=False, group_id=0, permission_list=[]):
        '''
        create user
        '''
        instance = cls()
        instance.user_name = user_name
        #if password: 密码已经在前端md5加密
        #  instance.password_hash = User.calc_password_hash(password)
        instance.password=password
        instance.email=email
        instance.is_active=is_active
        instance.is_superuser=is_superuser
        instance.group_id = group_id
        instance.permission_list = permission_list
        instance.created = instance.modified = unix_time()
        return instance

    @classmethod
    def calc_password_hash(cls, password):
        return unicode(md5digest(password))

    def change_password(self, new_password):
        self.password= User.calc_password_hash(new_password)
        self.modified = unix_time()

    def change_group(self, new_group_id):
        self.group_id = new_group_id
        self.modified = unix_time()

    def change_permission(self, new_permission_list):
        self.permission_list = new_permission_list
        self.modified = unix_time()


class Group(ModelBase):
    pass


class Permission(ModelBase):
    pass


class Session(ModelBase):
    pass



