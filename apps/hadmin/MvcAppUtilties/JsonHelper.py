# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 10:33'

import json
import datetime

class DateEncoder(json.JSONEncoder):
    def default(self,obj):
        if  isinstance(obj, datetime.datetime):
            returnValue = obj.strftime('%Y-%m-%d %H:%M:%S')
            return returnValue
        elif isinstance(obj, datetime):
            return obj.strftime("%Y-%m-%d")
        else:
            return json.JSONEncoder.default(self, obj)