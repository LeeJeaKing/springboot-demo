from django.db import models
import json
# Create your models here.
DATA_FILE = 'user.data.json'

'''# 1.导入模块'''
import pymysql
MYSQL_HOST='192.168.56.51'
MYSQL_USER='root'
MYSQL_PASSWORD='123456'
MYSQL_DATABASE='cmdb_kk'
MYSQL_PORT=3306
MYSQL_CHARSET='utf8'

SQL_LOGIN = 'SELECT id,name,age,tel,sex FROM user2 where name=%s and password=%s LIMIT 1'
SQL_LIST = 'SELECT id,name,age,tel,sex FROM user2'
SQL_GET_USER_BY_ID = 'SELECT id,name,age,tel,sex FROM user2 WHERE id=%s'
SQL_GET_USER_BY_NAME = 'SELECT id,name FROM user2 WHERE name=%s'
SQL_UPDATE_USER = 'UPDATE user2 SET name=%s,age=%s,tel=%s,sex=%s WHERE id=%s'
SQL_CREATE_USER = 'INSERT INTO user2(name,password,age,tel,sex) VALUES(%s,%s,%s,%s,%s)'
SQL_DELETE_USER = 'DELETE FROM user2 WHERE id=%s'

def get_users():
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_LIST)  # 查询是否存在用户
    result = cur.fetchall()
    cur.close()
    conn.close()

    #print([dict(zip(['id','name','age','tel','sex'],line)) for line in result]) 使用zip方式

    return [{'id':line[0],'name':line[1],'age':line[2],'tel':line[3],'sex':line[4]} for line in result] #列表推导式
    #[{'sex': 1, 'id': 1, 'tel': '123456', 'name': 'kk', 'age': 30}, {'sex': 1, 'id': 2, 'tel': '123456', 'name': 'kk1', 'age': 30}]




def dump_users(users):
    with open(DATA_FILE,'w') as f:
        f.write(json.dumps(users))
        return True


def valid_login(name,password):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_LOGIN,(name,password)) #查询是否存在用户
    result = cur.fetchone()
    cur.close()
    conn.close()
    if result:
        return {'id':result[0],
                'name':result[1]}
    return None



def delete_user(uid):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_DELETE_USER, (uid,))  # 查询是否存在用户
    conn.commit()
    cur.close()
    conn.close()
    return True


def get_user(uid):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_GET_USER_BY_ID,(uid,))  # 查询是否存在用户
    result = cur.fetchone()
    cur.close()
    conn.close()

    return dict(zip(['id', 'name', 'age', 'tel', 'sex'], result)) if result else False


#判断用户名是否存在
def get_user_by_name(name):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_GET_USER_BY_NAME, (name,))  # 查询是否存在用户
    result = cur.fetchone()
    cur.close()
    conn.close()
    return dict(zip(['id', 'name', 'age', 'tel', 'sex'], result)) if result else False


def valid_name_unique(name,uid=None):
    user = get_user_by_name(name)
    if not user:
        return True
    if uid is None: #创建新用户时判断
        return not user
    else:#更新时判断
        if user is None: #没有重复user返回True
            return True
        else:
            return  str(user['id']) == str(uid) #有重复用户，但是当前用户是返回True


def valid_update_user(params):
    is_valid = True
    user = {}
    errors = {}

    user['id'] = params.get('uid', '').strip()
    if get_user(user['id']) is None:
        errors['uid'] = '用户信息不存在'
        is_valid = False

    user['name'] = params.get('name', '').strip()

    if  user['name'] == '':
        errors['name'] = '用户名不能为空'
        is_valid = False

    if not valid_name_unique(user['name'],user['id']):
        errors['name'] = '用户名已存在'
        is_valid = False

    user['age'] = params.get('age', '').strip()
    user['tel'] = params.get('tel', '0').strip()
    user['sex'] = int(params.get('sex', '0').strip())
    print(errors)
    return is_valid,user,errors


def update_user(params):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_UPDATE_USER, (params['name'],params['age'],params['tel'],params['sex'],params['id']))  # 查询是否存在用户
    conn.commit()
    cur.close()
    conn.close()
    return True



def valid_create_user(params):
    is_valid = True
    user = {}
    errors = {}

    user['name'] = params.get('name', '').strip()

    if user['name'] == '':
        errors['name'] = '用户名不能为空'
        is_valid = False
    else:
        if get_user_by_name(user['name']):
            is_valid = False
            errors['name'] = '用户名已存在'

    user['age'] = params.get('age', '').strip()
    user['tel'] = params.get('tel', '0').strip()
    user['sex'] = int(params.get('sex', '0').strip())
    user['password'] = int(params.get('password', '').strip())

    return is_valid, user, errors


def create_user(params):
    conn = pymysql.connect(
        host=MYSQL_HOST, user=MYSQL_USER, passwd=MYSQL_PASSWORD, database=MYSQL_DATABASE, port=MYSQL_PORT,
        charset=MYSQL_CHARSET
    )
    cur = conn.cursor()
    cur.execute(SQL_CREATE_USER,
                (params['name'], params['password'],params['age'], params['tel'], params['sex']))  # 查询是否存在用户
    conn.commit()
    cur.close()
    conn.close()
    return True