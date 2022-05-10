from configparser import RawConfigParser
import os
import subprocess
import json
from mcdreforged.api.types import PluginServerInterface, CommandSource, Info
from mcdreforged.api.command import Literal
from mcdreforged.api.rcon import RconConnection
from mcdreforged.api.rtext import *

#some message
backup_message = RText("要备份嘞",color=RColor.gold)
nizaiganshenme = RText("李在赣神麽？",color=RColor.red)
attenetion_message = RText("手头东西停一停，机器停一停",color=RColor.gold)
obfuscated_text = RText("111111111111111111111",color=RColor.red,styles=RStyle.obfuscated)

def get_json_location(server: PluginServerInterface):
    return os.path.join(server.get_data_folder(), 'mirror_server_sync.json')

def qb_make(server: PluginServerInterface, src: CommandSource, info: Info):
    while src.has_permission_higher_than(2) == True:
        server.execute_command("!!qb make BeforeSyncBackup")
        server.say(RText.to_json_str(backup_message))
        server.say(RText.to_json_str(attenetion_message))
    while src.has_permission_higher_than(2) == False:
        server.reply(info.get_command_source(),nizaiganshenme)
        server.reply(info.get_command_source(),obfuscated_text)

def qb_back(server: PluginServerInterface, src: CommandSource):
    pass

def qb_list(server: PluginServerInterface):
    back_up_list = minecraft_rcon.command("!!qb list")
    server.logger.info(back_up_list)

def rcon_connect(server:PluginServerInterface,mcrcon: RconConnection):
    global minecraft_rcon
    minecraft_rcon = mcrcon(main_server_ip,rcon_password,int(rcon_port))
    minecraft_rcon.connect()
    server.logger.info("RCON Connected IP:{0} Port:{1}".format(main_server_ip,rcon_port))


def open_json(server: PluginServerInterface):
    global main_server_dir,main_server_ip,mirror_server_dir,world_name
    global rcon_port,rcon_password
    try:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'r') as json_file:
            data = json.load(json_file)
            main_server_dir = data["main_server_dir"]
            mirror_server_dir = data["mirror_server_dir"]
            main_server_ip = data["main_server_ip"]
            world_name = data["world_name"] 
            rcon_port = data["rcon_port"]
            rcon_password = data["rcon_password"]
    except:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'w') as json_file:
            json_file.write('''
{
    "main_server_ip": "127.0.0.1",
    "world_name": "world",
    "main_server_dir": "/root/my_mcdr_server/server",
    "mirror_server_dir": "/root/my_mcdr_server/server",
    "rcon_password": "123456",
    "rcon_port": "25575",
    "qb_folder_dir": "/root/my_mcdr_server/qb_multi"
}''')
        open_json(server)

            
def stop_sync_start(server: PluginServerInterface):
# TODO stop server, sync the folder, start server and good to go
    pass #先pass，一会来写
#How To You Fix The Command?
#I commented it :-P

        

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
def show_help(server:PluginServerInterface, src: CommandSource):
    while src.has_permission(2) == True:
        server.logger.info()
    # TODO 在src中显示上面的注释信息
    return None

# def do_nothing(server: PluginServerInterface):
#     server.load_config_simple()

def show_permission_fail(src: CommandSource):
    # TODO 在src中显示权限不足信息
    return None

# 确认权限等级
def permission_check(src: CommandSource):
    return src.has_permission(2)

# 注册指令树
def register_commands(server: PluginServerInterface, src: CommandSource):
    server.register_command(
        Literal('!!msync').requires(permission_check,show_permission_fail).runs(show_help)
        .then(
            Literal({"peek","-p","p"})
            .requires(permission_check, show_permission_fail)
            .runs(json_sync)
        )
        .then(
            Literal({"sync","s","-s"})
            .requires(permission_check, show_permission_fail)
            .runs(sync_world) #啊吧啊吧皮这一下很开心
        )
        .then(
            Literal({"recover","r","-r"})
            .requires(permission_check, show_permission_fail)
            .runs(do_nothing)
        )
        .then(
            Literal({"help","h","-h"})
            .requires(permission_check, show_permission_fail)
            .runs(do_nothing)
        )
    )

def on_load(server: PluginServerInterface, old):
    src = CommandSource
    mcrcon = RconConnection
    open_json(server)
    rcon_connect(server,mcrcon)
    register_commands(server,src)