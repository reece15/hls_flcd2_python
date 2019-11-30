# coding:utf-8

from Laser import Laser
import config

laser = Laser(com=config.PORT)
laser.start()
laser.main_loop()
