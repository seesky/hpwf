# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/28 8:55'

class ValidateUtil(object):

    def EnableCheckPasswordStrength(self, password):
        """
        密码强度检查
        Args:
            password (string): 密码
        Returns:
            returnValue (string): 是否通过
        """
        returnValue = False
        if password:
            returnValue = True
        else:
            returnValue = False

        isDigit = False
        isLetter = False

        if password:
            for t in password:
                if not isDigit:
                    isDigit = t.isdigit()
                if not isLetter:
                    isLetter = t.isalpha()
            returnValue = (isDigit and isLetter)
            if len(password) < 6:
                returnValue = False
        return returnValue