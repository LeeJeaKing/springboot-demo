from .models import User
from django.utils import timezone

class Validator():
    @classmethod
    def is_integer(cls,value):
        try:
            int(value)
            return True
        except BaseException as e:
            return False


class UserValiator(Validator):
    @classmethod
    def valid_login(cls, name, password):
        user = User.objects.filter(name=name).first()
        if user is None:
            return None
        if user.password == password:
            return user
        return None

    @classmethod
    def valid_name_unique(cls, name, uid=None):
        user = User.objects.filter(name=name).first()
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
    def valid_update(cls, params):
        is_valid = True
        user = User.objects.filter(id=params.get('uid', '').strip()).first()
        errors = {}

        if User.objects.get(id=user.id) is None:
            errors['uid'] = '用户信息不存在'
            is_valid = False

        name = params.get('name', '').strip()

        if name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False

        if not cls.valid_name_unique(name, user.id):
            errors['name'] = '用户名已存在'
            is_valid = False
        else:
            user.name = name

        age = params.get('age', '').strip()
        if not cls.is_integer(age):
            errors['age'] = '年龄格式错误'
            is_valid = False
        else:
            user.age = int(age)

        user.tel = params.get('tel', '0').strip()
        user.sex = int(params.get('sex', '0').strip())
        return is_valid, user, errors

    @classmethod
    def valid_create(cls, params):
        is_valid = True
        user = User()
        errors = {}

        user.name = params.get('name', '').strip()

        if user.name == '':
            errors['name'] = '用户名不能为空'
            is_valid = False
        else:
            if User.objects.filter(name=user.name).first():
                is_valid = False
                errors['name'] = '用户名已存在'

        user.age = params.get('age', '').strip()
        user.tel = params.get('tel', '0').strip()
        user.sex = int(params.get('sex', '0').strip())
        user.password = str(params.get('password', '').strip())
        user.create_time = timezone.now()

        return is_valid, user, errors