import os
import subprocess
import json
import rcon
import mcrcon
from mcdreforged.api.types import PluginServerInterface, PlayerCommandSource, CommandSource
from mcdreforged.api.command import Literal

def get_json_location(server: PluginServerInterface):
    return os.path.join(server.get_data_folder(), 'mirror_server_sync.json')

def qb_make(server: PluginServerInterface, src: CommandSource):
    pass

def qb_back(server: PluginServerInterface, src: CommandSource):
    pass

def qb_list(server: PluginServerInterface, src: CommandSource):
    pass

def rcon_connect(server: PluginServerInterface, src: CommandSource):
    pass


def open_json(server: PluginServerInterface):
    global main_server_dir,main_server_ip,mirror_server_dir,world_name
    try:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'r') as json_file:
            data = json.load(json_file)
            main_server_dir = data["main_server_dir"]
            mirror_server_dir = data["mirror_server_dir"]
            main_server_ip = data["main_server_ip"]
            world_name = data["world_name"] 
            return main_server_dir,main_server_ip,mirror_server_dir,world_name
    except:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'w') as json_file:
            json_file.write('''
{
    "main_server_ip": "",
    "world_name": "",
    "main_server_dir": "/root/my_mcdr_server/server",
    "mirror_server_dir": "/root/my_mcdr_server/server",
}
            ''')
            
        

def sync_world(main_server_dir, mirror_server_dir, main_server_ip, world_name):
    command_rsync = "rsync -avPz --progress {0}:{1}/{3} {2}".format(main_server_ip, main_server_dir, mirror_server_dir, world_name)
    cmd_content = subprocess.run(command_rsync,shell="True")
    print(cmd_content)

# 显示用法
# !!msync 显示用法
# !!msync peek 查看主服务器qb最新存档信息
# !!msync sync 备份当前镜像服存档，并同步主服务器qb最新存档
# !!msync recover 回档至同步前存档
# 所有操作需要权限等级2
def show_help(src: CommandSource):
    # TODO 在src中显示上面的注释信息
    return None

def do_nothing():
    pass

def show_permission_fail(src: CommandSource):
    # TODO 在src中显示权限不足信息
    return None

# 确认权限等级
def permission_check(src: CommandSource):
    return src.has_permission(2)

# 注册指令树
def register_commands(server: PluginServerInterface,src: CommandSource):
    server.register_command(
        Literal('!!msync').requires(src.has_permission(4)).runs(show_help())
        .then(
            Literal({"peek","-p","p"})
            .requires(permission_check, show_permission_fail)
            .runs(qb_list())
        )
        .then(
            Literal({"sync","s","-s"})
            .requires(permission_check, show_permission_fail)
            .runs(sync_world(main_server_dir=main_server_dir,main_server_ip=main_server_ip,world_name=world_name,mirror_server_dir=mirror_server_dir)) #啊吧啊吧皮这一下很开心
        )
        .then(
            Literal({"recover","r","-r"})
            .requires(permission_check, show_permission_fail)
            .runs(qb_back())
        )
        .then(
            Literal({"help","h","-h"})
            .requires(permission_check, show_permission_fail)
            .runs(show_help())
        )
    )

def on_load(server: PluginServerInterface, old):
    open_json(server)
    register_commands(server)