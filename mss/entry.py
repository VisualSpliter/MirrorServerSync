import subprocess
import json

from mcdreforged.api.types import PluginServerInterface, PlayerCommandSource
from mcdreforged.api.command import Literal

json_file_pos = "../Mirror_Server_Sync.json"

with open(json_file_pos) as json_file:
    data = json.load(json_file)
    main_server_dir = data["main_server_dir"]
    mirror_server_dir = data["mirror_server_dir"]
    main_server_ip = data["main_server_ip"]
    world_name = data["world_name"]

def sync_world(main_server_dir, mirror_server_dir, main_server_ip, world_name):
    command_rsync = "rsync -avPz --progress {0}:{1}+{3} {2}".format(main_server_ip, main_server_dir, mirror_server_dir, world_name)
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

def show_permission_fail(src: CommandSource):
    # TODO 在src中显示权限不足信息
    return None

# 确认权限等级
def permission_check(src: CommandSource):
    return src.has_permission(2):

# 注册指令树
def register_commands(server: PluginServerInterface):
    server.register_command(
        Literal('!!msync')
        .then(
            Literal("peek")
            .requires(permission_check, show_permission_fail)
            .runs()
        )
        .then(
            Literal("sync")
            .requires(permission_check, show_permission_fail)
            .runs()
        )
        .then(
            Literal("recover")
            .requires(permission_check, show_permission_fail)
            .runs()
        )
    ).runs(show_help)

def on_load(server: PluginServerInterface, old):
    register_commands(server)