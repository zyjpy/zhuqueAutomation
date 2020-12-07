#!/usr/bin/python
# -*- coding: utf-8 -*-
# import pytest
from selenium import webdriver
import time
import datetime
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
import  configparser
from PIL import ImageGrab
# from test_004_creatCourse import CreatCourse
config = configparser.ConfigParser()
config.read('E:/zhuqueAutomation/config/config.ini')
config_path = config.get('driver','personConfigPath')
excel_path = config.get('driver','excelPath')

wb = xlrd.open_workbook(excel_path)
sheet1 = wb.sheet_by_index(0)
sheet2 = wb.sheet_by_index(1)
sheet3 = wb.sheet_by_index(2)
sheet4 = wb.sheet_by_index(3)


class CheckCourse(unittest.TestCase):
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
        fp=webdriver.FirefoxProfile(config_path)
        dr = webdriver.Firefox(fp)
        self.driver = dr

        
    @classmethod
    def tearDownClass(self):
        pass
    def test_006_EditNopassCourseAndSave(self):
        self.driver.get("https://staging.www.qiaojianyun.com/basicadmin/#/course/examine/index")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(7,6)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,".course-name").click()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(2)
        #输入审核原因
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(43,2)).send_keys(sheet4.cell_value(43,3))
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(57,2)).click()
        #进入官网课程更多页
        self.driver.get("https://staging.www.qiaojianyun.com/#/courseCenterList")
        time.sleep(3)
        a = self.driver.find_elements_by_class_name("word")[0].text
        b = sheet1.cell_value(42,2)
        self.assertEqual(a, b, '发布失败，课程中心列表第一个课程的名称不对')
        self.driver.find_elements_by_class_name("word")[0].click()
        time.sleep(3)
        pic = ImageGrab.grab((0,0,1800,1040))
        pic.save('./screenshot/005_重新发布的课程的详情.jpg')
        self.driver.find_element(By.CSS_SELECTOR,sheet3.cell_value(17,2)).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH,sheet3.cell_value(18,4)).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,sheet3.cell_value(19,4)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("scene-title")[0].click()
        time.sleep(8)
        pic = ImageGrab.grab((0,0,1800,1040))
        pic.save('./screenshot/006_重新发布的课程的模型.jpg')


if __name__ == '__main__':
    unittest.main()
