<!--
 * @Author: 张深态 78351684+MRNOBODY-ZST@users.noreply.github.com
 * @Date: 2022-05-05 10:12:06
 * @LastEditors: 张深态 78351684+MRNOBODY-ZST@users.noreply.github.com
 * @LastEditTime: 2022-05-05 10:34:15
 * @FilePath: \MirrorServerSync\README.md
 * @Description: 这是默认设置,请设置`customMade`, 打开koroFileHeader查看配置 进行设置: https://github.com/OBKoro1/koro1FileHeader/wiki/%E9%85%8D%E7%BD%AE
-->
# Mirror Server Sync

A Simple MCDR Plugin To Sync Map Files Of Minecraft On Different Servers

## 一、使用前配置

本插件适用于Windows系统与Linux系统

​在使用本插件前，你需要在你的服务器上安装Rsync

​Linux安装方法：`yum -y install rsync`

​Windows安装方法：[cwRsync - Rsync for Windows | itefix.net](https://www.itefix.net/cwrsync)下载文件后安装Exe文件

一般服务器上默认会安装Rsync，为了保险，手动安装一遍。

请确保您的服务器放行了所有端口以确保Rsync能正常工作

打开终端，执行`ssh-keygen`。无需输入密码，无脑确认即可。再执行`ssh-copy-id {Main Server IP/Mirror Server IP}`（IP地址取决于你是在Main Server还是再Mirror Server，Main就写Mirror，Mirror写Main）之后确认Fingerprint，输入yes后输入对方服务器的密码，Enter。

第一次启动时会自动创建mirror_server_sync.json，内容如下

```json
{
    "main_server_ip": "", //这里修改为主服务器IP
    "world_name": "", //这里修改为主服务器世界名称
    "main_server_dir": "/root/my_mcdr_server/server", //这里修改为主服务器server目录
    "mirror_server_dir": "/root/my_mcdr_server/server", //这里修改为镜像服务器server目录
}
```

修改完后就可以启动MCDR

## 二、指令说明
