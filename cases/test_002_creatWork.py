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
        print("官网创建作品保存为草稿")
        global modleFileNmae,workIcon,workImg

        self.driver.get("https://staging.www.qiaojianyun.com/#/login")
        self.driver.set_window_size(1800, 1000)
        self.driver.set_window_rect(100,100)
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


        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.set_window_size(1829, 967)
        self.driver.set_window_rect(0,0)
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR,".creat-button").click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).send_keys(sheet2.cell_value(4,3))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(5,2)).click()
        # js = 'document.getElementsByClassName("avatar-uploader-icon")[0].click()'
        # self.driver.execute_script(js)

        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(5,3))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(6,3))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(7,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(8,2)).send_keys(sheet2.cell_value(28,4))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(9,2)).click()
        time.sleep(2)
        element = WebDriverWait(self.driver, 20).until(EC.element_to_be_clickable((By.CSS_SELECTOR, sheet2.cell_value(10,2)))).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(11,2)).click()
        self.driver.execute_script("window.scrollTo(0,32)")
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(1,2)
        self.assertEqual(a, b, '创建失败，创建的作品不在草稿箱中')
        

    def test_002_copyWork(self):
        '''官网复制作品'''
        # self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        # self.driver.set_window_size(1829, 967)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(16,2)).click()
        #复制的第二个是为了EditAndpublish
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(16,2)).click()

        time.sleep(1)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[1].text
        b = sheet1.cell_value(4,2)
        self.assertEqual(a, b, '复制失败')


    def test_003_deleteWork(self):
        '''官网删除作品'''
        self.driver.refresh()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(13,2)).click()
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(2,2)
        self.assertNotEqual(a, b, '删除失败，删除的作品还在草稿箱中')
    def test_004_EditWorkAndSave(self):
        '''官网编辑作品并保存'''
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(14,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).clear()
        #编辑作品的名称
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).send_keys(sheet2.cell_value(15,3))
        time.sleep(1)

        #编辑作品的icon
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(61,2)).click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(5,5))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        #删除第一张作品介绍图
        js = 'document.getElementsByClassName("el-icon-delete")[0].click()'
        self.driver.execute_script(js)

        #编辑添加课程的介绍图
        self.driver.find_element(By.XPATH, "//div/i").click()
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(6,5))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(2)

        #编辑添加课程的场景文件
        self.driver.find_element(By.XPATH, sheet2.cell_value(48,4)).click()

        moudleFileName = self.driver.find_elements_by_class_name("list-item-title")[1].text
        self.driver.find_elements_by_class_name("list-item-title")[1].click()

        #记录课程图标
        workIcon = self.driver.find_element_by_xpath("//form/div[2]/div/div/img").get_attribute("src")
        print(workIcon)
        #记录课程介绍图
        workImg = self.driver.find_element_by_class_name("el-upload-list__item-thumbnail").get_attribute("src")
        print(workImg)
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(11,2)).click()
        time.sleep(2)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        time.sleep(1)
        b = sheet1.cell_value(3,2)
        self.assertEqual(a, b, '编辑失败，编辑的作品名称失败')
        
        



    def test_005_publishWork(self):
        '''官网草稿页发布作品'''
        # self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        # self.driver.set_window_size(1829, 967)
        self.driver.refresh()
        time.sleep(2)
        # self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(17,2)).click()
        time.sleep(1)
        # 发布作品后草稿消失
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet2.cell_value(6,2)
        self.assertNotEqual(a, b, '发布失败，作品还在草稿箱')
        # 我的在线作品页存在发布的作品
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(20,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(5,2)
        self.assertEqual(a, b, '发布失败，我的在线作品页看不到发布的作品')
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(21,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('cell')[8].text #查看class的文本
        b = sheet1.cell_value(7,2)
        self.assertEqual(a, b, '发布失败，作品状态不为未审核')
        time.sleep(0.5)
        a = self.driver.find_elements_by_class_name('el-table_1_column_3')[1].text
        b = sheet1.cell_value(8,2)
        self.assertEqual(a, b, '发布失败，作品状态不为未审核')
        self.driver.get("https://staging.www.qiaojianyun.com/#/community")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(4,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(13,2)).click()
        a = self.driver.find_elements_by_class_name('word')[0].text
        b = sheet1.cell_value(9,2)
        self.assertEqual(a, b, '发布失败，社区平台没有看到这个作品')

    def test_006_EditAndPublish(self):
        '''官网编辑页发布作品'''
        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.refresh()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(19,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(12,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(14,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).clear()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).click()
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).send_keys(sheet2.cell_value(27,3))
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(26,2)).click()
        # 我的在线作品页存在发布的作品
        self.driver.refresh()
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(20,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(10,2)
        self.assertEqual(a, b, '发布失败，我的在线作品页看不到发布的作品')
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(21,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('cell')[8].text #查看class的审核状态
        b = sheet1.cell_value(12,2)
        self.assertEqual(a, b, '发布失败，发布后的作品状态不为未审核')
        time.sleep(0.5)
        a = self.driver.find_elements_by_class_name('el-table_1_column_3')[1].text#查看class的文本
        b = sheet1.cell_value(11,2)
        self.assertEqual(a, b, '发布失败，审核状态页的作品名不对')
        self.driver.get("https://staging.www.qiaojianyun.com/#/community")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(4,2)).click()
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(13,2)).click()
        a = self.driver.find_elements_by_class_name('word')[0].text
        b = sheet1.cell_value(13,2)
        self.assertEqual(a, b, '发布失败，社区平台没有看到这个作品')
    def test_007_creatWorkAndPublish(self):
        '''官网创建作品并发布'''

        self.driver.get("https://staging.www.qiaojianyun.com/#/workBench")
        self.driver.set_window_size(1829, 967)

        self.driver.find_element(By.CSS_SELECTOR,".creat-button").click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).click()

        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(3,2)).send_keys(sheet2.cell_value(28,3))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR,sheet2.cell_value(5,2)).click()
        # js = 'document.getElementsByClassName("avatar-uploader-icon")[0].click()'
        # self.driver.execute_script(js)

        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(5,4))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(6,2)).click()
        time.sleep(2)
        autoit.control_set_text("文件上传","[Class:Edit; instance:1]",sheet2.cell_value(6,4))
        autoit.control_click("文件上传","[Class:Button; instance:1]")
        time.sleep(3)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(7,2)).click()
        time.sleep(2)
        #输入作品简介
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(8,2)).send_keys(sheet2.cell_value(28,4))
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(9,2)).click()
        time.sleep(2)
        self.driver.find_elements_by_class_name("list-item-title")[0].click()
        js = 'document.getElementsByClassName("el-button")[2].click()'
        self.driver.execute_script(js)
        time.sleep(2)
        # 我的在线作品页存在发布的作品
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(20,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('ellipsis_box')[0].text
        b = sheet1.cell_value(14,2)
        self.assertEqual(a, b, '发布失败，我的在线作品页看不到发布的作品')
        time.sleep(1)
        self.driver.find_element(By.CSS_SELECTOR, sheet2.cell_value(21,2)).click()
        time.sleep(1)
        a = self.driver.find_elements_by_class_name('cell')[8].text #查看class的审核状态
        b = sheet1.cell_value(16,2)
        self.assertEqual(a, b, '发布失败，作品状态不为"未审核"')
        time.sleep(0.5)
        a = self.driver.find_elements_by_class_name('cell')[7].text #查看class的文本
        b = sheet1.cell_value(15,2)
        self.assertEqual(a, b, '发布失败，审核状态页的作品名不对')
        self.driver.get("https://staging.www.qiaojianyun.com/#/community")
        time.sleep(2)
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(4,2)).click()
        self.driver.find_element(By.CSS_SELECTOR, sheet3.cell_value(13,2)).click()
        a = self.driver.find_elements_by_class_name('word')[0].text
        b = sheet1.cell_value(17,2)
        self.assertEqual(a, b, '发布失败，社区平台没有看到这个作品')



# if __name__ == '__main__':
#     unittest.main()


