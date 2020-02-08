from django.db import models
import json
# Create your models here.

DATA_FILE = 'user.data.json'

def get_users():
    with open(DATA_FILE,'r') as f:
        cxt = f.read()
        users = json.loads(cxt)
        return users
            #{int(key):value for key,value in users.items()} #{1: {'age': '30', 'password': '123', 'tel': '123', 'name': 'kk'}}  可为数字

def dump_users(users):
    with open(DATA_FILE,'w') as f:
        f.write(json.dumps(users))
        return True


def valid_login(name,password):
    users = get_users()
    for uid,user in users.items():
        if user['name'] == name and user['password'] == password:
            user['id'] = uid
            return user
    return None


def delete_user(uid):
    users = get_users()
    users.pop(uid, None)
    dump_users(users)
    return True


def get_user(uid):
    users = get_users()
    user = users.get(uid,{})
    user['id'] = uid
    return user


def valid_update_user(params):
    is_valid = True
    user = {}
    errors = {}
    users = get_users()

    user['uid'] = params.get('uid', '').strip()
    if users.get(user['uid']) is None:
        errors['uid'] = '用户信息不存在'
        is_valid = False
    user['name'] = params.get('name', '').strip()
    user['age'] = params.get('age', '').strip()
    user['tel'] = params.get('tel', '0').strip()
    user['sex'] = int(params.get('sex', '0').strip())

    return is_valid,user,errors

def update_user(params):
    uid = params.pop('uid')
    users = get_users()
    users[uid].update(params)
    dump_users(users)
    return True