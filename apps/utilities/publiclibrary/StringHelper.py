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


