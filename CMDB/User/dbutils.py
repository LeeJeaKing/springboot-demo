'''# 1.导入模块'''
from django.db import connection
import traceback

class DBConnection(object):
    @classmethod
    def execute_mysql(cls,sql,args=(),fetch=True,one=False):
        cnt,result = 0 ,None
        conn,cur = None,None
        try:
            cur = connection.cursor()
            cnt = cur.execute(sql,args)
            if fetch:
                result = cur.fetchone() if one else cur.fetchall()
            else:
                connection.commit()
        except BaseException as e:
            print(e)
            print(traceback.format_exc())
        finally:
            if cur:
                cur.close()

        return cnt,result