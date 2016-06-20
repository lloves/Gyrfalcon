#-*- coding: UTF-8 -*-
__author__ = 'helios'

from Gyrfalcon.Globals import *

class DBSession:

    dbSession = torndb.Connection(dbhost,dbname,dbuser,dbpassword)

    def close(self):
        self.dbSession.close()

    def sqlKeys(self, items):
        sql = ""
        for item in items:
            sql += "{item},".format(item = item)

        if len(items) > 0:
            sql = sql[:-1]

        return sql

    def sqlValues(self, items):
        sql = ""
        for item in items:
            if type(item) == type(1) or type(item) == type(1.00):
                sql += "{item},".format(item = item)
            else:
                sql += '"{item}",'.format(item = str(item))
        if len(items) > 0:
            sql = sql[:-1]

        return sql

    def sqlInsert(self, tableName, dict):
        keys = self.sqlKeys(list(dict.keys()))
        values = self.sqlValues(list(dict.values()))
        sql = ""
        if len(dict) > 0:
            sql = "INSERT INTO {tableName} ({keys}) VALUES({values})".format(tableName=tableName,keys=keys,values=values)
        return sql

    def sqlQuery(self, tableName, items, condition):
        sql = ""
        keys = self.sqlKeys(items)
        if len(items) > 0:
            sql = "SELECT {keys} FROM {tableName} WHERE {condition}".format(keys=keys,tableName=tableName,condition=condition)
        else:
            sql = "SELECT {keys} FROM {tableName}".format(keys=keys,tableName=tableName)

        return sql

    def sqlUpdateItems(self, dict):
        sql = ""
        for key in list(dict.keys()):
            if dict[key] == None:
                continue

            if type(dict[key]) == type(1) or type(dict[key]) == type(1.00):
                sql += "{key}={value}, ".format(key=key, value=dict[key])
            else:
                sql += '{key}="{value}", '.format(key=key, value=dict[key])
        if len(dict) > 0:
            sql = sql[:-2]
        return  sql

    def sqlUpdate(self, tableName, dict):
        updateItems = self.sqlUpdateItems(dict)
        sql = ""
        if len(dict) > 0:
            sql = "UPDATE {tableName} SET {updateItems}".format(tableName=tableName,updateItems=updateItems)

        return sql

    def get(self, tableName, items, condition):
        if len(tableName) == 0 or tableName == None:
            return []
        return self.dbSession.query(self.sqlQuery(tableName, items, condition))

    def insert(self, tableName, params):
        if len(tableName) == 0 or tableName == None:
            return []
        return self.dbSession.insert(self.sqlInsert(tableName, params))

    def update(self, tableName, params, condition):
        if len(tableName) == 0 or tableName == None:
            return []
        sqlUpdate = self.sqlUpdate(tableName, params)
        if condition != None or len(condition) > 0:
            sqlUpdate += " WHERE "+condition
        return self.dbSession.update(self.sqlUpdate(tableName, params))
