from django.core.management import BaseCommand
import json
import shutil
from collections import namedtuple
from ansible.parsing.dataloader import DataLoader
from ansible.vars.manager import VariableManager
from ansible.inventory.manager import InventoryManager
from ansible.playbook.play import Play
from ansible.executor.task_queue_manager import TaskQueueManager
from ansible.plugins.callback import CallbackBase
import ansible.constants as C
import os
from django.conf import settings
from asset.models import Host

'''
回调
'''
class ResultCallback(CallbackBase):
    def v2_runner_on_ok(self, result, **kwargs):
        # print(result.task_name)
        # print(result._host.name)
        # print(result._result)
        if result.task_name == 'collect_host': #如果任务名称是collect_host 则调用collect_host
            self.collect_host(result._result)


    def collect_host(self,result):
        facts = result.get('ansible_facts',{})
        ip = facts.get('ansible_default_ipv4',{}).get('address','')
        name = facts.get('ansible_nodename','')
        mac = facts.get('ansible_default_ipv4',{}).get('macaddress','')
        os = facts.get('ansible_os_family','')
        arch = facts.get('ansible_architecture','')
        mem = facts.get('ansible_memtotal_mb','')
        cpu = facts.get('ansible_processor_vcpus','')
        disk = [ {'name':i.get('device'),'total':int(i.get('size_total'))/1048576} for i in facts.get('ansible_mounts',[])]
        disk = json.dumps(disk)

        Host.create_or_replace(ip,name,mac,os,arch,mem,cpu,disk)



class Command(BaseCommand):
    def handle(self, *args, **options):

        # connection='local' 连接    forks=10 并发    become_user 提权
        AnsibleOptions = namedtuple('AnsibleOptions',
                             ['connection', 'module_path', 'forks', 'become', 'become_method', 'become_user', 'check',
                              'diff'])
        ansible_options = AnsibleOptions(connection='smart', module_path=[], forks=10, become=None, become_method=None,
                          become_user=None, check=False, diff=False)



        # 加载剧本
        loader = DataLoader()  # Takes care of finding and reading yaml, json and ini files
        passwords = {}  # dict(vault_pass='secret') #加密剧本，可不用

        results_callback = ResultCallback()  # ResultCallback的实例

        inventory = InventoryManager(loader=loader, sources=os.path.join(settings.BASE_DIR,'etc','hosts'))  # 剧本的位置 sources=os.path.join(settings.BASE_DIR,'etc','hosts')

        variable_manager = VariableManager(loader=loader, inventory=inventory)

        # ansible all -i etc/hosts -m setup
        play_source = {
            'name': "cmdb",
            'hosts': 'all',
            'gather_facts': 'no',  # 对应 setup
            'tasks': [
                {
                    'name': 'collect_host',  # 任务名称 对应task_name
                    'setup': ''  # 执行模块
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
                options = ansible_options,
                passwords=passwords,
                stdout_callback=results_callback,
                # Use our custom callback instead of the ``default`` callback plugin, which prints to stdout
            )
            result = tqm.run(play)  # most interesting data for a play is actually sent to the callback's methods
        finally:  # 不管成功与否都执行
            if tqm is not None:
                tqm.cleanup()

            shutil.rmtree(C.DEFAULT_LOCAL_TMP, True)  # 删除临时文件