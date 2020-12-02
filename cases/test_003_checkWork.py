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
import  configparser

config = configparser.ConfigParser()
config.read('E:/zhuqueAutomation/config/config.ini')
config_path = config.get('driver','personConfigPath')
excel_path = config.get('driver','excelPath')

wb = xlrd.open_workbook(excel_path)
sheet1 = wb.sheet_by_index(0)
sheet2 = wb.sheet_by_index(1)
sheet3 = wb.sheet_by_index(2)
sheet4 = wb.sheet_by_index(3)

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
        fp=webdriver.FirefoxProfile(config_path)
        dr = webdriver.Firefox(fp)
        self.driver = dr
    @classmethod
    def tearDownClass(self):
        self.driver.quit()

    def test_001_loginOperation(self):
        '''登录运营后台'''
        self.driver.get("https://staging.www.qiaojianyun.com/basicadmin/#/login")
        self.driver.set_window_size(1600, 1040)
        self.driver.set_window_rect(0,0)
        time.sleep(4)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--medium > .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--medium > .el-input__inner").send_keys("zyj")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--small > .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--small > .el-input__inner").send_keys("12345678")
        time.sleep(1)
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
            if self.isElementExist("//div[@id='tab-/wel/index']"):
                print("进入首页")
                break
            else:
                print ('第%s次验证失败...'%k,'\n')
                time.sleep(1)
            k = k + 1
        print ('已经通过验证码!!!,登录运营后台成功')
    def test_002_checkWorkNopass(self):
        '''审核作品不通过'''
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(14,2)).click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, sheet4.cell_value(16,4)).click()
        time.sleep(2)
        #点击审核不通过的第三个作品 猴子2
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(17,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(31,2)).click()
        time.sleep(3)
        js = 'document.getElementsByClassName("el-select-dropdown__item")[36].click()'
        self.driver.execute_script(js)
        time.sleep(1)
        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").send_keys(sheet4.cell_value(41,3))
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, sheet4.cell_value(40,4)).click()
        time.sleep(2)
        #点击审核不通过的第二个作品 猴子3
        self.driver.find_element(By.XPATH, sheet4.cell_value(18,4)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(31,2)).click()
        time.sleep(3)
        js = 'document.getElementsByClassName("el-select-dropdown__item")[36].click()'
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").clear()
        self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").send_keys(sheet4.cell_value(41,3))
        time.sleep(0.5)
        self.driver.find_element(By.XPATH, sheet4.cell_value(40,4)).click()
        time.sleep(2)
        #点击审核通过第三个作品 猴子4
    def test_003_checkWorkPass(self):
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(19,2)).click()
        time.sleep(1)
        #点击打开作品状态下拉框
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(31,2)).click()
        time.sleep(3)
        js = 'document.getElementsByClassName("el-select-dropdown__item")[36].click()'
        self.driver.execute_script(js)
        self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").clear()
        self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").send_keys(sheet4.cell_value(39,3))

        # self.driver.find_element(By.XPATH, "//label[contains(.,'作品状态')]").click()
        # time.sleep(2)
        # self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").clear()
        # self.driver.find_element(By.XPATH, "//div[3]/div/div/textarea").send_keys(sheet4.cell_value(41,3))
        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        # time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(31,2)).click()
        js = 'document.getElementsByClassName("el-select-dropdown__item")[22].click()'
        self.driver.execute_script(js)


        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet4.cell_value(35,2)).click()
        time.sleep(1)
        js = 'document.getElementsByClassName("el-select-dropdown__item")[24].click()'
        self.driver.execute_script(js)
        #关闭作品分类选择框
        ActionChains(self.driver).send_keys(Keys.ESCAPE).perform()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//label[contains(.,'作品状态')]").click()

        time.sleep(0.5)
        self.driver.find_element(By.XPATH, sheet4.cell_value(40,4)).click()
        time.sleep(1)
        self.driver.get("https://staging.www.qiaojianyun.com/#/login")
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--medium > .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--medium > .el-input__inner").send_keys("admin032")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--small > .el-input__inner").clear()
        self.driver.find_element(By.CSS_SELECTOR, ".el-input--small > .el-input__inner").send_keys("123456")
        time.sleep(1)
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
                print("进入首页")
                break
            else:
                print ('第%s次验证失败...'%k,'\n')
                time.sleep(1)
            k = k + 1
        print ('已经通过验证码!!!,登录官网成功')
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(11,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(13,2)).click()
        time.sleep(2)
        #断言作品社区第三个位置不存在这个作品 猴子2
        a = self.driver.find_elements_by_class_name('word')[2].text
        b = sheet1.cell_value(46,2)
        self.assertNotEqual(a, b, '审核不通过，但在社区平台看到了这个作品：猴子2')
        #断言作品社区第二个位置不存在这个作品猴子3
        a = self.driver.find_elements_by_class_name('word')[1].text
        b = sheet1.cell_value(47,2)
        self.assertNotEqual(a, b, '审核不通过，但在社区平台看到这个作品：猴子3')
        #审核通过，断言作品社区第1个位置存在这个作品猴子4
        a = self.driver.find_elements_by_class_name('word')[0].text
        b = sheet1.cell_value(48,2)
        self.assertEqual(a, b, '审核不通过，社区平台看到了这个作品：猴子4')
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(20,2)).click()
        time.sleep(2)
        #断言我的在线作品页第三个位置没有作品 猴子2
        a = self.driver.find_elements_by_class_name('ellipsis_box')[2].text
        b = b = sheet1.cell_value(49,2)
        self.assertNotEqual(a, b, '审核不通过，但在线作品页看到这个作品：猴子2')
        #断言我的在线作品页第二个位置没有作品 猴子3
        a = self.driver.find_elements_by_class_name('ellipsis_box')[1].text
        b = b = sheet1.cell_value(50,2)
        self.assertNotEqual(a, b, '审核不通过，但在线作品页看到这个作品：猴子3')
        #审核通过，断言我的在线作品页第一个位置作品为 猴子4
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(51,2)
        self.assertEqual(a, b, '审核通过，在线作品页看到这个作品：猴子4')

    def test_004_republishWork(self):
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.set_window_size(1600, 1040)
        self.driver.set_window_rect(0,0)
        time.sleep(2)
        self.driver.find_element_by_css_selector(sheet2.cell_value(21,2)).click()
        #断言审核状态页第三个位置的作品的状态为未通过
        time.sleep(2)

        a = self.driver.find_elements_by_class_name('cell')[18].text
        b = b = sheet1.cell_value(52,2)
        self.assertEqual(a, b, '审核不通过，但在线作品页看到第三个位置的作品的状态错误')
        #断言审核状态页第二个位置的作品的状态为未通过
        a = self.driver.find_elements_by_class_name('cell')[13].text
        b = b = sheet1.cell_value(53,2)
        self.assertEqual(a, b, '审核不通过，但在线作品页看到第二个位置的作品的状态错误')
        #审核通过，断言审核状态页第一个位置作品的状态为 已通过
        a = self.driver.find_elements_by_class_name('cell')[8].text
        b = sheet1.cell_value(54,2)
        self.assertEqual(a, b, '审核通过，审核状态页第一个位置作品的状态为 已审核')
        #重新编辑第二个作品猴子3，保存到草稿
        self.driver.find_element_by_css_selector(sheet2.cell_value(98,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(99,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(99,2)).send_keys(sheet2.cell_value(99,3))

        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(5,1)).click()
        time.sleep(1)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(100,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)
        #删除介绍图
        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(101,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)        
        if self.isElementExist("//li/div/span"):
            print("上传介绍图成功")
        else:
            self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
            time.sleep(2)
            autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(101,2))
            autoit.control_click("文件上传","[Class:Button; instance:1]")        
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(102,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(102,2)).send_keys(sheet2.cell_value(102,3))
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(9,2)).click()
        time.sleep(2)
        #选择第三个素材
        self.driver.find_elements_by_class_name('list-item-title')[2].click()
        time.sleep(1)
        #点击发布
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(11,2)).click()
        time.sleep(2)
        #点击我的草稿，查看草稿是否存在
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(19,2)).click()
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(55,2)
        self.assertEqual(a, b, '在审核状态页编辑并保存,失败，在我的在线作品页看不到保存的作品')
        #点击审核状态页
        self.driver.find_element_by_css_selector(sheet2.cell_value(21,2)).click()
        time.sleep(2)
        
        self.driver.find_element_by_css_selector(sheet2.cell_value(98,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(99,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(99,2)).send_keys(sheet2.cell_value(99,3))

        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(5,1)).click()
        time.sleep(1)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(100,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)
        #删除介绍图
        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(101,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)        
        if self.isElementExist("//li/div/span"):
            print("上传介绍图成功")
        else:
            self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
            time.sleep(2)
            autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(101,2))
            autoit.control_click("文件上传","[Class:Button; instance:1]")        
        time.sleep(5)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(102,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(102,2)).send_keys(sheet2.cell_value(102,3))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(9,2)).click()
        time.sleep(2)
        #选择第三个素材
        self.driver.find_elements_by_class_name('list-item-title')[2].click()
        time.sleep(2)
        #点击发布到社区平台
        self.driver.find_element(By.XPATH,sheet2.cell_value(26,4)).click()
        time.sleep(2)
        #断言审核状态页第二个位置的作品的状态为未通过
        a = self.driver.find_elements_by_class_name('cell')[13].text
        b = b = sheet1.cell_value(56,2)
        self.assertEqual(a, b, '再次发布作品失败，但审核页看到第二个位置的作品的状态没有变成未审核')

        #社区平台
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet3.cell_value(11,2)).click()
        #最新发布排序
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,sheet3.cell_value(13,2)).click()
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('word')[1].text
        b = sheet1.cell_value(57,2)
        self.assertEqual(a, b, '再次发布作品失败，社区平台没有看到这个作品')






        







        


        



        
        

if __name__ == '__main__':
    unittest.main()