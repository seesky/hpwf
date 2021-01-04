# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/13 14:55'

from django.db import connection, transaction

class DbCommonLibaray(object):

    def executeQuery(self, sql):
        cursor = connection.cursor()  # 获得一个游标(cursor)对象
        cursor.execute(sql)
        rawData = cursor.fetchall()
        col_names = [desc[0] for desc in cursor.description]
        result = []
        for row in rawData:
            objDict = {}
            # 把每一行的数据遍历出来放到Dict中
            for index, value in enumerate(row):

                objDict[col_names[index]] = value
            result.append(objDict)
        return result

    def GetDTByPage(tableName, conditions, orderby, selectField = "*", pageIndex = 1, pageSize = 20):
        if not selectField:
            selectField = "*"
        if conditions:
            conditions = "WHERE " + conditions
        sqlStart = str((pageIndex - 1) * pageSize)
        sqlEnd = str(pageIndex * pageSize)
        sqlQuery = "SELECT " + str(selectField) + " FROM " + tableName + " " + str(conditions) + " ORDER BY " + str(orderby) + " LIMIT " + str(sqlStart) + ", " + str(sqlEnd)
        returnValue = DbCommonLibaray.executeQuery(None, sqlQuery)
        return returnValue