# coding:utf-8
import serial
import time
import atexit
import signal


class Laser(object):

    def __init__(self, com):
        self.rate = 230400
        self.com = com
        self.port = serial.Serial(port=self.com, baudrate=self.rate, timeout=2)
        self.stop_cmd = b'e'
        self.start_cmd = b'b'

        self.range = 42
        self.data_len = 42 * 60
        self.item_len = 6

        self.rpm = 0
        self.avr_rpm = 0

        atexit.register(self.stop)
        signal.signal(signal.SIGINT, lambda x,y: self.stop())
        signal.signal(signal.SIGTERM,  lambda x,y:self.stop())

    def start(self):
        if not self.port.is_open:
            self.port.open()
        self.port.write(self.start_cmd)

    def stop(self):
        if not self.port.is_open:
            self.port.open()
        self.port.write(self.stop_cmd)
        self.port.close()

    def main_loop(self):
        print("Ctrl+c to stop!")
        while self.port.is_open:
            for data in self.read_data():
                print(data)
            time.sleep(0.02)
            print("-"*30)

    def read_data(self):
        fa = [0XFF]
        a0 = [0XFF]


        # 搜索开始数据包  0度 数据包
        while a0[0] != 0xa0:
            fa = a0[::]
            while fa[0] != 0xfa:
                fa = self.port.read(1)
            a0 = self.port.read(1)

        # 读出剩下的数据包
        data = self.port.read(self.data_len - 2)

        data = fa + a0 + data
        rpms = 0


        frame_ok = 0
        for index, split in enumerate(range(0,self.data_len,self.range)):
            seg = data[split:split + self.range]   # 单个42字节的数据包

            check_sum = (0xff - sum(seg[:40])) & 0xff  # 校验数据
            if seg[40] != seg[41] or seg[40] != check_sum or seg[41] != check_sum:
                print("bad frame.checksum:{}, num1:{} num2:{}".format(check_sum, seg[40], seg[41]))
                continue

            if seg[0] == 0xfa and seg[1] == (0xa0 + index):  # seg[0]开始标志 0xfa,    seg[1]角度下标  实际角度 = (seg[1]-0xa0) * 6 + offset
                self.rpm = ((seg[3]<<8) + seg[2])/10.0
                rpms += self.rpm
                frame_ok += 1


                for r_index, deg_split in enumerate(range(4, 40,self.item_len)):
                    deg_data = seg[deg_split: deg_split + self.item_len]  # 单个1度 距离数据包  6个字节
                    intensity = (deg_data[1] << 8) + deg_data[0] # 反射强度
                    length = ((deg_data[3] << 8) + deg_data[2])/1000.0 #  距离 毫米转换为米
                    deg = (seg[1] - 0XA0) * 6 + r_index  # 角度


                    yield deg, length, intensity, self.rpm, rpms


            else:
                print("Data miss!")

        self.avr_rpm = rpms/frame_ok