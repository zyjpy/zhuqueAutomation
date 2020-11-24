#!/usr/bin/python
# -*- coding: utf-8 -*-
# import pytest
from selenium import webdriver
import time 
import re
import autoit
import unittest
import xlrd
# import document
from xml.dom.minidom import parse
import selenium
from selenium.webdriver.support import expected_conditions as EC        # 等待元素可见的条件
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support import expected_conditions
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
import urllib.request
import base64
import numpy as np
import urllib
from cv2 import cv2
from xml.dom.minidom import parse



wb = xlrd.open_workbook(r'E:\zhuqueAutomation\cases\case.xlsx')

sheet1 = wb.sheet_by_index(0)
sheet2 = wb.sheet_by_index(1)
sheet3 = wb.sheet_by_index(2)


class Login(unittest.TestCase):
    fp=webdriver.FirefoxProfile(r"C:\Users\zhangyihui\AppData\Roaming\Mozilla\Firefox\Profiles\jjgecsri.default-release")
    dr = webdriver.Firefox(fp)
    def isElementExist(self,element):
        flag = True
        try:
            self.dr.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag

    def setUp(self,driver= dr):
        self.driver = driver

    def tearDown(self):
        time.sleep(5)

    def test_001_loginOfficeByAccount(self):
        '''账号密码登录官网'''
        print("账号密码登录官网")
        self.driver.get("https://staging.www.qiaojianyun.com/#/login")
        self.driver.set_window_size(1600, 900)
        self.driver.set_window_rect(0,0)
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--medium > .el-input__inner").send_keys("admin032")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--small > .el-input__inner").send_keys("123456")
        self.driver.find_element_by_xpath('//span[contains(.,"登录")]').click()
        time.sleep(2)
        k = 1
        while True:
            #获取到两张图片链接
            src = self.driver.find_element_by_xpath('//div[2]/div/div/div/img').get_attribute('src')
            img = src.split(',')[1]
            bg_img_scr = base64.b64decode(img)
            with open('./bg.jpg', 'wb') as f:
                f.write(bg_img_scr) 

            src = self.driver.find_element_by_xpath('//div[2]/div/div[2]/div/div/div/img').get_attribute('src')
            img = src.split(',')[1]
            front_img_src = base64.b64decode(img)
            with open('./front.jpg', 'wb') as f:
                f.write(front_img_src)  

            #读取图片
            bg = cv2.imread('./bg.jpg')
            front = cv2.imread('./front.jpg')   

            #灰度处理
            bg = cv2.cvtColor(bg,cv2.COLOR_BGR2GRAY)
            front = cv2.cvtColor(front,cv2.COLOR_BGR2GRAY)  

            #去掉滑块黑色部分
            front = front[front.any(1)]#0表示黑色，1表示高亮部分   

            #匹配->cv图像匹配算法
            result = cv2.matchTemplate(bg, front, cv2.TM_CCOEFF_NORMED)#match匹配,Template模板;精度高，速度慢的方法
            index_max = np.argmax(result)#返回的是一维的位置，最大值索引   

            #反着推最大值的二维位置，和opencv是相反的
            x, y = np.unravel_index(index_max, result.shape)
            print ("二维中坐标的位置：",x, y)
            print ("正在进行第%s次滑动验证"%k)
            drop = self.driver.find_element_by_xpath('//div[2]/div/div/i')    
            ActionChains(self.driver).drag_and_drop_by_offset(drop, xoffset=y+10, yoffset=0).perform()
            time.sleep(3)
            #验证成功后获取“验证成功”，直到找到“验证成功”才跳出while True循环
            if self.isElementExist("//div[@id='kecheng']"):
                print("找到社区啦")
                break
            else:
                print ('第%s次验证失败...'%k,'\n')
                time.sleep(1)
            k = k + 1
        print ('已经通过验证码!!!')

if __name__ == '__main__':
    unittest.main()