import os
import subprocess
 
 
# 实时输出
def sh(command):
    p = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
    print(type(p))
    lines = []
    for line in iter(p.stdout.readline, b''):
        line = line.strip().decode("GB2312")
        print(line)
        lines.append(line)
    # return lines
 
 
if __name__ == "__main__":
    print("ping www.baidu.com")
    sh("ping www.baidu.com")