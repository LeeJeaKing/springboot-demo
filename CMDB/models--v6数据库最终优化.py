from django.db import models
import json
# Create your models here.
from .dbutils import DBConnection

class User():
    SQL_LOGIN = 'SELECT id,name,age,tel,sex FROM user2 where name=%s and password=%s LIMIT 1'
    SQL_LIST = 'SELECT id,name,age,tel,sex FROM user2'
    SQL_GET_USER_BY_ID = 'SELECT id,name,age,tel,sex FROM user2 WHERE id=%s'
    SQL_GET_USER_BY_NAME = 'SELECT id,name,age,tel,sex,password FROM user2 WHERE name=%s'
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
        return User(id=result[0],name=result[1],age=result[2],tel=result[3],sex=result[4],password=result[5]) if result else False


    def update(self):
        cnt, result = DBConnection.execute_mysql(sql=self.SQL_UPDATE_USER, args=(
            self.name, self.age, self.tel, self.sex, self.id), fetch=False)
        return True


    @classmethod
    def delete_by_id(cls,uid):
        cnt, result = DBConnection.execute_mysql(sql=cls.SQL_DELETE_USER, args=(uid,), fetch=False)
        return True


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




