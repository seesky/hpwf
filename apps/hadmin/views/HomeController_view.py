# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2019/1/7 10:55'

from django.shortcuts import render,render_to_response
from django.http.response import HttpResponse
from apps.hadmin.MvcAppUtilties.LoginAuthorize import LoginAuthorize
from apps.hadmin.MvcAppUtilties.CommonUtils import CommonUtils
from django.template import loader ,Context
import django.template
from apps.bizlogic.service.base.ModuleService import ModuleService
from apps.bizlogic.service.permission.UserPermission import UserPermission
from django.db.models import Q
from apps.hadmin.MvcAppUtilties.TreeJsonEntity import TreeJsonEntity

def index(request):
    """
    初始化页面
    Args:
    Returns:
    """
    return render(request, 'Login/Index.html')

@LoginAuthorize
def AccordiontreeIndex(request):
    """
    手风琴+树形目录(2级+)
    Args:
    Returns:
    """
    response = HttpResponse()
    tmp = loader.get_template('Home/AccordionTreeIndex.html')   #加载模板
    render_content = {'Skin':CommonUtils.Theme(response, request), 'Account':CommonUtils.Current(response, request).RealName}   #将要渲染到模板的数据
    new_body = tmp.render(render_content)   #渲染模板
    response.content = new_body #设置返回内容
    return response

@LoginAuthorize
def LoadTreeMenu(request):
    """
    加载无限树菜单
    Args:
    Returns:
    """
    try:
        moduleId = request.POST['moduleId']
    except:
        moduleId = '84CA44CB-8A0F-43A1-BD86-1ED764216C59'

    response = HttpResponse()
    list = None
    if CommonUtils.Current(response, request).IsAdministrator:
        list = ModuleService.GetList(ModuleService)
    else:
        list = UserPermission.GetModuleDTByUserId(None, CommonUtils.Current(response, request) , CommonUtils.Current(response, request).Id)

    listWhere = list.filter(Q(moduletype = None) | Q(moduletype = 2) | Q(moduletype = 3) | Q(ispublic = 1))

    treeList = []

    for item in listWhere:
        tree = TreeJsonEntity()
        hasChildren = False
        for i in list:
            if i.parentid == item.id:
                hasChildren = True
                break
        tree.id = item.id
        tree.text = item.fullname
        tree.value = item.id
        tree.url = item.mvcnavigateurl
        tree.title = item.fullname
        tree.isExpand = item.expand
        tree.hasChildren = hasChildren
        tree.parentId = item.parentid
        if item.iconcss:
            tree.iconCls = item.iconcss.replace('icon ', '')
        else:
            tree.iconCls = ''
        treeList.append(tree)
    response.content = TreeJsonEntity.TreeToJson(treeList, moduleId)
    return response

@LoginAuthorize
def StartPage(request):
    """
    起始页
    Args:
    Returns:
    """
    return render(request, 'Home/StartPage.html')


