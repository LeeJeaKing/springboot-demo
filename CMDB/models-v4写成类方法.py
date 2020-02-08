from django.db import models
import json
# Create your models here.
from .dbutils import DBConnection


class User():
    SQL_LOGIN = 'SELECT id,name,age,tel,sex FROM user2 where name=%s and password=%s LIMIT 1'
    SQL_LIST = 'SELECT id,name,age,tel,sex FROM user2'
    SQL_GET_USER_BY_ID = 'SELECT id,name,age,tel,sex FROM user2 WHERE id=%s'
    SQL_GET_USER_BY_NAME = 'SELECT id,name FROM user2 WHERE name=%s'
    SQL_UPDATE_USER = 'UPDATE user2 SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s'
    SQL_DELETE_USER = 'DELETE FROM user2 WHERE id=%s'
    SQL_CREATE_USER = 'INSERT INTO user2(name,password,age,tel,sex) VALUES(%s,%s,%s,%s,%s)'

    def __init__(self,id=None,name='',age=0,tel='',sex=1,password=''):
        self.id = id
        self.name = name
        self.age = age
        self.tel = tel
        self.sex = sex
        self.password = password

    @classmethod
    def valid_login(cls,name,password):
        '''
            类方法，
        '''
        cnt, result = DBConnection.execute_mysql(sql=cls.SQL_LOGIN, args=(name, password), fetch=True, one=True)

        return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4]) if result else None


    @classmethod
    def get_list(cls): #登录后拿用户列表
        cnt,result = DBConnection.execute_mysql(sql=cls.SQL_LIST,fetch=True,one=False)
        #查到用户，返回一个实例
        return [User(id=line[0], name=line[1], age=line[2], tel=line[3], sex=line[4]) for line in result]


    @classmethod
    def get_by_id(cls,uid): #拿用户信息进行编辑
        cnt, result = DBConnection.execute_mysql(sql=cls.SQL_GET_USER_BY_ID, args=(uid), fetch=True, one=True)
        return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4]) if result else False

    @classmethod
    def get_user_by_name(cls,name):
        cnt, result = DBConnection.execute_mysql(sql=cls.SQL_GET_USER_BY_NAME, args=(name,), fetch=True, one=True)
        return User(id=result[0],name=result[1]) if result else False

    @classmethod
    def valid_name_unique(cls,name,uid=None):
        user = cls.get_user_by_name(name)
        if not user:
            return True
        if uid is None:  # 创建新用户时判断
            return not user
        else:  # 更新时判断
            if user is None:  # 没有重复user返回True
                return True
            else:
                return str(user.id) == str(uid)  # 有重复用户，但是当前用户是返回True


    @classmethod
    def valid_update(cls,params):
        is_valid = True
        user = User()
        errors = {}

        user.id = params.get('uid', '').strip()
        if user.id is None:
            errors['uid'] = '用户信息不存在'
            is_valid = False

        user.name = params.get('name', '').strip()

        if user.name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False

        if not cls.valid_name_unique(user.name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False

        user.age = params.get('age', '').strip()
        user.tel = params.get('tel', '0').strip()
        user.sex = int(params.get('sex', '0').strip())
        return is_valid, user, errors


    def update(self):
        cnt, result = DBConnection.execute_mysql(sql=self.SQL_UPDATE_USER, args=(
            self.name, self.age, self.tel, self.sex, self.id), fetch=False)
        return True


    @classmethod
    def delete_by_id(cls,uid):
        cnt, result = DBConnection.execute_mysql(sql=cls.SQL_DELETE_USER, args=(uid,), fetch=False)
        return True


    @classmethod
    def valid_create(cls,params):
        is_valid = True
        user = User()
        errors = {}

        user.name = params.get('name', '').strip()

        if user.name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False
        else:
            if cls.get_user_by_name(user.name):
                is_valid = False
                errors['name'] = '用户名已存在'

        user.age = params.get('age', '').strip()
        user.tel = params.get('tel', '0').strip()
        user.sex = int(params.get('sex', '0').strip())
        user.password = str(params.get('password', '').strip())

        return is_valid, user, errors

    def create(self):
        cnt, result = DBConnection.execute_mysql(sql=self.SQL_CREATE_USER,
                                                 args=(self.name, self.password, self.age, self.tel,self.sex),
                                                 fetch=False)

        return True


    def as_dict(self): #字典类用于存放session
        return {'id':self.id,
                'name':self.name,
                'age':self.age,
                'tel':self.tel,
                'sex':self.sex,
                'password':self.password
                }













# def get_users():
#     cnt,result = DBConnection.execute_mysql(sql=SQL_LIST,fetch=True,one=False)
#
#     #print([dict(zip(['id','name','age','tel','sex'],line)) for line in result]) 使用zip方式
#
#     return [{'id':line[0],'name':line[1],'age':line[2],'tel':line[3],'sex':line[4]} for line in result] #列表推导式
#     #[{'sex': 1, 'id': 1, 'tel': '123456', 'name': 'kk', 'age': 30}, {'sex': 1, 'id': 2, 'tel': '123456', 'name': 'kk1', 'age': 30}]


# def valid_login(name,password):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_LOGIN,args=(name,password), fetch=True, one=True)
#
#     if result:
#         return {'id':result[0],
#                 'name':result[1]}
#     return None


# def delete_user(uid):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_DELETE_USER,args=(uid,) ,fetch=False)
#     return True


# def get_user(uid):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_GET_USER_BY_ID, args=(uid), fetch=True, one=True)
#     return dict(zip(['id', 'name', 'age', 'tel', 'sex'], result)) if result else False


# #判断用户名是否存在
# def get_user_by_name(name):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_GET_USER_BY_NAME, args=(name,), fetch=True, one=True)
#     return dict(zip(['id', 'name', 'age', 'tel', 'sex'], result)) if result else False


# def valid_name_unique(name,uid=None):
#     user = get_user_by_name(name)
#     if not user:
#         return True
#     if uid is None: #创建新用户时判断
#         return not user
#     else:#更新时判断
#         if user is None: #没有重复user返回True
#             return True
#         else:
#             return  str(user['id']) == str(uid) #有重复用户，但是当前用户是返回True


# def valid_update_user(params):
#     is_valid = True
#     user = {}
#     errors = {}
#
#     user['id'] = params.get('uid', '').strip()
#     if get_user(user['id']) is None:
#         errors['uid'] = '用户信息不存在'
#         is_valid = False
#
#     user['name'] = params.get('name', '').strip()
#
#     if  user['name'] == '':
#         errors['name'] = '用户名不能为空'
#         is_valid = False
#
#     if not valid_name_unique(user['name'],user['id']):
#         errors['name'] = '用户名已存在'
#         is_valid = False
#
#     user['age'] = params.get('age', '').strip()
#     user['tel'] = params.get('tel', '0').strip()
#     user['sex'] = int(params.get('sex', '0').strip())
#     print(errors)
#     return is_valid,user,errors

#
# def update_user(params):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_UPDATE_USER, args=(params['name'],params['age'],params['tel'],params['sex'],params['id']), fetch=False)
#     return True



# def valid_create_user(params):
#     is_valid = True
#     user = {}
#     errors = {}
# 
#     user['name'] = params.get('name', '').strip()
# 
#     if user['name'] == '':
#         errors['name'] = '用户名不能为空'
#         is_valid = False
#     else:
#         if get_user_by_name(user['name']):
#             is_valid = False
#             errors['name'] = '用户名已存在'
# 
#     user['age'] = params.get('age', '').strip()
#     user['tel'] = params.get('tel', '0').strip()
#     user['sex'] = int(params.get('sex', '0').strip())
#     user['password'] = int(params.get('password', '').strip())
# 
#     return is_valid, user, errors
# 
# 
# def create_user(params):
#     cnt, result = DBConnection.execute_mysql(sql=SQL_CREATE_USER,
#                                 args=(params['name'], params['password'],params['age'], params['tel'], params['sex']),
#                                 fetch=False)
# 
#     return True