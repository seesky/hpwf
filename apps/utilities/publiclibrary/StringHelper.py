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

