import json
'''读取用户信息'''
users = {}
# with open('test.txt','r') as f:
#     for line in f:
#         nodes = line.strip().split(',')
#         if len(nodes) == 4: #判断是否有密码
#             users[int(nodes[0])] = {'name':nodes[1],'age':int(nodes[2]),'tel':nodes[3],'password':''}
#         else:
#             users[int(nodes[0])] = {'name': nodes[1], 'age': int(nodes[2]), 'tel': nodes[3], 'password': nodes[4]}

DATA_FILE = 'user.data.json'
DISPLAY_TPL = '|{uid:10d}|{password:20s}|{name:10s}|{age:5s}|{tel:20s}|' #输出读取模板


def load_data():
    """
        读取数据文件并反序列化为dict
    :return:
    """
    with open(DATA_FILE,'r') as f:
        cxt = f.read()
        users = json.loads(cxt)
        return {int(key):value for key,value in users.items()} #{1: {'age': '30', 'password': '123', 'tel': '123', 'name': 'kk'}}  可为数字


def save_data(users):
    """
        序列化users为字符串，并存储到文件
    """
    with open(DATA_FILE,'w') as f:
        f.write(json.dumps(users))
        return True


def login():
    users = load_data()
    isLogin = False
    for _ in range(3):
        txt = input('请输入用户名和密码(user/password):')
        username, password = txt.strip().split('/')

        for user in users.values():
            if user['name'] == username and user['password'] == password:
                isLogin = True
                break
        if not isLogin:
            print('用户名或密码错误')
        else:
            break

    return isLogin


def input_add_user():
    is_valid = False
    user = {}
    text = input('请输入用户信息,(示例:name,age,tel,password):')
    nodes = text.split(',')
    if len(nodes) != 4:
        print('输入信息有误,请重新输入')
    else:
        if not nodes[1].isdigit():
            print('输入年龄有误,请重新输入')
        else:
            user = {'name': nodes[0],
                      'age': int(nodes[1]),
                      'tel': nodes[2],
                      'password': nodes[3]}
            is_valid = True
    return is_valid,user


def add_user():
    is_valid,user = input_add_user()
    if is_valid:
        users = load_data()
        uid = 1
        if users:
            uid = max(users) + 1
        users[uid] = user
        save_data(users)
        print('添加成功')


def input_delete_user():
    is_valid = False
    uid = input('请输入删除用户ID:')
    if not uid.isdigit():
        print('输入信息有误')
    else:
        is_valid = True
        uid = int(uid)
    return is_valid,uid

def delete_user():
    is_valid, uid = input_delete_user()
    if is_valid:
        users = load_data()
        users.pop(int(uid), None)
        save_data(users)
        print('删除成功')


def input_update_user():
    users = load_data()
    is_valid = False
    user = {}
    uid = input('请输入编辑用户ID:')
    if not uid.isdigit():
        print('输入信息有误')
    elif int(uid) not in users:
        print('输入信息有误')
    else:
        text = input('请输入用户信息,(示例:age,tel,password):')
        nodes = text.split(',')
        if len(nodes) != 3:
            print('输入信息有误,请重新输入')
        else:
            if not nodes[0].isdigit():
                print('输入年龄有误,请重新输入')
            else:
                is_valid = True
                uid = int(uid)
                user = {'age': int(nodes[0]),
                        'tel': nodes[1],
                        'password': nodes[2]}
    return is_valid,uid,user


def update_user():
    is_valid,uid,user = input_update_user()

    if is_valid:
        users = load_data()
        users[uid].update(user)
        save_data(users)
        print('更改成功')


def list_user():
    users = load_data()
    for key, value in users.items():
        print(DISPLAY_TPL.format(uid=key, name=value['name'], age=value['age'], tel=value['tel'],
                         password=len(value['password']) * '*'))

def find_user():
    users = load_data()
    text = input('请输入查询的字符串:')
    for key, value in users.items():
        if text in value['name']:
            print(DISPLAY_TPL.format(uid=key, name=value['name'], age=value['age'], tel=value['tel'],
                             password=len(value['password']) * '*'))

def main():
    '''
        主程序入口
    '''
    login_tag = login()

    if not login_tag:
        print('登录失败')
        return

    actions = {
        'add':add_user,
        'delete':delete_user,
        'update':update_user,
        'list':list_user,
        'find':find_user,
        'exit':save_data,
    }

    while True:
        operate =  input('请输入操作(add/delete/update/find/list/exit):')
        if operate == 'exit':
            break
        func = actions.get(operate,None) #通过用户输入，在actions字典内找对应函数
        if not func:
            print('输入有误请重新输入')
            continue
        func()


if __name__ == '__main__':
    main()