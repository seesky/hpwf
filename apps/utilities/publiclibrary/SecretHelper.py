# _*_ coding: utf-8 _*_
__author__ = 'baxuelong@163.com'
__date__ = '2018/12/27 13:51'

from Crypto.Cipher import AES
import base64
import os

class SecretHelper(object):

    def AESEncrypt(toEncrypt):
        """
        256位AES加密
        Args:
            toEncrypt (string): 待加密文本
        Returns:
            returnValue(string): 加密后文本
        """
        if toEncrypt.strip() == '':
            return ''

        key = '12345678901234567890123456789012'.encode()  # 加密时使用的key，只能是长度16,24和32的字符串
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        x = pad(toEncrypt)
        x = x.encode()
        cipher = AES.new(key, AES.MODE_ECB)
        encrypted = cipher.encrypt(x)  # aes加密
        result = base64.b64encode(encrypted)  # base64 encode
        return result

    def AESDecrypt(toDecrypt):
        """
        256位AES解密
        Args:
            toDecrypt (string): 待解密文本
        Returns:
            returnValue(string): 解密后的文本
        """
        if toDecrypt.strip() == '':
            return ''

        key = '12345678901234567890123456789012'.encode()
        unpad = lambda s: s[0:-ord(s[-1])]
        cipher = AES.new(key, AES.MODE_ECB)
        # missing_padding = 4 - len(toDecrypt) % 4
        # # toDecrypt.lstrip('b\'')
        # # toDecrypt.rstrip('\'')
        # if toDecrypt:
        #     toDecrypt = toDecrypt + (r'=' * missing_padding)
        result2 = base64.b64decode(toDecrypt)
        #result2 = base64.urlsafe_b64decode(toDecrypt)
        result2 = cipher.decrypt(result2)
        result2 = str(result2, encoding='utf-8')
        decrypted = unpad(result2)
        return decrypted
