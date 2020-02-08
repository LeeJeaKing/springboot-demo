import json
import shutil
from ansible.module_utils.common.collections import ImmutableDict
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
from ansible import context
import ansible.constants as C


'''
回调
'''
class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        # print(result.task_name)
        print(result._result)


#connection='local' 连接    forks=10 并发    become_user 提权
context.CLIARGS = ImmutableDict(connection='local', module_path=['/to/mymodules'], forks=10, become=None,
                                become_method=None, become_user=None, check=False, diff=False)


#加载剧本
loader = DataLoader() # Takes care of finding and reading yaml, json and ini files
passwords = {} #dict(vault_pass='secret') #加密剧本，可不用

results_callback = ResultCallback() #ResultCallback的实例

inventory = InventoryManager(loader=loader, sources='hosts') #剧本的位置

variable_manager = VariableManager(loader=loader, inventory=inventory)

# ansible all -i etc/hosts -m setup
play_source =  {
        'name' : "test",
        'hosts' : 'all',
        'gather_facts' : 'no', #对应 setup
        'tasks' : [
            {
                'name':'fact', #任务名称
                'setup':'' #执行模块
             },
         ]
    }


play = Play().load(play_source, variable_manager=variable_manager, loader=loader)


tqm = None
try:
    tqm = TaskQueueManager(
              inventory=inventory,
              variable_manager=variable_manager,
              loader=loader,
              passwords=passwords,
              stdout_callback=results_callback,  # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
          )
    result = tqm.run(play) # most interesting data for a play is actually sent to the callback's methods
finally: #不管成功与否都执行
    if tqm is not None:
        tqm.cleanup()

    shutil.rmtree(C.DEFAULT_LOCAL_TMP, True) #删除临时文件