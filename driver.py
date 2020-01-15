"""
selenium driver 再次封装模块
"""

import os
import time
from time import sleep
from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
from logfunc import print_log
from public_data import ProjectPath


def wrapper(func):
    """装饰器函数"""

    def inner(*args, **kwargs):
        self = args[0]
        if self.driver_log_switch:
            try:
                strFuncName = func.__name__
                self.log("Call %s%s" % (strFuncName, args[1:]))
            except:
                pass
        try:
            return func(*args, **kwargs)
        except:
            self.print_screen()

    return inner


class Broswer():
    """ 浏览器类 , 对 selenium 驱动再次封装"""

    def __init__(self, log_func=print_log, driver_log_switch=True):
        """
       log_func: 日志处理函数
       driver_log_switch：debug日志开关,如果不想看到driver日志,可以屏蔽掉(改为False)
       """
        self.log = log_func
        self.driver_log_switch = driver_log_switch
        self.driver = None

        # 获取当前项目目录
        current_path = ProjectPath.project_path
        # 获取当前时间
        current_time = time.strftime("%Y-%m-%d_%H-%M-%S", time.localtime())
        # 保存截图的路径
        self.dir4save = os.path.join(current_path, 'pictures')
        self.pic_name = '%s.png' % current_time
        # 判断是否已存在文件夹
        if not os.path.exists(self.dir4save):
            os.makedirs(self.dir4save)

        self.pic_path = os.path.join(self.dir4save, self.pic_name)

    @wrapper
    def print_screen(self, name=''):
        """
        截图,保存当前浏览器界面
        :param name: 自定义照片名称
        :return: None
        """
        # 默认照片名称
        pic_path = self.pic_path
        # 自定义照片名称
        if name:
            name += '.png'
            pic_path = os.path.join(self.dir4save, name)
        self.driver.save_screenshot(pic_path)

    @wrapper
    def open(self, url, browser_type='chrome'):
        """
        用浏览器打开指定URL
        :param url: 网址
        :param browser_type: 浏览器种类(需要提前安装驱动)
        :return:None
        """
        if browser_type == 'chrome':
            self.driver = webdriver.Chrome()
        elif browser_type == 'firefox':
            self.driver = webdriver.Firefox()
        elif browser_type == 'ie':
            self.driver = webdriver.Ie()
        else:
            self.log('未安装此(:%s)浏览器驱动,将使用默认driver' % browser_type)
            self.driver = webdriver.Chrome()

        self.driver.get(url)
        self.driver.maximize_window()
        self.wait(3)

    @wrapper
    def quit(self):
        """Quits the driver and closes every associated window."""
        self.driver.quit()

    @wrapper
    def close(self):
        """ Closes the current window."""
        self.driver.close()

    @wrapper
    def clear(self, operand, by='xpath'):
        """
        清除输入框内容
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).clear()

    @wrapper
    def input(self, operand, value, by='xpath'):
        """
        向输入框输入内容
        :param operand:操作对象
        :param value:
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).send_keys(value)

    @wrapper
    def click(self, operand, by='xpath'):
        """
        点击
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        self.driver.find_element(by, operand).click()

    @wrapper
    def mousedown(self, operand, by='xpath'):
        """
        按下鼠标左键不放,Holds down the left mouse button on an element.
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:
        """
        ActionChains(self.driver).click_and_hold(self.driver.find_element(by, operand)).perform()

    @wrapper
    def wait(self, seconds):
        """
        等待
        :param seconds:等待时间(秒)
        :return:None
        """
        sleep(int(seconds))

    @wrapper
    def waitAppear(self, operand, timeout=60, by='xpath'):
        """
        等待控件出现
        :param operand:操作对象
        :param timeout:超时时间
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        timeout = int(timeout)
        while timeout > 0:
            if self.isElementPresent(operand, by):
                return True
            timeout -= 1
            self.wait(1)
        return False

    @wrapper
    def waitDisappear(self, operand, timeout=60, by='xpath'):
        """
        等待控件消失
        :param operand:操作对象
        :param timeout:超时时间
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        timeout = int(timeout)
        while timeout > 0:
            if not self.isElementPresent(operand, by):
                return True
            timeout -= 1
            self.wait(1)
        return False

    @wrapper
    def isElementPresent(self, operand, by='xpath'):
        """
        判断控件是否存在
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:True/False
        """
        try:
            self.driver.find_element(by, operand)
            return True
        except:
            return False

    @wrapper
    def getElementCount(self, operand, by='xpath'):
        """
        统计控件个数
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:控件个数
        """
        count = len(self.driver.find_elements(by, operand))
        return count

    @wrapper
    def getAttribute(self, operand, attribute, by='xpath'):
        """
        获取控件属性
        :param operand:操作对象
        :param attribute:属性名称
        :param by:查找控件的方式,默认xpath
        :return:控件属性
        """
        return self.driver.find_element(by, operand).get_attribute(attribute)

    @wrapper
    def getValue(self, operand, by='xpath'):
        """
        获取控件的value
        :param operand:操作对象
        :param by:查找控件的方式,默认xpath
        :return:字段value的值
        """
        return self.getAttribute(operand, 'value', by)

    @wrapper
    def refresh(self):
        """刷新"""
        self.driver.refresh()

    @wrapper
    def switch_to_window(self, Index=-1):
        """
        切换操作浏览器窗口
        :param Index: # 0表示跳回原窗口,负数的绝对值越小离原窗口越近,正数越小离原窗口越远
        :return:None
        """
        # 获得当前浏览器所有窗口
        windows = self.driver.window_handles
        self.driver.switch_to.window(windows[Index])

    @wrapper
    def switch_to_frame(self):
        """Switch focus to the default frame."""
        self.driver.switch_to.default_content()
        self.driver.switch_to.frame(self.driver.find_element('xpath', '/html/body/iframe'))

    @wrapper
    def click_hold(self, operand, by='xpath'):
        """用于拖动(如淘宝等)验证滑块"""
        action = ActionChains(self.driver)
        attrible = self.driver.find_element(by, operand)
        action.click_and_hold(attrible)
        action.move_by_offset(308, 44)
        action.release().perform()

    @wrapper
    def change_attribute_value(self, operand, types, value, by='xpath'):
        """
        改变元素属性
        :param operand:操作对象
        :param types:属性类型
        :param value:值
        :param by:查找控件的方式,默认xpath
        :return:None
        """
        ele1 = self.driver.find_element(by, operand)
        self.driver.execute_script("arguments[0].%s='%s'" % (types, value), ele1)


browser = Broswer()
