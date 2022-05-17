# At least it works
from http import server
from quopri import decode
import random
import os
import subprocess
import json
from turtle import color
from mcdreforged.api.types import PluginServerInterface, CommandSource, Info
from mcdreforged.api.command import Literal
from mcdreforged.api.rcon import RconConnection
from mcdreforged.api.rtext import *
from numpy import source

#meta data
PLUGIN_METADATA = {
    "id": "mirror_server_sync",
    "version": "0.0.1-alpha",
    "name": "Mirror Server Sync",
    "description":"A Simple MCDR Plugin To Sync Map FIles Of Minecraft On Different Servers",
    "author": [
        "MRNOBODY-ZST",
        "Power-tile"
    ], 
    "link": "https://github.com/VisualSpliter/MirrorServerSync",
    "dependences": {
        "mcdreforged": ">=2.0.0"
    }
}

# some message
backup_message = RText("要备份嘞", color=RColor.gold)
nizaiganshenme = RText("李在赣神麽？", color=RColor.red)
attenetion_message = RText("手头东西停一停，机器停一停", color=RColor.gold)
obfuscated_text = RText("111111111111111111111", color=RColor.red, styles=RStyle.obfuscated)
bruh_img = RText('''⡏⠉⠉⠉⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠋⠉⠉⠉⠉⠉⠉⠉⠉⠉⠉⠙⠉⠉⠉⠹
⡇⢸⣿⡟⠛⢿⣷⠀⢸⣿⡟⠛⢿⣷⡄⢸⣿⡇⠀⢸⣿⡇⢸⣿⡇⠀⢸⣿⡇⠀
⡇⢸⣿⣧⣤⣾⠿⠀⢸⣿⣇⣀⣸⡿⠃⢸⣿⡇⠀⢸⣿⡇⢸⣿⣇⣀⣸⣿⡇⠀
⡇⢸⣿⡏⠉⢹⣿⡆⢸⣿⡟⠛⢻⣷⡄⢸⣿⡇⠀⢸⣿⡇⢸⣿⡏⠉⢹⣿⡇⠀
⡇⢸⣿⣧⣤⣼⡿⠃⢸⣿⡇⠀⢸⣿⡇⠸⣿⣧⣤⣼⡿⠁⢸⣿⡇⠀⢸⣿⡇⠀
⣇⣀⣀⣀⣀⣀⣀⣄⣀⣀⣀⣀⣀⣀⣀⣠⣀⡈⠉⣁⣀⣄⣀⣀⣀⣠⣀⣀⣀⣰
⣇⣿⠘⣿⣿⣿⡿⡿⣟⣟⢟⢟⢝⠵⡝⣿⡿⢂⣼⣿⣷⣌⠩⡫⡻⣝⠹⢿⣿⣷
⡆⣿⣆⠱⣝⡵⣝⢅⠙⣿⢕⢕⢕⢕⢝⣥⢒⠅⣿⣿⣿⡿⣳⣌⠪⡪⣡⢑⢝⣇
⡆⣿⣿⣦⠹⣳⣳⣕⢅⠈⢗⢕⢕⢕⢕⢕⢈⢆⠟⠋⠉⠁⠉⠉⠁⠈⠼⢐⢕⢽
⡗⢰⣶⣶⣦⣝⢝⢕⢕⠅⡆⢕⢕⢕⢕⢕⣴⠏⣠⡶⠛⡉⡉⡛⢶⣦⡀⠐⣕⢕
⡝⡄⢻⢟⣿⣿⣷⣕⣕⣅⣿⣔⣕⣵⣵⣿⣿⢠⣿⢠⣮⡈⣌⠨⠅⠹⣷⡀⢱⢕
⡝⡵⠟⠈⢀⣀⣀⡀⠉⢿⣿⣿⣿⣿⣿⣿⣿⣼⣿⢈⡋⠴⢿⡟⣡⡇⣿⡇⡀⢕
⡝⠁⣠⣾⠟⡉⡉⡉⠻⣦⣻⣿⣿⣿⣿⣿⣿⣿⣿⣧⠸⣿⣦⣥⣿⡇⡿⣰⢗⢄
⠁⢰⣿⡏⣴⣌⠈⣌⠡⠈⢻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣬⣉⣉⣁⣄⢖⢕⢕⢕
⡀⢻⣿⡇⢙⠁⠴⢿⡟⣡⡆⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣷⣵⣵⣿
⡻⣄⣻⣿⣌⠘⢿⣷⣥⣿⠇⣿⣿⣿⣿⣿⣿⠛⠻⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿
⣷⢄⠻⣿⣟⠿⠦⠍⠉⣡⣾⣿⣿⣿⣿⣿⣿⢸⣿⣦⠙⣿⣿⣿⣿⣿⣿⣿⣿⠟
⡕⡑⣑⣈⣻⢗⢟⢞⢝⣻⣿⣿⣿⣿⣿⣿⣿⠸⣿⠿⠃⣿⣿⣿⣿⣿⣿⡿⠁⣠
⡝⡵⡈⢟⢕⢕⢕⢕⣵⣿⣿⣿⣿⣿⣿⣿⣿⣿⣶⣶⣿⣿⣿⣿⣿⠿⠋⣀⣈⠙
⡝⡵⡕⡀⠑⠳⠿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⣿⠿⠛⢉⡠⡲⡫⡪⡪⡣''')
help_message = RText('''!!msync 显示用法\n!!msync peek 查看主服务器qb最新存档信息\n!!msync sync 备份当前镜像服存档并同步主服务器qb最新存档\n!!msync recover 回档至同步前存档\n!!msync help 显示用法''',color=RColor.white)


#just a little test
def get_json_location(server: PluginServerInterface):
    return os.path.join(server.get_data_folder(), 'mirror_server_sync.json')


def qb_make(server: PluginServerInterface, src: CommandSource):
    random_number = random.randint(0, 100)
    if src.has_permission_higher_than(2):
        # server.execute_command("!!qb make BeforeSyncBackup")
        src.reply(backup_message)
        src.reply(attenetion_message)
        src.reply(bruh_img)
    if not src.has_permission_higher_than(2):
        random_number = random.randint(0,1)
        if random_number == 0:
            src.reply(nizaiganshenme)
        if random_number == 1:
            src.reply(obfuscated_text)


def sync_json(server:PluginServerInterface,src: CommandSource):
    server.reply("Start Sync Json")
    for i in range(1, number_of_qb_slots + 1):
        json_sync_command = "rsync -avPz --progress {0}:{1}/slot{3}/*.json {2}/slot{3}".format(main_server_ip, qb_folder_dir_main, qb_folder_dir_mirror,i)
        src.reply(json_sync_command)
        cmd_content = subprocess.Popen(json_sync_command, shell="True" , stdout=subprocess.PIPE)
        lines = []
        for line in iter(cmd_content.stdout.readline, b''):
            line = line.strip().decode("GB2312")
            server.logger.info(line)
            lines.append(line)

def json_sync(server: PluginServerInterface, src: CommandSource):
    if src.has_permission_higher_than(2):
        sync_json(server,src)
    if not src.has_permission_higher_than(2):
        random_number = random.randint(0,1)
        if random_number == 0:
            src.reply(nizaiganshenme)
        if random_number == 1:
            src.reply(obfuscated_text)



# def qb_back(server: PluginServerInterface, src: CommandSource):
#     pass
# def qb_list(server: PluginServerInterface):
#     back_up_list = minecraft_rcon.command("!!qb list")
#     server.logger.info(back_up_list)
# shit code
# def rcon_connect(server:PluginServerInterface,mcrcon: RconConnection):
#     global minecraft_rcon
#     minecraft_rcon = mcrcon(main_server_ip,rcon_password,int(rcon_port))
#     minecraft_rcon.connect()
#     server.logger.info("RCON Connected IP:{0} Port:{1}".format(main_server_ip,rcon_port))
# shit code too

def open_json(server: PluginServerInterface):
    global main_server_dir, main_server_ip, mirror_server_dir, world_name
    global rcon_port, rcon_password
    global qb_folder_dir_main,qb_folder_dir_mirror,number_of_qb_slots
    try:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'r') as json_file:
            data = json.load(json_file)
            main_server_dir = data["main_server_dir"]
            mirror_server_dir = data["mirror_server_dir"]
            main_server_ip = data["main_server_ip"]
            world_name = data["world_name"]
            rcon_port = data["rcon_port"]
            rcon_password = data["rcon_password"]
            qb_folder_dir_main = data["qb_folder_dir_main"]
            qb_folder_dir_mirror = data["qb_folder_dir_mirror"]
            number_of_qb_slots = data["number_of_qb_slots"]
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
    "qb_folder_dir_main": "/root/my_mcdr_server/qb_multi",
    "qb_folder_dir_mirror": "/root/my_mcdr_server/qb_multi",
    "number_of_qb_slots": 5
}''')
        open_json(server)


def stop_sync_start(server: PluginServerInterface):
    # TODO stop server, sync the folder, start server and good to go
    server.stop()
    server.logger.info("Wait for complete stop")
    server.wait_for_start()
    sync_world(server)
    server.start()

# How Did You Fix It?
# I commented it :-P

baidu = "ping www.baidu.com"

def ping_test(src: CommandSource,command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print(type(p))
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        src.reply(line)
        lines.append(line)
    # return lines


def sync_world(server:PluginServerInterface):
    command_rsync = "rsync -avPz --progress {0}:{1}/{3} {2}".format(main_server_ip, main_server_dir, mirror_server_dir, world_name)
    cmd_content = subprocess.Popen(command_rsync, shell="True" , stdout=subprocess.PIPE)
    lines = []
    server.logger.info("Start Sync")
    server.logger.info(command_rsync)
    for line in iter(cmd_content.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        server.logger.info(line)
        lines.append(line)
#Why I Wrote This?

#Now I Know


# 显示用法
# !!msync 显示用法
# !!msync peek 查看主服务器qb最新存档信息
# !!msync sync 备份当前镜像服存档，并同步主服务器qb最新存档
# !!msync recover 回档至同步前存档
# !!msync help 显示用法
# 所有操作需要权限等级2
# def show_help(server: PluginServerInterface, src: CommandSource):
#     if src.is_console:
#         server.logger.info(help_message)
#     if src.is_player:
#         server.reply(help_message)
#     # TODO 在src中显示上面的注释信息
#Fxxk shit code again
#Use src.reply() to reply to the player
#do not use this function


# def do_nothing(server: PluginServerInterface):
#     server.load_config_simple()
#Another shit code


#shitcode
#use .requires(lambda src: src.has_permission_higher_than(2)) to check permission
# def show_permission_fail(src: CommandSource):
#     # TODO 在src中显示权限不足信息
#     return None


# # 确认权限等级
# def permission_check(src: CommandSource):
#     return src.has_permission(2)




# 注册指令树
def register_commands(server: PluginServerInterface):
    server.register_command(
        Literal('!!msync').requires(lambda src: src.has_permission_higher_than(2)).runs(lambda src:src.reply(help_message))
            .then(
            Literal({"peek"})
                .requires(lambda src: src.has_permission_higher_than(2))
                .runs(lambda src:qb_make(server,src))
        )
            .then(
            Literal({"sync"})
                .requires(lambda src: src.has_permission_higher_than(2))
                .runs(lambda : stop_sync_start(server))
        )
            .then(
            Literal({"recover"})
                .requires(lambda src: src.has_permission_higher_than(2))
                .runs(lambda src:json_sync(server,src))
        )
            .then(
            Literal({"help"})
                .requires(lambda src: src.has_permission_higher_than(2))
                .runs(lambda src:src.reply(help_message))
        )
    )


def on_load(server: PluginServerInterface, old):
    open_json(server)
    register_commands(server)
