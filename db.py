# -*- coding: utf-8 -*-
from pymongo import MongoClient

client = MongoClient('localhost',27017)
db = client.lagou
position = db.position

db_bosszhipin = client.boss
bosszhipin = db.bosszhipin

def insert_position(v):
    #  # bson.errors.InvalidDocument: key 'https://b23.tv/bveMkV' must not contain '.'
    # https://stackoverflow.com/questions/28664383/mongodb-not-allowing-using-in-key
    # insert_one 上的 bypass_document_validation=True 无效
    # 使用 insert ,check_keys=False 可以插入，但是insert已经过期
    position.insert(v,check_keys=False)

def insert_positions(v):
    position.insert_many(v,bypass_document_validation=True)

def insert_bosszhipin_positions(v):
    bosszhipin.insert_many(v,bypass_document_validation=True)