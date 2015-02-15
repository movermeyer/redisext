from __future__ import absolute_import

import redisext.serializer
import redisext.utils


class Queue(object):
    __metaclass__ = redisext.utils.KeyHandler
    KEY = None

    @classmethod
    def pop(cls, key):
        item = cls.connect().rpop(key)
        if item and issubclass(cls, redisext.serializer.ISerializer):
            return cls.decode(item)
        else:
            return item

    @classmethod
    def push(cls, key, item):
        if issubclass(cls, redisext.serializer.ISerializer):
            item = cls.encode(item)
        return cls.connect().lpush(key, item)


class PriorityQueue(object):
    __metaclass__ = redisext.utils.KeyHandler
    KEY = None

    @classmethod
    def pop(cls, key):
        redis = cls.connect()
        item = redis.zrangebyscore(key, '-inf', '+inf', num=1)
        item = item[0] if item else None
        redis.zrem(key, item)
        if item and issubclass(cls, redisext.serializer.ISerializer):
            return cls.decode(item)
        else:
            return item

    @classmethod
    def push(cls, key, item, priority):
        if issubclass(cls, redisext.serializer.ISerializer):
            item = cls.encode(item)
        return cls.connect().zadd(key, int(priority), item)
