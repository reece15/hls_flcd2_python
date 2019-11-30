# coding:utf-8

import serial.tools.list_ports

import time

plist = list(serial.tools.list_ports.comports())

for com in plist:
    print("com name:{name}".format(name=com[0]))


port = serial.Serial(plist[0][0], 230400, timeout=60)
port.write(b'b')
print("开始旋转")
time.sleep(5)
port.write(b'e')

print("停止")
port.close()
