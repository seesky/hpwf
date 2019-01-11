# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/10 15:57'

import json
import urllib.parse

class SearchFilter(object):

    searchField = ''
    searchString = ''
    searchOper = ''

    def TransfromFilterToSql(filter, urlDecode = True):
        """
        转换EasyUi分页时的条件Filters为Sql
        Args:
            filter (string): Filters
            urlDecode (bool):
        Returns:
            returnValue (string): 字段值字符串
        """
        returnSql = ''
        if filter:
            grouptype = ''
            grouptype,list = SearchFilter.GetSearchList(filter)
            if urlDecode:
                urllib.parse.urlencode(SearchFilter.ToSql(list, grouptype))
            else:
                returnSql = SearchFilter.ToSql(list, grouptype)
        return returnSql


    def GetSearchList(jsons):
        """
        将JSON字符串转换为LIST
        Args:
            jsons (string): json 串
        Returns:
            returnValue (string): 字段值字符串
        """
        o = json.loads(jsons)
        torrentsArray = o['rules']
        groupop = str(o['groupOp']).replace("\"", "")
        searchResults = []
        for result in torrentsArray:
            c = SearchFilter()
            c.searchField = result['field']
            c.searchString = result['data']
            c.searchOper = result['op']
            searchResults.append(c)
        return groupop,searchResults


    def ToSql(list, grouptype):
        """
        将查询条件转换成SQL语句
        Args:
            list (List[SearchFilter]):
            grouptype (string):
        Returns:
            returnValue (string): 字段值字符串
        """
        sb = ''
        for result in list:
            sb = sb + " " + grouptype + " "
            if result.searchOper == "eq":
                sb = sb + result.searchField + " = '" + result.searchString + "'"
            elif result.searchOper == "gt":
                sb = sb + result.searchField + " > '" + result.searchString + "'"
            elif result.searchOper == "ge":
                sb = sb + result.searchField + " >= '" + result.searchString + "'"
            elif result.searchOper == "lt":
                sb = sb + result.searchField + " < '" + result.searchString + "'"
            elif result.searchOper == "le":
                sb = sb + result.searchField + " <= '" + result.searchString + "'"
            elif result.searchOper == "ne":
                sb = sb + result.searchField + " <> '" + result.searchString + "'"
            elif result.searchOper == "cn":
                sb = sb + result.searchField + " like '%" + result.searchString + "%'"
            elif result.searchOper == "nu":
                sb = sb + result.searchField + " IS NULL "
            elif result.searchOper == "nn":
                sb = sb + result.searchField + " IS NOT NULL "
            else:
                sb = sb + result.searchField + " = '" + result.searchString + "'"
        sb = sb[4:]
        return sb