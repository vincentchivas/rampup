from db.config import USER_DB
from model.user import User,Group,Permission
from db.seqid import get_next_id


def save_user(user):
    assert user
    if not user.get('_id'):
        # assign sequential id
        user._id = get_next_id('user')
    USER_DB.user.save(user)
    return user

def find_one_user(filters={}):
    item=USER_DB.user.find_one(filters)
    if item:
        user=User(item)
        return  user

def del_user(user_id):
    assert user_id
    USER_DB.user.remove({'_id':user_id})

def find_users(filters={}):
    users=[]
    items=USER_DB.user.find(filters)
    if items:
        for item in items:
            users.append(User(item))
        return users

def find_session(filters={}):
    item=USER_DB.sessions.find_one(filters)
    return item

def save_group(group):
    assert group
    if not group.get('_id'):
        group._id = get_next_id('group')
    USER_DB.groups.save(group)
    
def find_one_group(filters={}):
    item=USER_DB.group.find_one(filters)
    if item:
        group=Group(item)
        return  group

def del_group(group_id):
    assert group_id
    USER_DB.groups.remove({'_id':group_id})

def find_groups(filters={}):
    groups=[]
    items=USER_DB.groups.find(filters)
    if items:
        for item in items:
            groups.append(Group(item))
        return groups     

def save_permission(permission):
    assert permission
    if not permission.get('_id'):
        # assign sequential id
        permission._id = get_next_id('permission')
    permission_DB.permission.save(permission)
    return permission

def find_one_permission(filters={}):
    item=permission_DB.permission.find_one(filters)
    if item:
        permission=permission(item)
        return  permission

def del_permission(permission_id):
    assert permission_id
    permission_DB.permission.remove({'_id':permission_id})

def find_permissions(filters={}):
    permissions=[]
    items=permission_DB.permission.find(filters)
    if items:
        for item in items:
            permissions.append(permission(item))
        return permissions

def init_perms():
    p=Permission()
    containers={'usermanage':['userauth']}
    apps={'userauth':['user','group','permission']}
    ops=['add','modify','delete']
    for k,v in containers:
        container=k
        app_labels=v
        for app_label in app_labels:
            model_labels=apps.get(app_label)
            for model_label in model_labels:
                for op in ops:
                    p.perm_name=op+'_'+model_labels
                    p.perm_profile='can '+op+' '+model_label
                    p.container=container
                    p.app_label=app_label
                    p.model_label=model_label
                    p.operator=op
                    save_permission(p)

