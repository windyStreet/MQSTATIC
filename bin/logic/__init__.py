#!/usr/bin/env python
# !-*- coding:utf-8 -*-

from bin.until import Mongo

project_ds_info = {}
for ds_info in Mongo.getInstance(table="project_ds").getCollection().find():
    project_ds_info[ds_info["project"]] = ds_info["ds_code"]
