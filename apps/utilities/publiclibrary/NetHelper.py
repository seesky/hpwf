# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/4 14:16'

class NetHelper(object):

    def GetIpAddress(request):
        """
        获得当前页面客户端的IP
        Args:
        Returns:
            returnValue (string): IP地址
        """
        # if request.META.has_key('HTTP_X_FORWARDED_FOR'):
        #     returnValue = request.META['HTTP_X_FORWARDED_FOR']
        # else:
        #     returnValue = request.META['REMOTE_ADDR']
        # return returnValue
        if 'HTTP_X_FORWARDED_FOR' in request.META:
            returnValue = request.META['HTTP_X_FORWARDED_FOR']
        else:
            returnValue = request.META['REMOTE_ADDR']
        return returnValue