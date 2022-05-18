# At least it works
import random,os,subprocess,json
from mcdreforged.api.types import PluginServerInterface, CommandSource, Info
from mcdreforged.api.command import Literal
from mcdreforged.api.rcon import RconConnection
from mcdreforged.api.rtext import *
from mcdreforged.api.decorator import *


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

def qb_back(server: PluginServerInterface,src: CommandSource):
    server.execute_command("!!qb back 1")
    if qb_auto_back == "True":
        server.execute_command("!!qb confirm")
    if qb_auto_back == "False":
        src.reply("已经回档，请手动确认")
        

def qb_make(server: PluginServerInterface):
    server.execute_command("!!qb make BeforeSyncBackup")


@new_thread("json_sync")
def sync_json(server:PluginServerInterface,src: CommandSource):
    src.reply("Start Sync Json")
    for i in range(1, number_of_qb_slots + 1):
        json_sync_command = "rsync -avPz --progress {0}:{1}/slot{3}/*.json {2}/slot{3}".format(main_server_ip, qb_folder_dir_main, qb_folder_dir_mirror,i)
        src.reply(json_sync_command)
        cmd_content = subprocess.Popen(json_sync_command, shell="True" , stdout=subprocess.PIPE)
        lines = []
        for line in iter(cmd_content.stdout.readline, b''):
            line = line.strip().decode("GB2312")
            server.logger.info(line)
            lines.append(line)



def open_json(server: PluginServerInterface):
    global main_server_dir, main_server_ip, mirror_server_dir, world_name
    global qb_folder_dir_main,qb_folder_dir_mirror,number_of_qb_slots
    global qb_auto_back
    try:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'r') as json_file:
            data = json.load(json_file)
            main_server_dir = data["main_server_dir"]
            mirror_server_dir = data["mirror_server_dir"]
            main_server_ip = data["main_server_ip"]
            world_name = data["world_name"]
            qb_folder_dir_main = data["qb_folder_dir_main"]
            qb_folder_dir_mirror = data["qb_folder_dir_mirror"]
            number_of_qb_slots = data["number_of_qb_slots"]
            qb_auto_back = data["qb_auto_make"]
    except:
        with open(os.path.join(server.get_data_folder(), 'mirror_server_sync.json'), 'w') as json_file:
            json_file.write('''
{
    "main_server_ip": "127.0.0.1",
    "world_name": "world",
    "main_server_dir": "/root/my_mcdr_server/server",
    "mirror_server_dir": "/root/my_mcdr_server/server",
    "qb_folder_dir_main": "/root/my_mcdr_server/qb_multi",
    "qb_folder_dir_mirror": "/root/my_mcdr_server/qb_multi",
    "number_of_qb_slots": 5,
    "qb_auto_make" : "True"
}''')
        open_json(server)

@new_thread("stop_sync_start")
def stop_sync_start(server: PluginServerInterface):
    # TODO stop server, sync the folder, start server and good to go
    server.stop()
    server.logger.info("Wait for the server to shut down completely")
    server.wait_for_start()
    sync_world(server)
    server.start()

# How Did You Fix It?
# I commented it :-P

@new_thread("world_sync")
def sync_world(server:PluginServerInterface):
    server.execute_command("!!qb make BeforeSyncBackup")
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


#Another shit code


#shitcode
#use .requires(lambda src: src.has_permission_higher_than(2)) to check permission
@new_thread("no_permission_msg")
def no_permission_msg(src: CommandSource):
    random_number = random.randint(0,2)
    if random_number == 0:
        src.reply(nizaiganshenme)
    if random_number == 1:
        src.reply(obfuscated_text)
    if random_number == 2:
        src.reply(bruh_img)


# 注册指令树
def register_commands(server: PluginServerInterface):
    server.register_command(
        Literal('!!msync').requires(lambda src: src.has_permission_higher_than(2),lambda src:no_permission_msg(src)).runs(lambda src:src.reply(help_message))
            .then(
            Literal({"peek"})
                .requires(lambda src: src.has_permission_higher_than(2),lambda src:no_permission_msg(src))
                .runs(lambda src:qb_make(server))
        )
            .then(
            Literal({"sync"})
                .requires(lambda src: src.has_permission_higher_than(2),lambda src:no_permission_msg(src))
                .runs(lambda : stop_sync_start(server))
        )
            .then(
            Literal({"recover"})
                .requires(lambda src: src.has_permission_higher_than(2),lambda src:no_permission_msg(src))
                .runs(lambda src:sync_json(server,src))
        )
            .then(
            Literal({"help"})
                .requires(lambda src: src.has_permission(2),lambda src:no_permission_msg(src))
                .runs(lambda src:src.reply(help_message))
        )
    )


def on_load(server: PluginServerInterface, old):
    open_json(server)
    register_commands(server)

# def on_unload(server: PluginServerInterface):