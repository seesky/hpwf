import datetime
from django.test import TestCase
from apps.bizlogic.service.base import ExceptionService
from apps.bizlogic.models import Ciexception

from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.service.base.OrganizeService import OrganizeService

from apps.bizlogic.models import Piuser
from apps.bizlogic.models import Piorganize
from apps.bizlogic.models import Piuserrole

# Create your tests here.
class ExceptionServiceTest(TestCase):

    def test_Add(self):
        pass

class UserServiceTest(TestCase):

    # 新增用户
    def test_AddUser(self):
        #添加失败
        # user = Piuser()
        # returnCode, returnMessage, returnValue = UserSerivce.AddUser(self, user)
        # self.assertEqual(returnCode, 0)
        # self.assertEqual(returnMessage, '发生未知错误。')
        # self.assertEqual(returnValue, None)
        #添加成功
        user = Piuser()
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode,returnMessage,returnValue = UserSerivce.AddUser(self, user)
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')
        print('新增用户测试完成  ' + str(datetime.datetime.now()))

    # 根据用户id获取用户实体
    def test_GetEntity(self):
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
        print('根据用户id获取用户实体测试完成  ' + str(datetime.datetime.now()))

    #用户名是否重复
    def test_Exists(self):
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
        print('用户名是否重复测试完成  ' + str(datetime.datetime.now()))

    #根据用户名获取用户实体
    def test_GetEntityByUserName(self):
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
        print('根据用户名获取用户实体测试完成  ' + str(datetime.datetime.now()))

    #获取用户列表
    def test_GetDT(self):
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
        print('获取用户列表测试完成  ' + str(datetime.datetime.now()))

    #分页查询
    def test_GetDTByPage(self):
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
        print(returnValue.count)
        print(returnValue.num_pages)
        print(returnValue.page_range)
        print(returnValue.object_list)


class UserOrganzieServiceTest(TestCase):

    #根据组织机构主键获取其指定分类下的子节点列表
    def test_GetChildrensById(self):
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
        print('根据组织机构主键获取其指定分类下的子节点列表测试完成  ' + str(datetime.datetime.now()))