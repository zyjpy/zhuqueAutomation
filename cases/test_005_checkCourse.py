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

wb = xlrd.open_workbook(r'E:\zhuqueautomatiic\cases\case.xlsx')
sheet1 = wb.sheet_by_index(0)
sheet2 = wb.sheet_by_index(1)
sheet3 = wb.sheet_by_index(2)


class CreatCourse(unittest.TestCase):
    def isElementExist(self,element):
        flag = True
        try:
            self.driver.find_element_by_xpath(element)
            return flag
        except:
            flag = False
            return flag    
    @classmethod        
    def setUpClass(self):
        fp=webdriver.FirefoxProfile(r"C:\Users\zhangyihui\AppData\Roaming\Mozilla\Firefox\Profiles\jjgecsri.default-release")
        dr = webdriver.Firefox(fp)
        self.driver = dr
    @classmethod
    def tearDownClass(self):
        pass

    def test_001_creatWorkSaveDraft(self):
        '''官网创建作品保存为草稿'''
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.set_window_size(1600, 900)
        self.driver.set_window_rect(0,0)
        time.sleep(5)
if __name__ == '__main__':
    unittest.main()
