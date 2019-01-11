# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/12 8:01'

from apps.bizlogic.models import Ciitemdetails
from apps.bizlogic.models import Ciitems
from django.db.models import Q

class ItemDetailsService(object):

    def Add(self, entity, statusMessage):
        pass

    def GetDT(self):
        pass

    def GetEntity(self, id):
        pass

    def Update(self, entity, statusMessage):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetDTByValues(self, names, values):
        pass

    def BatchSave(self, entites):
        pass

    def Delete(self, id):
        pass

    def BatchDelete(self, ids):
        pass

    def SetDeleted(self, ids):
        pass

    def GetDTByCode(self, code):
        """
        绑定下列列表
        Args:
            code (string): Code
        Returns:
            returnValue (Item): 数据表
        """
        returnValue = Ciitemdetails.objects.filter(Q(itemid__in = Ciitems.objects.filter(code=code)) & Q(deletemark=0) & Q(enabled=1)).order_by('sortcode')
        return returnValue