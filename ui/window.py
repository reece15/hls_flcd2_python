# coding:utf-8

import pygame,sys
import Laser
import math


laser = Laser.Laser(com="COM3")

pygame.init()
screen=pygame.display.set_caption('laser data view')
screen=pygame.display.set_mode([800,800])
screen.fill([0,0,0])

x1 = y1=400

pygame.draw.circle(screen,[255, 0, 0],[x1,y1],2,0)
pygame.display.flip()

laser.start()
while True:
    screen.fill([0, 0, 0])
    for event in pygame.event.get():
        if event.type==pygame.QUIT:
            sys.exit()

    for deg, length, intensity, rpm, rpms in laser.read_data():
        if length < 0.000001 and intensity < 0.00000001:
            continue
        d = (360 - deg) * math.pi / 180.0
        x2 = x1 + length * 100 * math.cos(d)
        y2 = y1 + length * 100 * math.sin(d)
        i = intensity/1000
        if i > 1:
            i = 1
        pygame.draw.circle(screen, [int(255 * i), 0, 0], [int(x2), int(y2)], 2, 0)
        pygame.display.set_caption(u'laser data view 转速: {:.2f}r/min  平均转速:{:.2f}r/min'.format(rpm, laser.avr_rpm))

    pygame.display.flip()