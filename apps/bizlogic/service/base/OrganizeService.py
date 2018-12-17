# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/11 14:25'

from apps.bizlogic.models import Piorganize

from apps.utilities.publiclibrary.DbCommonLibaray import DbCommonLibaray

class OrganizeService(object):
    def Add(self, entity, statusCode, statusMessage):
        pass

    def BatchDelete(self, ids):
        pass

    def BatchMoveTo(self, organizeIds, parentId):
        pass

    def BatchSave(self, dataTable):
        pass

    def Delete(self, id):
        pass

    def GetChildrensById(self, organizeId):
        """
        根据组织机构主键获取其指定分类下的子节点列表
        Args:
            organizeId (string): 组织机构主键
        Returns:
            returnValue (List): 子节点列表
        """
        try:
            returnValue = []
            for piorganize in Piorganize.objects.filter(parentid=organizeId):
                returnValue.append(piorganize.id)
            return returnValue
        except Piorganize.DoesNotExist:
            return returnValue

    def GetDT(self):
        pass

    def GetDTByIds(self, ids):
        pass

    def GetDTByParent(self, parentId):
        pass

    def GetDTByValues(self, names, values):
        pass

    def GetEntity(self, id):
        pass

    def GetList(self):
        pass

    def GetListByParent(self):
        pass

    def MoveTo(self, organizeId, parentId):
        pass

    def SetDeleted(self, ids):
        pass

    def Update(self, entity, statusMessage):
        pass

    def GetChildrensIdByCode(self, code):
        """
        根据编号获取子节点列表
        Args:
            code (string): 编号
        Returns:
            returnValue (List): 子节点列表
        """
        returnValue = []
        sqlQuery = "select id from piorganize where (LEFT(CODE,LENGTH('" + code + "'))='" + code + "')"
        childrens = DbCommonLibaray.executeQuery(self, sqlQuery)
        for c in childrens:
            returnValue.append(c.get('id'))
        return returnValue