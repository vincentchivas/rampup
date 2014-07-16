from db.config import USER_DB
from model.user import User, Group, Permission
from db.seqid import get_next_id
from testdjango.settings import CONTAINERS, APPS


def save_user(user):
    assert user
    if not user.get('_id'):
        # assign sequential id
        user._id = get_next_id('user')
    USER_DB.user.save(user)
    return user


def find_one_user(filters={}):
    item = USER_DB.user.find_one(filters)
    if item:
        user = User(item)
        return user


def del_user(user_id):
    assert user_id
    USER_DB.user.remove({'_id': user_id})


def find_users(filters={}):
    users = []
    items = USER_DB.user.find(filters)
    if items:
        for item in items:
            users.append(User(item))
        return users


def find_session(filters={}):
    item = USER_DB.sessions.find_one(filters)
    return item


def save_group(group):
    assert group
    if not group.get('_id'):
        group._id = get_next_id('group')
    USER_DB.groups.save(group)


def find_one_group(filters={}):
    item = USER_DB.groups.find_one(filters)
    if item:
        group = Group(item)
        return group


def del_group(group_id):
    assert group_id
    USER_DB.groups.remove({'_id': group_id})


def find_groups(filters={}):
    groups = []
    items = USER_DB.groups.find(filters)
    if items:
        for item in items:
            groups.append(Group(item))
        return groups


def save_permission(permission):
    assert permission
    if not permission.get('_id'):
        # assign sequential id
        permission._id = get_next_id('permission')
    USER_DB.permission.save(permission)
    return permission


def find_one_permission(filters={}):
    item = USER_DB.permission.find_one(filters)
    if item:
        permission = Permission(item)
        return permission


def del_permission(permission_id):
    assert permission_id
    USER_DB.permission.remove({'_id': permission_id})


def find_permissions(filters={}):
    permissions = []
    items = USER_DB.permission.find(filters)
    if items:
        for item in items:
            permissions.append(Permission(item))
        return permissions


def init_perms():
    count = 0
    containers = CONTAINERS
    apps = APPS
    ops = ['add', 'modify', 'delete']
    for key in containers:
        container = key
        app_labels = containers[key]
        for app_label in app_labels:
            model_labels = apps.get(app_label)
            print model_labels
            for model_label in model_labels:
                for op in ops:
                    p = Permission()
                    p.perm_name = op + '_' + model_label + \
                        '_' + app_label  # check unique
                    if not find_one_permission({'perm_name': p.perm_name}):
                        p.perm_profile = 'can ' + op + ' ' + model_label
                        p.container = container
                        p.app_label = app_label
                        p.model_label = model_label
                        p.operator = op
                        count = count + 1
                        save_permission(p)
    return count

    
