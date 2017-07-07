#!/usr/bin/env python
# !-*- coding:utf-8 -*-

import pymongo

from bin import init



class Mongo(object):
    def __init__(self, table, db=None, ds=None, ip=None, port=None):
        _db_info = init.CONF_INFO["DB"]
        self.db = None
        self.table = None
        if ds is None:
            ds = "base"
        if ip is None:
            ip = _db_info[ds]["ip"]
        if port is None:
            port = _db_info[ds]["port"]
        if db is None:
            self.db = _db_info[ds]["dbname"]
        else:
            self.db = db
        if table is None:
            self.table = "default"
        else:
            self.table = table
        user = _db_info[ds]["user"]
        password = _db_info[ds]["password"]

        self.client = pymongo.MongoClient(ip, port)
        self.collection = None
        pass

    def getCollection(self):
        if self.db is None or self.table is None:
            return None
        return self.client[self.db][self.table]

    def getClient(self):
        return self.client

    def close(self):
        return self.client.close()


def getInstance(table, db=None, ip=None, ds=None, port=None):
    return Mongo(table, db, ds, ip, port)


if __name__ == "__main__":
    print(pymongo.get_version_string())
    client = pymongo.MongoClient("192.168.7.216", 27017)
    db = client["echartdb"]
    collection = db["echart_collection"]
    print(collection.find().count())
    # collection.insert({"A":"aa","B":"bb"})
    # collection.insert({"A":"aa"})
    # collection.insert({"A1":"aa1","B1":"bb1"})
    # collection.insert({"C1":"cc1","B1":"bb1"})
    # collection.insert({"C1":"cc1","A1":"aa1"})
    # collection.insert({"C1":"cc1","A1":"aa"})
    # collection.insert({"C1":"cc1","A":"aa"})
    print(db.collection_names())
    print(str(collection.find()))
    print(str(collection.find().count()))
    print(str(collection.find({"A": "aa"})))
    print(collection.find_one())
    print("||||||||||||||||||||||")
    print(collection.find_one({"A": "aa"}))
    print("----------------------")
    print(collection.find({"A": "aa"}).count())
    for it in collection.find({"A": "aa"}):
        print(it)
    print("||||||||||||||||||||||")
    for item in collection.find():
        print(item)
    print("+++++++++++++++++++++++")
    for itts in collection.find().limit(5):
        print(itts)
    print("##################################")
    for itta in collection.find().sort("A", -1).limit(13):
        print(itta)
    print("**********************************")
    for ittb in collection.find().sort("B", -1).limit(10):
        print(ittb)
    print("&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&")
    for ittc in collection.find().skip(3).sort("B", -1).limit(10):
        print(ittc)
    print("((((((((((((((((((((((((((((((((((((")
    for ittd in collection.find().sort("A", -1).sort("B", -1).limit(13):
        print(ittd)
    print("))))))))))))))))))))))))))))))")
    for itte in collection.find().sort("A", -1).limit(13):
        print(itte)
    print("@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@@")
    for ittf in collection.find({"A1": {"$regex": "1"}}):
        print(ittf)
    print("!!!!!!!!!!!!!!!!!!!!!!!!!!!!")
    for ittg in collection.find({"A1": "/?1?/"}):
        print(ittg)
