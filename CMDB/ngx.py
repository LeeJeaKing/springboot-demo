''''''

'''
使用Py生成nginx模板文件
'''

# tpl = """
# {{
#     host:{HOST};
#     port:{PORT};
# }}
# """
# conf = tpl.format(HOST='192.168.56.1',PORT='8080')
#
# with open('ngx.conf','w') as f:
#     f.write(conf)