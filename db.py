# -*- coding: utf-8 -*-
from pymongo import MongoClient
from pymongo.message import delete

client = MongoClient('localhost', 27017)
db = client.position
lagou = db.lagou

db_bosszhipin = client.boss
bosszhipin = db.bosszhipin


def all_lagou_positionids():
    return lagou.distinct('_id')


lagou_positionids = []

lagou_positionids = all_lagou_positionids()


def insert_lagou_position(v):
    #  # bson.errors.InvalidDocument: key 'https://b23.tv/bveMkV' must not contain '.'
    # https://stackoverflow.com/questions/28664383/mongodb-not-allowing-using-in-key
    # insert_one 上的 bypass_document_validation=True 无效
    # 使用 insert ,check_keys=False 可以插入，但是insert已经过期
    lagou.insert(v, check_keys=False)


def insert_lagou_positions(v):
    r = []
    for p in v:
        if p['positionId'] in lagou_positionids:
            continue
        r.append(p)
        lagou_positionids.append(p['positionId'])
    lagou.insert_many(r, bypass_document_validation=True)


def insert_bosszhipin_positions(v):
    bosszhipin.insert_many(v, bypass_document_validation=True)


if __name__ == '__main__':
    ids = all_lagou_positionids()
    print(ids)
    print(len(ids))
