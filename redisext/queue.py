from __future__ import absolute_import

import redisext.utils


class Queue(object):
    __metaclass__ = redisext.utils.KeyHandler
    KEY = None

    @classmethod
    def pop(cls, key):
        item = cls.connect().rpop(key)
        return redisext.utils.decode(cls, item)

    @classmethod
    def push(cls, key, item):
        item = redisext.utils.encode(cls, item)
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
        return redisext.utils.decode(cls, item)

    @classmethod
    def push(cls, key, item, priority):
        item = redisext.utils.encode(cls, item)
        return cls.connect().zadd(key, int(priority), item)
