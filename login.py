#-*- coding: utf-8 -*-
# Author:w k
import requests
import re
class Login(object):
    '''登陆的类'''
    def __init__(self,username,password):
        self.username = username
        self.password = password
        self.access_key = ''
        self.cookies = ''
    def logining(self):
        self.getKey()
        self.getCookies()
    def getKey(self):
        '''获取access_key'''
        keyUrl = 'https://api.kaaass.net/biliapi/user/login'
        argv = {'user':self.username,
                'passwd':self.password}
        tmp = requests.post(url=keyUrl,data=argv)
        res = tmp.json()
        self.access_key = str(res['access_key'])
    def getCookies(self):
        '''获取cookies'''
        CookiesUrl = 'https://api.kaaass.net/biliapi/user/sso?access_key='+self.access_key      
        tmp = requests.get(url=CookiesUrl)       
        res  = tmp.json()
        self.cookies = res["cookie"]
        return self.cookies


        
        
        
        



