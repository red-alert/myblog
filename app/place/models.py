from datetime import datetime

import struct
import time

from flask import flash

from app import place_redis
from app import db

CANVAS_ID = "real_1"
CANVAS_WIDTH = 100
CANVAS_HEIGHT = 100

class RedisCanvas(object):
    @classmethod
    def get_board(cls):
        timestamp = time.time()
        bitmap = place_redis.get(CANVAS_ID) or ''
        return struct.pack('I', int(timestamp)) + bitmap

    @classmethod
    def set_pixel(cls, color, x, y):
        UNIT_SIZE = 'u4'
        offset = y * CANVAS_WIDTH + x
        place_redis.execute_command('bitfield', CANVAS_ID, 'SET', UNIT_SIZE, '#%d' % offset, color)

class Pixel(db.Document):
    color = db.IntField(min_value=0,max_value=15)
    x = db.IntField()
    y = db.IntField()

    def __repr__(self):
        return '<Pixel {x,y:color}>'.format(x=self.x, y=self.y, color=self.color)

    @classmethod
    def create(cls, color, x, y):
        p = cls.objects.get(x=x,y=y) or None
        if p:
            p.color = color
        else:
            pixel = cls(color=color, x=x, y=y)
        pixel.save()

        RedisCanvas.set_pixel(color, x, y)

        print('pixel created!')
        return pixel

    @classmethod
    def get_all(cls):
        try:
            gen = cls.objects
        except:
            return {}
        return {
            (t.x, t.y): t.color for t in gen
        }
