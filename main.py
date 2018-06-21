# coding:utf-8

from Laser import Laser

laser = Laser(com="COM3")
laser.start()
laser.main_loop()