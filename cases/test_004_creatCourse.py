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
        pass

    def test_001_creatWorkSaveDraft(self):
        '''官网创建作品保存为草稿'''
        print("官网创建作品保存为草稿")
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.set_window_size(1600, 900)
        self.driver.set_window_rect(0,0)
        time.sleep(5)

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(29,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(30,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(31,2)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name(sheet2.cell_value(32,2))[6].click()
        self.driver.find_elements_by_class_name(sheet2.cell_value(33,2))[7].click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(34,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(35,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(36,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(37,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(38,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(39,2)).send_keys(sheet2.cell_value(39,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(40,2)).send_keys(sheet2.cell_value(40,3))
        
        self.driver.find_element(By.XPATH, sheet2.cell_value(41,4)).click()
        #添加第一章节
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(42,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).send_keys(sheet2.cell_value(43,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).send_keys(sheet2.cell_value(44,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(45,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(46,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(47,2)).send_keys(sheet2.cell_value(47,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(48,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(49,2)).click()
        time.sleep(1)
        #添加第一章的第一课时
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(50,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(51,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)

        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sheet2.cell_value(52,2))))
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(52,2)).click()
        #添加第二章节
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(42,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).send_keys(sheet2.cell_value(43,4))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).send_keys(sheet2.cell_value(44,4))
        WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sheet2.cell_value(45,2))))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(45,2)).click()
        time.sleep(2)
        #添加第二章的第一课时
        self.driver.find_elements_by_class_name("el-button--success")[1].click()

        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sheet2.cell_value(46,3))))
        # self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(46,3)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(47,2)).send_keys(sheet2.cell_value(47,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(48,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(49,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(50,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(51,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)
        # WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sheet2.cell_value(52,2))))
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(52,2)).click()
        time.sleep(1)
        #保存课程到草稿
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(53,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(29,2)
        self.assertEqual(a, b, '创建失败，创建的课程不在草稿箱中')
    def test_002_copyCourse(self):
        '''复制课程'''
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(1)
        js = 'document.getElementsByClassName("backRotate")[0].click()'
        self.driver.execute_script(js)        
        time.sleep(1)
        #点击复制按钮
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(16,2)).click()
        #复制的第二个是为了EditAndpublish
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(54,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(2)
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".tabs-title > div:nth-child(2)").click()
        time.sleep(1)

        js = 'document.getElementsByClassName("backRotate")[0].click()'
        self.driver.execute_script(js)  
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(16,2)).click()

        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[1].text
        b = sheet1.cell_value(30,2)
        self.assertEqual(a, b, '复制失败')
        time.sleep(2)
    def test_003_deleteCourse(self):
        '''删除课程'''
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, ".tabs-title > div:nth-child(2)").click()
        time.sleep(1)
        js = 'document.getElementsByClassName("backRotate")[0].click()'
        self.driver.execute_script(js)

        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(13,2)).click()
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(31,2)
        self.assertNotEqual(a, b, '删除失败，删除的作品还在草稿箱中')
    def test_004_EditCourseAndSave(self):
        '''官网编辑课程并保存'''
        global courseIcon,CreatCourse,chaptersName,chaptersIntroduce,sceneName,pptName,lessonName
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div/div[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div[2]/div/div[2]/div/div").click()
        #点击右下角课程按钮
        time.sleep(3)
        self.driver.find_element(By.XPATH, sheet2.cell_value(56,4)).click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(14,2)).click()
        #编辑课程的名称
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(39,2)).clear()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(39,2)).send_keys(sheet2.cell_value(57,3))
        time.sleep(1)
        #编辑课程的icon
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(61,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(58,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        #删除第一张课程介绍图

        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)

        #编辑课程的介绍图
        js = 'document.getElementsByClassName("el-icon-plus")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)
        # self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(37,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(58,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        #编辑课程简介
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(63,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(63,2)).send_keys(sheet2.cell_value(63,3))

        time.sleep(1)
        #记录课程图标
        courseIcon = self.driver.find_element_by_xpath("//form/div[2]/div/div/img").get_attribute("src")
        print(courseIcon)
        #记录课程介绍图
        courseImg = self.driver.find_element_by_class_name("el-upload-list__item-thumbnail").get_attribute("src")
        print(courseImg)
        time.sleep(1)
        self.driver.find_element(By.XPATH, sheet2.cell_value(41,4)).click()
        #编辑更新章节1的名称
        time.sleep(1)
        self.driver.find_element(By.XPATH, sheet2.cell_value(64,4)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).send_keys(sheet2.cell_value(65,3))
        time.sleep(1)
        chaptersName = self.driver.find_elements_by_class_name('chapter-header-title__label')[0].text
        print("更改后的章节标题=" +chaptersName)
        #编辑更新章节1的介绍
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).send_keys(sheet2.cell_value(66,3))        
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(45,2)).click()
        time.sleep(1)
        chaptersIntroduce = self.driver.find_elements_by_class_name('chapter-header-title__desc')[0].text
        print("更改后的章节介绍=" +chaptersIntroduce)
        #编辑更新章节1的课时1的名称
        self.driver.find_element(By.XPATH, sheet2.cell_value(67,4)).click()
        self.driver.find_element(By.XPATH, sheet2.cell_value(68,4)).click()
        time.sleep(2)

        self.driver.find_elements_by_class_name("el-input__inner")[5].clear()
        self.driver.find_elements_by_class_name("el-input__inner")[5].send_keys(sheet2.cell_value(69,3))
        #删除第一个场景文件
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(70,2)).click()
        #添加场景文件
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(48,2)).click()
        time.sleep(1)
        #选择第二个场景文件
        self.driver.find_elements_by_class_name("list-item-title")[1].click()
        time.sleep(1)
        sceneName = self.driver.find_elements_by_class_name('courseware-name')[0].text
        print("更改后的课件标题=" +sceneName)
        #上传课件
        js = 'document.getElementsByClassName("el-icon-delete deleteIcon")[1].click()'
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(50,4)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(73,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)
        pptName = self.driver.find_elements_by_class_name('courseware-name')[0].text
        print("更改后的课件名称："+pptName)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(74,2)).click()
        time.sleep(1)
        lessonName = self.driver.find_elements_by_class_name('chapter-header-title__label')[1].text
        print("更改后的课时标题=" +lessonName)
        self.driver.find_element(By.XPATH, sheet2.cell_value(75,4)).click()
        time.sleep(2)
        #断言名称编辑成功
        a = self.driver.find_elements_by_class_name(sheet2.cell_value(79,1))[0].text
        b = sheet1.cell_value(32,2)
        self.assertEqual(a, b, '编辑失败，编辑课程名称失败')
    def test_005_coursePublish(self):
        '''课程草稿箱点击右下角的设置按钮发布'''
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div/div[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div[2]/div/div[2]/div/div").click()
        time.sleep(2)
        #点击右下角设置按钮
        self.driver.find_element(By.XPATH, sheet2.cell_value(56,4)).click()
        time.sleep(1)
        #点击发布按钮
        self.driver.find_element(By.XPATH, sheet2.cell_value(76,4)).click()
        time.sleep(2)
        #断言发布的课程后不在我的课程草稿页
        a = self.driver.find_elements_by_class_name(sheet2.cell_value(79,1))[0].text
        b = sheet1.cell_value(33,2)
        self.assertNotEqual(a, b, '发布失败，我的在线课程页的第一个课程名称不对')

        #断言我的在线课程有新发布的课程
        # self.driver.find_element(By.XPATH, sheet2.cell_value(77,4)).click()
        # time.sleep(1)
        # a = self.driver.find_elements_by_class_name(sheet2.cell_value(80,1))[0].text
        # b = sheet1.cell_value(34,2)
        # self.assertEqual(a, b, '发布失败，我的在线课程页的第一个课程名称不对')

        #断言审核状态有新发布的课程
        self.driver.find_element(By.XPATH, sheet2.cell_value(78,4)).click()
        #点击待审核
        self.driver.find_element(By.XPATH, sheet2.cell_value(83,4)).click()

        time.sleep(1)
        a = self.driver.find_elements_by_class_name("cell")[7].text
        b = sheet1.cell_value(35,2)
        self.assertEqual(a, b, '发布失败，审核状态页第一个课程的名称不对')

    def test_006_EditCourseAndPublish(self):
        '''课程编辑页发布课程'''
        global courseIcon,CreatCourse,chaptersName,chaptersIntroduce,sceneName,pptName,lessonName
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div/div[2]").click()
        time.sleep(1)
        self.driver.find_element(By.XPATH, "//div[@id='app']/div/div[2]/div[2]/div/div[2]/div/div").click()
        #点击右下角课程按钮
        time.sleep(3)
        self.driver.find_element(By.XPATH, sheet2.cell_value(56,4)).click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(14,2)).click()
        #编辑课程的名称
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(39,2)).clear()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(39,2)).send_keys(sheet2.cell_value(87,3))
        time.sleep(1)
        #编辑课程的icon
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(61,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(90,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        # WebDriverWait(self.driver, 20, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,".el-icon-delete")))

        time.sleep(4)
        #删除第一张课程介绍图

        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)

        #编辑课程的介绍图
        js = 'document.getElementsByClassName("el-icon-plus")[0].click()'
        self.driver.execute_script(js)
        time.sleep(0.5)
        # self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(37,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(91,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(4)

        # WebDriverWait(self.driver, 20, 0.5).until(EC.element_to_be_clickable((By.CSS_SELECTOR,sheet2.cell_value(63,2))))
        #编辑课程简介
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(63,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(63,2)).send_keys(sheet2.cell_value(88,3))

        time.sleep(1)
        #记录课程图标
        courseIcon2 = self.driver.find_element_by_xpath("//form/div[2]/div/div/img").get_attribute("src")
        print(courseIcon2)
        #记录课程介绍图
        courseImg2 = self.driver.find_element_by_class_name("el-upload-list__item-thumbnail").get_attribute("src")
        print(courseImg2)
        time.sleep(1)
        self.driver.find_element(By.XPATH, sheet2.cell_value(41,4)).click()
        #编辑更新章节1的名称
        time.sleep(1)
        self.driver.find_element(By.XPATH, sheet2.cell_value(64,4)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(43,2)).send_keys(sheet2.cell_value(65,3))
        time.sleep(1)
        chaptersName2 = self.driver.find_elements_by_class_name('chapter-header-title__label')[0].text
        print("更改后的章节标题=" +chaptersName2)
        #编辑更新章节1的介绍
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(44,2)).send_keys(sheet2.cell_value(66,3))        
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(45,2)).click()
        time.sleep(1)
        chaptersIntroduce2 = self.driver.find_elements_by_class_name('chapter-header-title__desc')[0].text
        print("更改后的章节介绍=" +chaptersIntroduce2)
        #编辑更新章节1的课时1的名称
        self.driver.find_element(By.XPATH, sheet2.cell_value(67,4)).click()
        self.driver.find_element(By.XPATH, sheet2.cell_value(68,4)).click()
        time.sleep(2)

        self.driver.find_elements_by_class_name("el-input__inner")[5].clear()
        self.driver.find_elements_by_class_name("el-input__inner")[5].send_keys(sheet2.cell_value(69,3))
        #删除第一个场景文件
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(70,2)).click()
        #添加场景文件
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(48,2)).click()
        #选择第二个场景文件
        self.driver.find_elements_by_class_name("list-item-title")[1].click()
        time.sleep(1)
        sceneName2 = self.driver.find_elements_by_class_name('courseware-name')[0].text
        print("更改后的课件标题=" +sceneName2)
        #上传课件
        js = 'document.getElementsByClassName("el-icon-delete deleteIcon")[1].click()'
        self.driver.execute_script(js)
        time.sleep(2)
        self.driver.find_element(By.XPATH, sheet2.cell_value(50,4)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(73,2))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(5)
        pptName2 = self.driver.find_elements_by_class_name('courseware-name')[0].text
        print("更改后的课件名" +pptName2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(74,2)).click()
        time.sleep(1)
        lessonName2 = self.driver.find_elements_by_class_name('chapter-header-title__label')[1].text
        print("更改后的课时标题=" +lessonName2)




if __name__ == '__main__':
    unittest.main()







