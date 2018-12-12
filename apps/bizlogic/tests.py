import datetime
from django.test import TestCase
from apps.bizlogic.service.base import ExceptionService
from apps.bizlogic.service.base.UserService import UserSerivce
from apps.bizlogic.models import Ciexception
from apps.bizlogic.models import Piuser

# Create your tests here.
class ExceptionServiceTest(TestCase):

    def test_Add(self):
        pass

class UserServiceTest(TestCase):

    # 新增用户
    def test_AddUser(self):
        user = Piuser()
        user.username = 'wuyujia'
        user.realname = '邬育佳'
        user.isstaff = 1
        user.isvisible = 1
        user.isdimission = 1
        user.deletemark = 0
        user.enabled = 1
        user.createon = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        returnCode,returnMessage,returnValue = UserSerivce.AddUser(self, user, '', '')
        self.assertEqual(returnCode, 11)
        self.assertEqual(returnMessage, '新增成功。')
        self.assertEqual(returnValue, 11)

    # 根据用户id获取用户实体
    def test_GetEntity(self):
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
        UserSerivce.AddUser(self, user, '', '')
        user = UserSerivce.GetEntity('0003d3f5-6aa1-4475-adf6-50961c8bd739')
        self.assertEqual(user.realname, '邬育佳')

