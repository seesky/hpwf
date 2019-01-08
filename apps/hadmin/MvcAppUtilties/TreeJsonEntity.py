# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/8 10:08'\

class TreeJsonEntity(object):
    parentId = ''
    id = ''
    text = ''
    value = ''
    url = ''
    checkState = ''
    #是否展开
    isExpand = ''
    #是否有子节点
    hasChildren = ''
    iconCls = ''
    title = ''
    #自定义属性
    Attribute = ''
    #自定义属性值
    AttributeValue = ''
    #自定义属性A
    AttributeA = ''
    #自定义属性值A
    AttributeValueA = ''

    def obj_2_json(obj):
        return {
            'parentId' : obj.parentId,
            'id' : obj.id,
            'text' : obj.text,
            'value' : obj.value,
            'url' : obj.url,
            'checkState' : obj.checkState,
            #是否展开
            'isExpand' : obj.isExpand,
            #是否有子节点
            'hasChildren' : obj.hasChildren,
            'iconCls' : obj.iconCls,
            'title' : obj.title,
            #自定义属性
            'Attribute' : obj.Attribute,
            #自定义属性值
            'AttributeValue' : obj.AttributeValue,
            #自定义属性A
            'AttributeA' : obj.AttributeA,
            #自定义属性值A
            'AttributeValueA' : obj.AttributeValueA
        }

    def TreeToJson(list, ParentId = '0'):
        strJson = ''
        item = []
        for i in list:
            if i.parentId == ParentId:
                item.append(i)

        strJson = strJson + '['

        if len(item) > 0:
            for entity in item:
                strJson = strJson + '{'
                strJson = strJson + "\"id\":\"" + entity.id + "\","
                strJson = strJson + "\"text\":\"" + entity.text.replace("&nbsp;", "") + "\","
                strJson = strJson + "\"value\":\"" + entity.value + "\","
                if entity.iconCls and entity.iconCls.replace("&nbsp;", ""):
                    strJson = strJson + "\"iconCls\":\"" + entity.iconCls.replace("&nbsp;", "") + "\","
                if entity.Attribute or entity.AttributeA or entity.title or entity.url:
                    strJson = strJson + "\"attributes\":{"
                    strJson = strJson + "\"url\":\"" + entity.url
                    strJson = strJson + "\",\"title\":\"" + entity.title + "\","
                    if entity.Attribute:
                        strJson = strJson + "\"" + entity.Attribute + "\":\"" + entity.AttributeValue + "\","
                    if entity.AttributeA:
                        strJson = strJson + "\"" + entity.AttributeA + "\":\"" + entity.AttributeValueA + "\","
                    if entity.checkState:
                        strJson = strJson + "\"checkState\":" + entity.checkState + ","
                    if entity.parentId:
                        strJson = strJson + "\"parentNodes\":\"" + entity.parentId + "\"}"

                if entity.hasChildren:
                    if entity.isExpand:
                        strJson = strJson + ",\"state\":\"open\","
                    else:
                        strJson = strJson + ",\"state\":\"closed\","
                    strJson = strJson + "\"children\":" + TreeJsonEntity.TreeToJson(list, entity.id) + ""
                strJson = strJson + "},"
            strJson = strJson[:-1]
        strJson = strJson + "]"
        return strJson