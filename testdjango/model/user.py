# -*- coding: utf-8 -*-
from utils.common import md5digest, unix_time
from model.base import ModelBase
#from db import  user


class User(ModelBase):

    @classmethod
    def new(cls, user_name, password='', email='', is_active=True, is_superuser=False, group_id=0, permission_list=[]):
        '''
        create user
        '''
        instance = cls()
        instance.user_name = user_name
        # if password: 密码已经在前端md5加密
        #  instance.password_hash = User.calc_password_hash(password)
        instance.password = password
        instance.email = email
        instance.is_active = is_active
        instance.is_superuser = is_superuser
        instance.group_id = group_id
        instance.permission_list = permission_list
        instance.created = instance.modified = unix_time()
        return instance

    @classmethod
    def calc_password_hash(cls, password):
        return unicode(md5digest(password))

    @classmethod
    def check_unique_name(cls,user_name):
        u=user.find_one_user({'user_name':user_name})
        if u:
            return False
        else:
            return True            


    def change_password(self, new_password):
        self.password = User.calc_password_hash(new_password)
        self.modified = unix_time()

    def change_group(self, new_group_id):
        self.group_id = new_group_id
        self.modified = unix_time()

    def change_permission(self, new_permission_list):
        self.permission_list = new_permission_list
        self.modified = unix_time()


class Group(ModelBase):

    @classmethod
    def new(cls, group_name, permission_list=[]):
        """
        creat group
        """
        instance = cls()
        instance.group_name = group_name
        instance.permission_list = permission_list
        return instance


class Permission(ModelBase):

    @classmethod
    def new(cls, perm_name, perm_profile='', container='', app_label='', model_label='', operator=''):
        instance = cls()
        instance.perm_name = perm_name
        instance.perm_profile = perm_profile
        instance.container = container
        instance.app_label = app_label
        instance.model_label = model_label
        instance.operator = operator
        return instance
