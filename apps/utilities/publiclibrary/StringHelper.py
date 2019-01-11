# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/13 13:46'



class StringHelper(object):

    def ArrayToList(self, ids, separativeSign):
        rowCount = 0
        returnValue = ''
        for id in  ids:
            rowCount = rowCount + 1
            returnValue = returnValue + separativeSign + id + separativeSign + ','
        if rowCount == 0:
            returnValue = ''
            return returnValue
        else:
            returnValue = returnValue.strip("\,")
            return  returnValue


    def RepeatString(self, targetString, repeatCount):
        """
        重复字符串
        Args:
            targetString (string): 目标字符串
            repeatCount (int): 重复次数
        Returns:
            returnValue (string): 结果字符串
        """
        returnValue = ''
        for i in range(repeatCount):
            returnValue = returnValue + targetString
        return returnValue

    def GetSearchString(self, searchValue, allLike = False):
        """
        获取查询字符串
        Args:
            searchValue (string): 查询字符
            allLike (bool): 是否所有的匹配都查询，建议传递"%"字符
        Returns:
            returnValue (string): 结果字符串
        """
        searchValue = searchValue.strip()
        if len(searchValue) > 0:
            searchValue = searchValue.replace('[', '_')
            searchValue = searchValue.replace(']', '_')

        if searchValue == '%':
            searchValue = '[%]'

        if len(searchValue) > 0 and ('%' not in searchValue) and ('_' not in searchValue):
            if allLike:
                tmpStr = ''
                for s in searchValue:
                    tmpStr = '%' + s
                searchValue = tmpStr + '%'
            else:
                searchValue = '%' + searchValue + '%'
        return searchValue

    def ObjectsToList(ids):
        """
        字段值数组转换为字符串列表
        Args:
            ids (string): 字段值
        Returns:
            returnValue (string): 字段值字符串
        """
        returnValue = ''
        baseStr = "'"
        for id in ids:
            baseStr = baseStr + id + "', '"
        if len(ids) == 0:
            returnValue = " NULL "
        else:
            returnValue = returnValue[0, len(returnValue) - 3]
        return returnValue

