import datetime
from django.test import TestCase
from django.db.models import Q
from apps.bizlogic.service.base import ExceptionService
from apps.bizlogic.models import Ciexception
import uuid

from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.OrganizeService import OrganizeService
from apps.bizlogic.service.base.StaffService import StaffService
from apps.bizlogic.service.base.PermissionItemService import PermissionItemService

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Piuserrole
from apps.bizlogic.models import Pipermission
from apps.bizlogic.models import Pipermissionscope
from apps.bizlogic.models import Piuserorganize
from apps.bizlogic.models import Pistaff
from apps.bizlogic.models import Pistafforganize
from apps.bizlogic.models import Pipermissionitem

# Create your tests here.
class ExceptionServiceTest(TestCase):

    def test_Add(self):
        pass

class UserServiceTest(TestCase):

    # 新增用户
    def test_AddUser(self):
        print('新增用户测试...  ' + str(datetime.datetime.now()))
        #添加失败
        # user = Piuser()
        # returnCode, returnMessage, returnValue = UserSerivce.AddUser(self, user)
        # self.assertEqual(returnCode, 0)
        # self.assertEqual(returnMessage, '发生未知错误。')
        # self.assertEqual(returnValue, None)
        #添加成功
        user = Piuser()
        user.id = uuid.uuid1()
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode,returnMessage,returnValue = UserSerivce.AddUser(self, user)
        self.assertEqual(Piuser.objects.get(username='wuyujia').realname, '邬育佳')
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')

        user1 = Piuser()
        user1.id = uuid.uuid1()
        user1.username = 'wuyujia1'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = UserSerivce.AddUser(self, user1)
        self.assertEqual(Piuser.objects.get(username='wuyujia1').realname, '邬育佳1')
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')


    # 根据用户id获取用户实体
    def test_GetEntity(self):
        print('根据用户id获取用户实体测试...  ' + str(datetime.datetime.now()))
        #不存在
        user = UserSerivce.GetEntity('0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(user, None)
        #存在
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        user = UserSerivce.GetEntity('0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(user.realname, '邬育佳')


    #用户名是否重复
    def test_Exists(self):
        print('用户名是否重复测试...  ' + str(datetime.datetime.now()))
        # 不存在重复
        exists = UserSerivce.Exists(self, 'id', '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(exists, False)
        # 存在重复
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        exists = UserSerivce.Exists(self, 'id', '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(exists, True)


    #根据用户名获取用户实体
    def test_GetEntityByUserName(self):
        print('根据用户名获取用户实体测试...  ' + str(datetime.datetime.now()))
        # 不存在
        user = UserSerivce.GetEntityByUserName(self, 'wuyujia')
        self.assertEqual(user, None)
        # 存在
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        user = UserSerivce.GetEntityByUserName(self, 'wuyujia')
        self.assertNotEqual(user, None)


    #获取用户列表
    def test_GetDT(self):
        print('获取用户列表测试...  ' + str(datetime.datetime.now()))
        #没有用户
        returnValue = UserSerivce.GetDT(self)
        self.assertEqual(len(returnValue), 0)
        #有用户
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        returnValue = UserSerivce.GetDT(self)
        self.assertEqual(len(returnValue), 1)


    #分页查询
    def test_GetDTByPage(self):
        print('用户分页查询测试...  ' + str(datetime.datetime.now()))
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.companyid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.save()

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie1.fullname = 'o2'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.save()

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()
        returnValue = UserSerivce.GetDTByPage(self, '', '07DF66FA-644E-4B1F-9994-AE7332796058', '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81', 1, None)

    #获取用户列表
    def test_GetList(self):
        print('获取用户列表测试...  ' + str(datetime.datetime.now()))
        # 没有用户
        returnValue = UserSerivce.GetDT(self)
        self.assertEqual(len(returnValue), 0)
        # 有用户
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        returnValue = UserSerivce.GetDT(self)
        self.assertEqual(len(returnValue), 1)


    #按主键获取用户列表
    def test_GetDTByIds(self):
        print('按主键获取用户列表测试...  ' + str(datetime.datetime.now()))
        # 没有用户
        ids = ['0003d3f5-6aa1-4475-adf6-50961c8bd739','0003d3f5-6aa1-4475-adf6-50961c8bd738']
        returnValue = UserSerivce.GetDTByIds(self, ids)
        self.assertEqual(len(returnValue), 0)
        # 有用户
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        returnValue = UserSerivce.GetDTByIds(self, ids)
        self.assertEqual(len(returnValue), 1)

        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd738'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)
        returnValue = UserSerivce.GetDTByIds(self, ids)
        self.assertEqual(len(returnValue), 2)


    #更新用户
    def test_UpdateUser(self):
        print('更新用户测试...  ' + str(datetime.datetime.now()))
        #更新失败
        user = Piuser()
        returnCode,returnMessage = UserSerivce.UpdateUser(self, user)
        self.assertEqual(returnCode, 9)
        self.assertEqual(returnMessage, '发生未知错误。')


    #查询用户
    def test_Search(self):
        print('查询用户测试...  ' + str(datetime.datetime.now()))
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        roleIds = ['27A40BF7-D68C-4BF5-9B40-056A8D3E9A81']
        returnValue = UserSerivce.Search(self, '', '', roleIds)
        self.assertEqual(len(returnValue), 1)


    #单个删除用户
    def test_Delete(self):
        print('单个删除用户测试...  ' + str(datetime.datetime.now()))
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid, '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid, '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(UserSerivce.Delete(self, '0003d3f5-6aa1-4475-adf6-50961c8bd730'), False)
        self.assertEqual(UserSerivce.Delete(self, '0003d3f5-6aa1-4475-adf6-50961c8bd739'), True)


    #批量删除用户
    def test_BatchDelete(self):
        print('批量删除用户测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()
        ##########################################################################################
        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)

        piuserrole1 = Piuserrole()
        piuserrole1.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A83'
        piuserrole1.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85'
        piuserrole1.enabled = 1
        piuserrole1.deletemark = 0
        piuserrole1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        piuserrole1.save()

        pipermission1 = Pipermission()
        pipermission1.id = '0058389d-cdba-47ca-8785-06f5c9a92f01'
        pipermission1.resourcecategory = 'PIUSER'
        pipermission1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermission1.enabled = 1
        pipermission1.deletemark = 0
        pipermission1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.save()

        pipermissionscope1 = Pipermissionscope()
        pipermissionscope1.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd70'
        pipermissionscope1.resourcecategory = 'PIUSER'
        pipermissionscope1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermissionscope1.enabled = 1
        pipermissionscope1.deletemark = 0
        pipermissionscope1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.save()
        ##############################################################################################
        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid, '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid, '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd731').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A83').roleid, '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f01').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd70').resourceid, '0003d3f5-6aa1-4475-adf6-50961c8bd731')

        idsTrue = ['0003d3f5-6aa1-4475-adf6-50961c8bd739', '0003d3f5-6aa1-4475-adf6-50961c8bd731']
        idsFalse = ['0003d3f5-6aa1-4475-adf6-50961c8bd733']
        self.assertEqual(UserSerivce.BatchDelete(self, idsTrue), True)
        self.assertEqual(UserSerivce.BatchDelete(self, idsFalse), False)


    #批量打删除标志
    def test_SetDeleted(self):
        print('批量打删除标志测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()
        ##########################################################################################
        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)

        piuserrole1 = Piuserrole()
        piuserrole1.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A83'
        piuserrole1.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85'
        piuserrole1.enabled = 1
        piuserrole1.deletemark = 0
        piuserrole1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        piuserrole1.save()

        pipermission1 = Pipermission()
        pipermission1.id = '0058389d-cdba-47ca-8785-06f5c9a92f01'
        pipermission1.resourcecategory = 'PIUSER'
        pipermission1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermission1.enabled = 1
        pipermission1.deletemark = 0
        pipermission1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.save()

        pipermissionscope1 = Pipermissionscope()
        pipermissionscope1.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd70'
        pipermissionscope1.resourcecategory = 'PIUSER'
        pipermissionscope1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermissionscope1.enabled = 1
        pipermissionscope1.deletemark = 0
        pipermissionscope1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.save()
        ##############################################################################################
        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd731').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A83').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f01').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd70').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd731')

        idsTrue = ['0003d3f5-6aa1-4475-adf6-50961c8bd739', '0003d3f5-6aa1-4475-adf6-50961c8bd731']
        idsFalse = ['0003d3f5-6aa1-4475-adf6-50961c8bd733']
        self.assertEqual(UserSerivce.SetDeleted(self, idsTrue), True)
        self.assertEqual(UserSerivce.SetDeleted(self, idsFalse), False)


    #批量保存
    def test_BatchSave(self):
        print('批量保存测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()
        ##########################################################################################
        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)

        piuserrole1 = Piuserrole()
        piuserrole1.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A83'
        piuserrole1.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85'
        piuserrole1.enabled = 1
        piuserrole1.deletemark = 0
        piuserrole1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        piuserrole1.save()

        pipermission1 = Pipermission()
        pipermission1.id = '0058389d-cdba-47ca-8785-06f5c9a92f01'
        pipermission1.resourcecategory = 'PIUSER'
        pipermission1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermission1.enabled = 1
        pipermission1.deletemark = 0
        pipermission1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.save()

        pipermissionscope1 = Pipermissionscope()
        pipermissionscope1.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd70'
        pipermissionscope1.resourcecategory = 'PIUSER'
        pipermissionscope1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermissionscope1.enabled = 1
        pipermissionscope1.deletemark = 0
        pipermissionscope1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.save()
        ##############################################################################################
        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd731').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A83').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f01').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd70').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd731')

        dataTable = [user, user1]
        self.assertEqual(UserSerivce.BatchSave(self, dataTable), True)


    #得到当前用户所在公司的用户列表
    def test_GetCompanyUser(self):
        print('得到当前用户所在公司的用户列表测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.companyname = 'hstecs.com'
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()
        ##########################################################################################
        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.companyname = 'hstecs.com'
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)

        piuserrole1 = Piuserrole()
        piuserrole1.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A83'
        piuserrole1.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85'
        piuserrole1.enabled = 1
        piuserrole1.deletemark = 0
        piuserrole1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        piuserrole1.save()

        pipermission1 = Pipermission()
        pipermission1.id = '0058389d-cdba-47ca-8785-06f5c9a92f01'
        pipermission1.resourcecategory = 'PIUSER'
        pipermission1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermission1.enabled = 1
        pipermission1.deletemark = 0
        pipermission1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.save()

        pipermissionscope1 = Pipermissionscope()
        pipermissionscope1.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd70'
        pipermissionscope1.resourcecategory = 'PIUSER'
        pipermissionscope1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermissionscope1.enabled = 1
        pipermissionscope1.deletemark = 0
        pipermissionscope1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.save()
        ##############################################################################################
        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd731').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A83').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f01').resourcecategory, 'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd70').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd731')

        returnValue = UserSerivce.GetCompanyUser(self, user)
        self.assertEqual(returnValue[0].realname, '邬育佳')
        self.assertEqual(returnValue[1].realname, '邬育佳1')


    # 得到当前用户所在部门的用户列表
    def test_GetDepartmentUser(self):
        print('得到当前用户所在部门的用户列表测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.companyname = 'hstecs.com'
        user.departmentname = '研发部'
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        piuserrole = Piuserrole()
        piuserrole.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A82'
        piuserrole.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81'
        piuserrole.enabled = 1
        piuserrole.deletemark = 0
        piuserrole.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        piuserrole.save()

        pipermission = Pipermission()
        pipermission.id = '0058389d-cdba-47ca-8785-06f5c9a92f09'
        pipermission.resourcecategory = 'PIUSER'
        pipermission.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermission.enabled = 1
        pipermission.deletemark = 0
        pipermission.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission.save()

        pipermissionscope = Pipermissionscope()
        pipermissionscope.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd78'
        pipermissionscope.resourcecategory = 'PIUSER'
        pipermissionscope.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        pipermissionscope.enabled = 1
        pipermissionscope.deletemark = 0
        pipermissionscope.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope.save()
        ##########################################################################################
        user1 = Piuser()
        user1.id = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        user1.username = 'wuyujia'
        user1.realname = '邬育佳1'
        user1.isstaff = 1
        user1.isvisible = 1
        user1.isdimission = 1
        user1.deletemark = 0
        user1.enabled = 1
        user1.companyname = 'hstecs.com'
        user1.departmentname = '研发部'
        user1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user1)

        piuserrole1 = Piuserrole()
        piuserrole1.id = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A83'
        piuserrole1.roleid = '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85'
        piuserrole1.enabled = 1
        piuserrole1.deletemark = 0
        piuserrole1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        piuserrole1.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        piuserrole1.save()

        pipermission1 = Pipermission()
        pipermission1.id = '0058389d-cdba-47ca-8785-06f5c9a92f01'
        pipermission1.resourcecategory = 'PIUSER'
        pipermission1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermission1.enabled = 1
        pipermission1.deletemark = 0
        pipermission1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermission1.save()

        pipermissionscope1 = Pipermissionscope()
        pipermissionscope1.id = '021578bc-a8c7-4c35-9e2b-2c11c970dd70'
        pipermissionscope1.resourcecategory = 'PIUSER'
        pipermissionscope1.resourceid = '0003d3f5-6aa1-4475-adf6-50961c8bd731'
        pipermissionscope1.enabled = 1
        pipermissionscope1.deletemark = 0
        pipermissionscope1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        pipermissionscope1.save()
        ##############################################################################################
        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A82').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A81')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f09').resourcecategory,
                         'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd78').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd739')

        self.assertEqual(Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd731').username, 'wuyujia')
        self.assertEqual(Piuserrole.objects.get(id='27A40BF7-D68C-4BF5-9B40-056A8D3E9A83').roleid,
                         '27A40BF7-D68C-4BF5-9B40-056A8D3E9A85')
        self.assertEqual(Pipermission.objects.get(id='0058389d-cdba-47ca-8785-06f5c9a92f01').resourcecategory,
                         'PIUSER')
        self.assertEqual(Pipermissionscope.objects.get(id='021578bc-a8c7-4c35-9e2b-2c11c970dd70').resourceid,
                         '0003d3f5-6aa1-4475-adf6-50961c8bd731')

        returnValue = UserSerivce.GetCompanyUser(self, user)
        self.assertEqual(returnValue[0].realname, '邬育佳')
        self.assertEqual(returnValue[1].realname, '邬育佳1')
        self.assertEqual(returnValue[0].companyname, returnValue[1].companyname)
        self.assertEqual(returnValue[0].departmentname, returnValue[1].departmentname)


    #得到指定部门包含的用户列表
    def test_GetDepartmentUsers(self):
        print('得到指定部门包含的用户列表测试...  ' + str(datetime.datetime.now()))
        #####################################################
        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.companyname = 'hstecs.com'
        user.departmentname = '研发部'
        user.departmentid = '9007C958-4C6A-432E-BD06-E50F8A2F110A'
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)
        ##############################################################################################
        organzie = Piuserorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.userid = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        organzie.departmentid = '9007C958-4C6A-432E-BD06-E50F8A2F110A'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.save()
        returnValue = UserSerivce.GetDepartmentUsers(self, '9007C958-4C6A-432E-BD06-E50F8A2F110A', False)
        self.assertEqual(returnValue[0].get('ID'), '0003d3f5-6aa1-4475-adf6-50961c8bd739')


class UserOrganzieServiceTest(TestCase):

    #根据组织机构主键获取其指定分类下的子节点列表
    def test_GetChildrensById(self):
        print('根据组织机构主键获取其指定分类下的子节点列表测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.save()

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie1.fullname = 'o2'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.save()

        returnValue = OrganizeService.GetChildrensById(self, '07DF66FA-644E-4B1F-9994-AE7332796058')
        self.assertEqual(len(returnValue), 1)
        self.assertEqual(returnValue[0], '07DF66FA-644E-4B1F-9994-AE7332796059')


    #添加组织
    def test_Add(self):
        print('添加组织测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode,returnMessage,returnValue = OrganizeService.Add(self, organzie)
        self.assertEqual(returnValue, '07DF66FA-644E-4B1F-9994-AE7332796058')
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')


    #批量物理删除组织机构
    def test_BatchDelete(self):
        print('批量物理删除组织机构测试...  ' + str(datetime.datetime.now()))
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058','07DF66FA-644E-4B1F-9994-AE7332796059']
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        self.assertEqual(returnValue, '07DF66FA-644E-4B1F-9994-AE7332796058')
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')

        self.assertEqual(returnValue1, '07DF66FA-644E-4B1F-9994-AE7332796059')
        self.assertEqual(returnCode1, 11)
        self.assertEqual(returnMessage1, '新增成功。')

        self.assertEqual(OrganizeService.BatchDelete(self, ids), True)

        names = ['id','deletemark']
        values = ['07DF66FA-644E-4B1F-9994-AE7332796058']

        returnValue3 = Piorganize.objects.filter(Q(id = '07DF66FA-644E-4B1F-9994-AE7332796058') & Q(deletemark = 0))
        self.assertEqual(len(returnValue3), 0)
        returnValue3 = Piorganize.objects.filter(Q(id='07DF66FA-644E-4B1F-9994-AE7332796059') & Q(deletemark=0))
        self.assertEqual(len(returnValue3), 0)


    #批量移动组织机构
    def test_BatchMoveTo(self):
        print('批量移动组织机构测试...  ' + str(datetime.datetime.now()))
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059']
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        self.assertEqual(OrganizeService.BatchMoveTo(self, ids, '123456789'), True)

        for o in Piorganize.objects.filter(id__in=ids):
            self.assertEqual(o.parentid, '123456789')


    #批量保存
    def test_BatchSave(self):
        print('批量保存测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")

        org = [organzie, organzie1]
        returnValue = OrganizeService.BatchSave(self, org)
        self.assertEqual(returnValue, True)

        self.assertEqual(len(Piorganize.objects.filter(id__in=['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059'])), 2)


    #单个删除组织机构
    def test_Delete(self):
        print('单个删除组织机构测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)
        self.assertEqual(returnValue, '07DF66FA-644E-4B1F-9994-AE7332796058')
        OrganizeService.Delete(self, '07DF66FA-644E-4B1F-9994-AE7332796058')
        o = OrganizeService.GetEntity(self, '07DF66FA-644E-4B1F-9994-AE7332796058')
        self.assertEqual(OrganizeService.GetEntity(self, '07DF66FA-644E-4B1F-9994-AE7332796058').deletemark, 1)


    #获取组织机构列表
    def test_GetDT(self):
        print('获取组织机构列表测试...  ' + str(datetime.datetime.now()))
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059']
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        returnValue = OrganizeService.GetDT(self)
        self.assertEqual(len(returnValue), 2)

    #按主键获取组织机构列表
    def test_GetDTByIds(self):
        print('按主键获取组织机构列表测试...  ' + str(datetime.datetime.now()))
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059']
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        org = OrganizeService.GetDTByIds(self, ids)
        self.assertEqual(len(org), 2)

    #按父节点获取列表
    def test_GetDTByParent(self):
        print('按父节点获取列表测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 0
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        organzie2 = Piorganize()
        organzie2.id = '07DF66FA-644E-4B1F-9994-AE7332796050';
        organzie2.fullname = 'o1'
        organzie2.isinnerorganize = 1
        organzie2.deletemark = 0
        organzie2.enabled = 1
        organzie2.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie2.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie2.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie2)

        org = OrganizeService.GetDTByParent(self, '07DF66FA-644E-4B1F-9994-AE7332796059')
        self.assertEqual(len(org), 3)

    #按键值对获取列表
    def test_GetDTByValues(self):
        print('按键值对获取列表测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 1
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        organzie2 = Piorganize()
        organzie2.id = '07DF66FA-644E-4B1F-9994-AE7332796050';
        organzie2.fullname = 'o1'
        organzie2.isinnerorganize = 1
        organzie2.deletemark = 0
        organzie2.enabled = 1
        organzie2.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie2.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie2.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode2, returnMessage2, returnValue2 = OrganizeService.Add(self, organzie2)
        valueDic3 = {'id': '07DF66FA-644E-4B1F-9994-AE7332796050'}
        valueDic = {'parentid': '07DF66FA-644E-4B1F-9994-AE7332796059', 'id': '07DF66FA-644E-4B1F-9994-AE7332796050'}
        self.assertEqual(len(OrganizeService.GetDTByValues(self, valueDic)), 1)
        self.assertEqual(len(OrganizeService.GetDTByValues(self, valueDic3)), 1)

    #获取组织机构实体
    def test_GetEntity(self):
        print('获取组织机构实体测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        self.assertEqual(OrganizeService.GetEntity(self, '07DF66FA-644E-4B1F-9994-AE7332796058').parentid, '07DF66FA-644E-4B1F-9994-AE7332796059')

    #移动组织机构
    def test_MoveTo(self):
        print('移动组织机构测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        self.assertEqual(OrganizeService.GetEntity(self, '07DF66FA-644E-4B1F-9994-AE7332796058').parentid, '07DF66FA-644E-4B1F-9994-AE7332796059')
        OrganizeService.MoveTo(self, '07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796058')
        self.assertEqual(OrganizeService.GetEntity(self, '07DF66FA-644E-4B1F-9994-AE7332796058').parentid,
                         '07DF66FA-644E-4B1F-9994-AE7332796058')

    #批量打删除标志
    def test_SetDeleted(self):
        print('批量打删除标志测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie1 = Piorganize()
        organzie1.id = '07DF66FA-644E-4B1F-9994-AE7332796059';
        organzie1.fullname = 'o1'
        organzie1.isinnerorganize = 1
        organzie1.deletemark = 1
        organzie1.enabled = 1
        organzie1.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = OrganizeService.Add(self, organzie1)

        self.assertEqual(len(Piorganize.objects.all()) , 2)
        ids = ['07DF66FA-644E-4B1F-9994-AE7332796058', '07DF66FA-644E-4B1F-9994-AE7332796059']
        OrganizeService.SetDeleted(self, ids)
        self.assertEqual(Piorganize.objects.get(id='07DF66FA-644E-4B1F-9994-AE7332796058').deletemark, 1)
        self.assertEqual(Piorganize.objects.get(id='07DF66FA-644E-4B1F-9994-AE7332796059').deletemark, 1)

    #更新组织机构
    def test_Update(self):
        print('更新组织机构测试...  ' + str(datetime.datetime.now()))
        organzie = Piorganize()
        organzie.id = '07DF66FA-644E-4B1F-9994-AE7332796058';
        organzie.fullname = 'o1'
        organzie.isinnerorganize = 1
        organzie.deletemark = 0
        organzie.enabled = 1
        organzie.parentid = '07DF66FA-644E-4B1F-9994-AE7332796059'
        organzie.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        organzie.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = OrganizeService.Add(self, organzie)

        organzie.enabled = 0
        returnValue,returnMessage = OrganizeService.Update(self, organzie)
        self.assertEqual(returnValue, 14)

    #根据编号获取子节点列表
    def test_GetChildrensIdByCode(self):
        print('更新组织机构测试...SQLITE不支持部分SQL操作  ' + str(datetime.datetime.now()))


class UserStaffServiceTest(TestCase):

    #添加员工
    def test_Add(self):
        print('增加员工测试...  ' + str(datetime.datetime.now()))
        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staff.save()

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '李四'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.save()
        returnCode1, returnMessage1, returnValue1 = StaffService.Add(self, staff1)

        self.assertEqual(len(Pistaff.objects.all()), 2)

    #获取员工列表
    def test_GetDT(self):
        print('获取员工列表测试...  ' + str(datetime.datetime.now()))

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '李四'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = StaffService.Add(self, staff1)

        self.assertEqual(len(StaffService.GetDT(self)), 2)

    #分页查询
    def test_GetDTByPage(self):
        print('分页查询测试...  ' + str(datetime.datetime.now()))

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '李四'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode1, returnMessage1, returnValue1 = StaffService.Add(self, staff1)

        staffCount,returnValue = StaffService.GetDTByPage(self, '', 1, '')
        self.assertEqual(staffCount, 2)

    #获取员工实体
    def test_GetEntity(self):
        print('获取员工实体测试...  ' + str(datetime.datetime.now()))

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)

        staffId = staff.id
        self.assertEqual(StaffService.GetEntity(self, staffId).gender, '男')

    #更新员工
    def test_UpdateStaff(self):
        print('更新员工测试...  ' + str(datetime.datetime.now()))
        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)

        staffId = staff.id
        staff.gender = '女'
        returnCode,returnMessage = StaffService.UpdateStaff(self, staff)
        self.assertEqual(returnCode, 14)

    #按主键获取员工列表
    def test_GetDTByIds(self):
        print('按主键获取员工列表测试...  ' + str(datetime.datetime.now()))
        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '张三'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff1)
        staffId1 = staff1.id

        ids = [staffId, staffId1]

        self.assertEqual(len(StaffService.GetDTByIds(self, ids)), 2)

    #按组织结构获取员工列表
    def test_GetDTByOrganize(self):
        print('按组织机构主键获取员工列表测试...  ' + str(datetime.datetime.now()))

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        staff1 = Pistaff()
        staff1.id = uuid.uuid1()
        staff1.isdimission = 0
        staff1.deletemark = 0
        staff1.enabled = 1
        staff1.gender = '男'
        staff1.realname = '张三'
        staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff1)

        starffOrg = Pistafforganize()
        starffOrg.id = '17B501A9-697A-4226-816D-003903FC8AA5'
        starffOrg.deletemark = 0
        starffOrg.enabled = 1
        starffOrg.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.staffid = staffId
        starffOrg.organizeid = '07B501A9-697A-4226-816D-003903FC8AA5'
        starffOrg.save()

        self.assertEqual(len(StaffService.GetDTByOrganize(self, '07B501A9-697A-4226-816D-003903FC8AA5', False)), 1)

    #得到未设置组织机构的员工列表
    def test_GetDTNotOrganize(self):
        print('得到未设置组织机构的员工列表测试...  ' + str(datetime.datetime.now()))

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id
        #
        # staff1 = Pistaff()
        # staff1.id = uuid.uuid1()
        # staff1.isdimission = 0
        # staff1.deletemark = 0
        # staff1.enabled = 1
        # staff1.gender = '男'
        # staff1.realname = '张三'
        # staff1.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # staff1.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        # returnCode, returnMessage, returnValue = StaffService.Add(self, staff1)

        starffOrg = Pistafforganize()
        starffOrg.id = '07B501A9-697A-4226-816D-003903FC8AA8'
        starffOrg.deletemark = 0
        starffOrg.enabled = 1
        starffOrg.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        starffOrg.staffid = staffId
        starffOrg.organizeid = '07B501A9-697A-4226-816D-003903FC8AA5'
        starffOrg.save()
        pistafforganize = Pistafforganize.objects.all()
        print(pistafforganize)

    #员工关联用户
    def test_SetStaffUser(self):
        print('员工关联用户测试...  ' + str(datetime.datetime.now()))

        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, True)
        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, False)

    #删除员工关联的用户
    def test_DeleteUser(self):
        print('删除员工关联的用户测试...  ' + str(datetime.datetime.now()))

        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, True)

        userCheck = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(userCheck.deletemark, 0)

        returnValue = StaffService.DeleteUser(self, staffId)
        self.assertEqual(returnValue, True)

        userCheck = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(userCheck.deletemark, 1)

    #单个删除
    def test_Delete(self):
        print('删除员工关联的用户测试...  ' + str(datetime.datetime.now()))

        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, True)

        StaffService.Delete(self, staffId)

        self.assertEqual(len(Pistaff.objects.filter(id=staffId)), 0)
        userCheck = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(userCheck.deletemark, 1)

    #批量删除
    def test_BatchDelete(self):
        print('批量删除员工测试...  ' + str(datetime.datetime.now()))

        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, True)


        ids = [staffId]
        StaffService.BatchDelete(self, ids)

        self.assertEqual(len(Pistaff.objects.filter(id__in=ids)), 0)
        userCheck = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(userCheck.deletemark, 1)

    #批量打删除标志
    def test_SetDeleted(self):
        print('批量打员工删除标志测试...  ' + str(datetime.datetime.now()))

        user = Piuser()
        user.id = '0003d3f5-6aa1-4475-adf6-50961c8bd739'
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        UserSerivce.AddUser(self, user)

        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        returnValue = StaffService.SetStaffUser(self, staffId, '0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(returnValue, True)

        ids = [staffId]
        StaffService.SetDeleted(self, ids)

        staff = Pistaff.objects.get(id=staffId)
        self.assertEqual(staff.deletemark, 1)
        userCheck = Piuser.objects.get(id='0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(userCheck.deletemark, 1)

    #移动员工数据到指定组织机构
    def test_MoveTo(self):
        print('移动员工数据到指定组织机构测试...  ' + str(datetime.datetime.now()))

        staffOrg = Pistafforganize()
        staffOrg.id = uuid.uuid1()
        staffOrg.deletemark = 0
        staffOrg.enabled = 1
        staffOrg.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staffOrg.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staffOrg.organizeid = 'ssss'
        staffOrg.staffid = uuid.uuid1()
        staffOrgId = staffOrg.id
        staffId = staffOrg.staffid
        staffOrg.save()

        StaffService.MoveTo(self, staffId, 'mmmm')
        staffOrg = Pistafforganize.objects.get(id = staffOrgId)
        self.assertEqual(staffOrg.organizeid, 'mmmm')

    #批量移动员工数据到指定组织机构
    def test_BatchMoveTo(self):
        print('移动员工数据到指定组织机构测试...  ' + str(datetime.datetime.now()))

        staffOrg = Pistafforganize()
        staffOrg.id = uuid.uuid1()
        staffOrg.deletemark = 0
        staffOrg.enabled = 1
        staffOrg.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staffOrg.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staffOrg.organizeid = 'ssss'
        staffOrg.staffid = uuid.uuid1()
        staffOrgId = staffOrg.id
        staffId = staffOrg.staffid
        staffOrg.save()

        ids = [staffId]

        StaffService.BatchMoveTo(self, ids, 'mmmm')
        staffOrg = Pistafforganize.objects.get(id=staffOrgId)
        self.assertEqual(staffOrg.organizeid, 'mmmm')

    #获取主键
    def test_GetId(self):
        print('获取员工主键测试...  ' + str(datetime.datetime.now()))
        staff = Pistaff()
        staff.id = uuid.uuid1()
        staff.isdimission = 0
        staff.deletemark = 0
        staff.enabled = 1
        staff.gender = '男'
        staff.realname = '张三'
        staff.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        staff.modifiedon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode, returnMessage, returnValue = StaffService.Add(self, staff)
        staffId = staff.id

        valueDic = {'id':staffId}

        returnValue = StaffService.GetId(self, valueDic)
        self.assertEqual(len(returnValue), 1)

class PermissionItemServiceTest(TestCase):

    #添加操作权限项
    def test_Add(self):
        print('添加操作权限项测试...  ' + str(datetime.datetime.now()))
        item = Pipermissionitem()
        returnCode,returnMessage,returnValue = PermissionItemService.Add(self, item)
        self.assertEqual(returnCode, 11)

    #添加操作权限项
    def test_AddByDetail(self):
        print('添加操作权限项测试...  ' + str(datetime.datetime.now()))
        returnCode,returnMessage,returnValue = PermissionItemService.AddByDetail(self, '0001', 'Add_Enable')
        self.assertEqual(returnCode, 11)

    #获取权限项列表
    def test_GetDT(self):
        returnValue = PermissionItemService.GetDT(self)
        self.assertEqual(len(returnValue), 0)
        item = Pipermissionitem()
        PermissionItemService.Add(self, item)
        returnValue = PermissionItemService.GetDT(self)
        self.assertEqual(len(returnValue), 1)

    #获取权限项列表
    def test_GetDTByParent(self):
        item = Pipermissionitem()
        item.parentid=uuid.uuid1()
        PermissionItemService.Add(self, item)
        parentId = item.parentid
        returnValue = PermissionItemService.GetDTByParent(self, parentId)
        self.assertEqual(len(returnValue), 1)

    #按主键数组获取列表
    def test_GetDTByIds(self):
        item = Pipermissionitem()
        PermissionItemService.Add(self, item)
        item1 = Pipermissionitem()
        PermissionItemService.Add(self, item1)

        ids = [item.id, item1.id]

        returnValue = PermissionItemService.GetDTByIds(self, ids)
        self.assertEqual(len(returnValue), 2)
















