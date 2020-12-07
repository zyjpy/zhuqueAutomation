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

    def test_001_loginOperation(self):
        '''登录运营后台'''
        #登录运营后台
        self.driver.get("https://staging.www.qiaojianyun.com/basicadmin/#/login")
        self.driver.set_window_size(1800,1040)
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
    def test_002_checkNopass(self):
        '''第三课程斑马2审核不通过'''
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(2,2)).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,sheet4.cell_value(4,4)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(6,2)).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,sheet4.cell_value(54,4)).click()
        time.sleep(1)
        #点击两次向下按键，审核状态为不通过
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(1)
        ActionChains(self.driver).send_keys(Keys.ENTER).perform()
        #输入审核原因
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(43,2)).send_keys(sheet4.cell_value(43,3))
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(57,2)).click()
    def test_003_checkpass(self):
        '''第一课程和第二课程都审核通过，第一课程修改分类为第2和第3分类'''
        #先审核第二课程
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(7,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,".course-name").click()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        ActionChains(self.driver).send_keys(Keys.DOWN).perform()
        time.sleep(2)
        #输入审核原因
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(43,2)).send_keys(sheet4.cell_value(43,3))
        #选择选择难度为中级
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(46,2)).click()
        #售价为19.9
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(59,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(59,2)).send_keys("19.99")
        time.sleep(1)
        #现价为0.01
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(60,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(60,2)).send_keys("0.01")
        time.sleep(1)
        #删除分类自然科学和走进历史
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(61,2)).click()
        time.sleep(0.5)
        self.driver.find_element(By.XPATH,"//div[2]/div/div/div/span/span/i").click()
        #选择自然科学和多彩的生物的分类
        self.driver.find_element(By.XPATH,sheet4.cell_value(49,4)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("el-select-dropdown__item")[31].click()
        time.sleep(0.5)
        self.driver.find_elements_by_class_name("el-select-dropdown__item")[32].click()
        time.sleep(1)
        #保存审核
        self.driver.find_element(By.CSS_SELECTOR,sheet4.cell_value(57,2)).click()
        time.sleep(2)
        #审核第一课程
        #点击课程审核页
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

    def test_004_checkCourseCentre(self):
        '''检查官网的课程的审核结果'''
        self.driver.get("https://staging.www.qiaojianyun.com/#/login")
        self.driver.set_window_size(1800,1040)
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
        time.sleep(2)
        #点击课程中心
        self.driver.find_element(By.ID,"kecheng").click()
        time.sleep(3)
        #断言课程中心页斑马3的作品的属性，名称，简介，原价，现价，难度
        a = self.driver.find_elements_by_class_name('word')[1].text
        b = sheet1.cell_value(63,2)
        self.assertEqual(a, b, '课程审核通过后，课程平台没有看到了这个课程：斑马3')
        a = self.driver.find_elements_by_class_name('description')[1].text
        b = sheet1.cell_value(64,2)
        self.assertEqual(a, b, '课程审核通过后，课程平台的课程简介不对')
        a = self.driver.find_elements_by_class_name('title')[3].text
        b = sheet1.cell_value(66,2)
        self.assertEqual(a, b, '课程审核通过后课程平台的课程现价不对')
        a = self.driver.find_elements_by_class_name('el-tag')[1].text
        b = sheet1.cell_value(67,2)
        self.assertEqual(a, b, '课程审核通过后课程平台的难度应该为中级')
        self.driver.find_elements_by_class_name('pic')[1].get_attribute('src')
        # a = self.driver.find_elements_by_class_name('el-tag')[1].text
        # b = sheet1.cell_value(68,2)
        # self.assertEqual(a, b, '课程审核通过后课程平台的作品的图标不对')
        
        #断言课程中心页斑马4的作品的属性，名称，简介，原价，现价，难度
        a = self.driver.find_elements_by_class_name('word')[0].text
        b = sheet1.cell_value(69,2)
        self.assertEqual(a, b, '课程审核通过后，课程平台没有看到了这个课程：斑马4')
        a = self.driver.find_elements_by_class_name('description')[0].text
        b = sheet1.cell_value(70,2)
        self.assertEqual(a, b, '课程审核通过后，课程平台的课程简介不对')
        a = self.driver.find_elements_by_class_name('title')[2].text
        b = sheet1.cell_value(72,2)
        self.assertEqual(a, b, '课程审核通过后课程平台的课程现价不对')
        a = self.driver.find_elements_by_class_name('el-tag')[0].text
        b = sheet1.cell_value(73,2)
        self.assertEqual(a, b, '课程审核通过后课程平台的难度应该为初级')
        self.driver.find_elements_by_class_name('pic')[0].get_attribute('src')
        # a = self.driver.find_elements_by_class_name('el-tag')[0].text
        # b = sheet1.cell_value(74,2)
        # self.assertEqual(a, b, '课程审核通过后课程平台的作品的图标不对')
        #断言斑马2不在课程中心
        a = self.driver.find_elements_by_class_name('word')[2].text
        b = sheet1.cell_value(75,2)
        self.assertNotEqual(a, b, '课程审核不通过后，课程平台看到了这个课程：斑马2')
    def test_005_checkResultOfDetail(self):
        '''点击斑马3,进入详情页,断言日期'''

        #点击斑马3
        self.driver.find_elements_by_class_name('pic')[1].click()
        time.sleep(5)
        pic = ImageGrab.grab((0,0,1800,1040))
        pic.save('./screenshot/003_课程详情.jpg')

        #断言名称是斑马3
        a = self.driver.find_element_by_xpath('//div[2]/div/div/div[2]/div/div').text
        b = sheet1.cell_value(76,2)
        self.assertEqual(a, b, '课程详情页课程名称错误')
        #断言难度是中级
        a = self.driver.find_element_by_xpath('//div[2]/div/div/div[2]/div/div[2]').text
        b = sheet1.cell_value(77,2)
        self.assertEqual(a, b, '课程详情页课程难度错误')
        #断言课程作者是集合
        a = self.driver.find_element_by_xpath('//div[2]/div/div/div[2]/div[2]/div[2]').text
        b = sheet1.cell_value(78,2)
        self.assertEqual(a, b, '课程详情页课程作者错误')
        #断言上传时间是在今天
        timeNow = datetime.datetime.now().strftime('%Y-%m-%d')
        timeCreat = self.driver.find_element(By.XPATH,"//div[2]/div/div/div[2]/div[3]/div").text
        timeDate = timeCreat.partition(timeNow)
        print(timeDate[1])
        self.assertEqual(timeNow, timeDate[1], '课程详情的时间不对')
        #断言课程简介
        a = self.driver.find_element_by_xpath("//pre[contains(.,'斑马3简介')]").text
        b = sheet1.cell_value(80,2)
        self.assertEqual(a, b, '课程详情页课程简介错误')
        #断言现价
        a = self.driver.find_element_by_xpath('//div[2]/div/div/div[2]/div[5]/div').text
        b = sheet1.cell_value(81,2)
        self.assertEqual(a, b, '课程详情页现价错误')
        #断言存在加入购物车按钮和立即结算按钮,打开课程章节页
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR,sheet3.cell_value(17,2)).click()
        time.sleep(1)
        #章节1名称
        a = self.driver.find_elements_by_class_name('chapter-header-title__label')[0].text
        b = sheet1.cell_value(85,2)
        self.assertEqual(a, b, '章节1名称错误')
        #章节1介绍
        a = self.driver.find_element_by_xpath("//pre[contains(.,'章节1介绍')]").text
        b = sheet1.cell_value(86,2)
        self.assertEqual(a, b, '章节1简介错误')
        #点击第一章节，展开
        time.sleep(1)
        self.driver.find_elements_by_class_name("el-collapse-item__arrow")[0].click()
        time.sleep(1)
        #点击第一章节第1课时的可试看
        self.driver.find_elements_by_class_name("title_right")[0].click()
        time.sleep(2)
        #断言第一章节节第一课时的场景文件名称
        a = self.driver.find_elements_by_class_name('el-popover__reference')[1].text
        b = sheet1.cell_value(87,2)
        self.assertEqual(a, b, '场景文件名称错误')

        #断言第一章节第一课时的课件名称
        a = self.driver.find_elements_by_class_name('word')[1].text
        b = sheet1.cell_value(88,2)
        self.assertEqual(a, b, '课件名称错误')
        #点击课件并截图
        self.driver.find_elements_by_class_name('el-popover__reference')[1].click()
        time.sleep(7)
        pic = ImageGrab.grab((0,0,1800,1040))
        pic.save('./screenshot/004_课程详情页预览模型.jpg')
        self.driver.find_element_by_class_name('el-dialog__close').click()
        time.sleep(1)

    def test_006_EditNopassCourseAndSave(self):
        '''编辑不通过的课程并保存草稿'''
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(29,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(78,2)).click()
        time.sleep(3)
        #编辑审核状态页第三个课程
        self.driver.find_element(By.XPATH,sheet2.cell_value(85,4)).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH,sheet2.cell_value(105,4)).click()
        time.sleep(3)
        #编辑课程名称斑马22
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(39,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(39,2)).send_keys(sheet2.cell_value(112,3))
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(41,4)).click()
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(120,4)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("tabs-item")[0].click()
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(54,2)).click()
        time.sleep(3)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(40,2)
        self.assertEqual(a, b, '在审核状态页编辑并保存,结果失败，在我草稿页看不到保存的作品')


    def test_007_republishCourse(self): 
        '''编辑不通过的课程并发布''' 
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(78,2)).click()
        time.sleep(2)
        #编辑审核状态页第三个课程
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(103,2)).click()
        time.sleep(1)
        #编辑课程名称斑马22
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(39,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(39,2)).send_keys(sheet2.cell_value(112,3))

        #编辑课程的icon
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(61,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(113,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(4)
        #删除第一张课程介绍图
        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)
        #编辑课程的介绍图
        js = 'document.getElementsByClassName("el-icon-plus")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(113,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(6)
        if self.isElementExist("//li/div/span"):
            print("上传成功")
        else:
            self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(37,2)).click()
            time.sleep(1)
            autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(114,2))
            autoit.control_click("文件上传","[Class:Button; instance:1]")
            time.sleep(5)
        self.driver.find_element(By.XPATH, sheet2.cell_value(41,4)).click()

        #编辑更新章节1的名称
        time.sleep(2)
        self.driver.find_elements_by_class_name("el-button--primary")[40].click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).send_keys(sheet2.cell_value(115,3))
        time.sleep(2)
        #编辑更新章节1的介绍
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).send_keys(sheet2.cell_value(116,3))        
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(45,2)).click()
        time.sleep(1)
        chaptersIntroduce2 = self.driver.find_elements_by_class_name('chapter-header-title__desc')[0].text
        print("更改后的章节介绍=" +chaptersIntroduce2)
        #编辑更新章节1的课时1的名称
        #点击弹出已有课时列表
        self.driver.find_element(By.XPATH, sheet2.cell_value(67,4)).click()
        #点击编辑第一课时
        self.driver.find_element(By.XPATH, sheet2.cell_value(68,4)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("el-input__inner")[6].clear()
        self.driver.find_elements_by_class_name("el-input__inner")[6].send_keys(sheet2.cell_value(117,3))
        # #删除第一个场景文件
        # self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(70,2)).click()
        #添加场景文件
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(48,2)).click()
        #选择第三个场景文件：内脏
        time.sleep(2)
        self.driver.find_elements_by_class_name("list-item-title")[2].click()
        time.sleep(1)
        sceneName2 = self.driver.find_elements_by_class_name('scene-item')[0].text
        print("更改后的场景文件=" +sceneName2)

        #上传课件，先删除课件
        # js = 'document.getElementsByClassName("el-icon-delete deleteIcon")[1].click()'
        # self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(50,4)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(73,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(8)
        pptName2 = self.driver.find_elements_by_class_name('courseware-name')[0].text
        print("更改后的课件名" +pptName2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(74,2)).click()
        time.sleep(1)
        lessonName2 = self.driver.find_elements_by_class_name('chapter-header-title__label')[1].text
        print("更改后的课时标题=" +lessonName2)
        chaptersName2 = self.driver.find_elements_by_class_name('chapter-header-title__label')[0].text
        print("更改后的章节标题=" +chaptersName2)
        #点击发布到课程社区
        self.driver.find_element(By.XPATH, sheet2.cell_value(86,4)).click()
        #断言审核状态有新发布的课程
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(78,4)).click()
        #点击待审核页
        self.driver.find_element(By.XPATH, sheet2.cell_value(83,4)).click() 
        time.sleep(1)
        a = self.driver.find_elements_by_class_name("cell")[7].text
        b = sheet1.cell_value(41,2)
        self.assertEqual(a, b, '发布失败，审核状态页第一个课程的名称不对')
        
        #登录运营后台审核
        self.driver.get("https://staging.www.qiaojianyun.com/basicadmin/#/course/examine/index")
        self.driver.set_window_size(1800,1040)
        self.driver.set_window_rect(0,0)
        time.sleep(2)
        if self.isElementExist("//div[@id='tab-user']"):
            print("账号密码登录运营后台")
            self.driver.get("https://staging.www.qiaojianyun.com/#/login")
            self.driver.set_window_size(1800,1040)
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
            print ('登录运营后台成功!!!')
            time.sleep(1)
        else:
            pass
        time.sleep(3)
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

        #跳转到运营后台审核页
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
