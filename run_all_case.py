#!/usr/bin/python3
# -*- coding: utf-8 -*-
import time
from HTMLTestRunner import HTMLTestRunner
import unittest
# import paramiko
import os
import datetime

case_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'cases')
# case_dir = 'E:/zhuqueautomatiic/cases/'   # 定义用例所在路径
report_dir = os.path.join(os.path.dirname(os.path.realpath(__file__)),'report')
"""定义discover方法"""
discover = unittest.defaultTestLoader.discover(case_dir,
                                               pattern='test*.py',
                                               top_level_dir=None)
"""
1.case_dir即测试用例所在目录
2.pattern='test_*.py' ：表示用例文件名的匹配原则，“*”表示任意多个字符，这里表示匹配所有以test_开头的文件
3.top_level_dir=None：测试模块的顶层目录。如果没顶层目录（也就是说测试用例不是放在多级目录
中），默认为 None
"""

# def uploadFile2Server():
#     hostname = '47.92.93.77'
#     port = 22
#     password = 'aA82985272'
#     username = 'root'
#     remote_dir = '/www/admin/mdxck.xyz_80/wwwroot/report/'  # 服务器文件夹
    
#     local_dir = "E:/pyy/report/"  # 本地文件夹，测试
#     t = paramiko.Transport(hostname, port)
#     t.connect(username=username, password=password)
#     sftp = paramiko.SFTPClient.from_transport(t)
#     files = os.listdir(local_dir)
#     # 获取本地文件夹下所有文件，二级文件夹需定义递归函数
#     for file in files:
#         file_path = local_dir + os.sep + file  # 本地文件路径
#         remote_path = remote_dir + file  # 服务器文件路径
#         sftp.put(file_path, remote_path)
#         print('文件"{}"上传成功！\n'.format(file))
#     t.close()


if __name__ == "__main__":
    """直接加载discover"""
    now = time.strftime("%Y-%m-%d %H_%M_%S")
    filename = './report/' + now + '_result.html'
    fp = open(filename, 'wb')
    runner = HTMLTestRunner(stream=fp,
                            title='Test Report',
                            description='Implementation Example with: ')
    runner.run(discover)
    fp.close()
