# _*_ coding: utf-8 _*_
__author__ = 'seesky@hstecs.com'
__date__ = '2018/12/27 13:51'

from Crypto.Cipher import AES
import base64
import os

class SecretHelper(object):

    def AESEncrypt(self, toEncrypt):
        """
        256位AES加密
        Args:
            toEncrypt (string): 待加密文本
        Returns:
            returnValue(string): 加密后文本
        """
        if toEncrypt.strip() == '':
            return ''

        key = '12345678901234567890123456789012'  # 加密时使用的key，只能是长度16,24和32的字符串
        BS = AES.block_size
        pad = lambda s: s + (BS - len(s) % BS) * chr(BS - len(s) % BS)
        cipher = AES.new(key)
        encrypted = cipher.encrypt(pad(toEncrypt))  # aes加密
        result = base64.b64encode(encrypted)  # base64 encode
        return result

    def AESDecrypt(self, toDecrypt):
        """
        256位AES解密
        Args:
            toDecrypt (string): 待解密文本
        Returns:
            returnValue(string): 解密后的文本
        """
        if toDecrypt.strip() == '':
            return ''

        key = '12345678901234567890123456789012'
        unpad = lambda s: s[0:-ord(s[-1])]
        cipher = AES.new(key)
        result2 = base64.b64decode(toDecrypt)
        decrypted = unpad(cipher.decrypt(result2))
        return decrypted
