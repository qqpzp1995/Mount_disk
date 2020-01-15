"""
公共逻辑
"""
import os
import time
from functools import wraps
from driver import browser
from logfunc import print_log, print_warning
from public_data import Area

# 打印函数名称
func_name = True

def log_level_select(func_name=func_name):
    """打印函数名称,便于定位"""
    def decorator(func):
        def wrapper(*args, **kw):
            if func_name:
                print_log('call %s() ...' % func.__name__)
                return func(*args, **kw)
        return wrapper
    return decorator


@log_level_select(func_name)
def login(account, iam_name, pwd):
    """
    登录逻辑
    :param account:用户名
    :param iam_name: IAM 用户名
    :param pwd: 密码
    :return: None
    """
    # 等待登录按钮加载完成
    browser.waitAppear('//*[@id="btn_submit"]')
    # 点击'IAM用户登录'
    browser.click('//*[@id="subUserLogin"]')
    # 等待用户登录信息栏加载完成
    browser.waitAppear('//*[@id="IAMAccountInputId"]/input')
    browser.waitAppear('//*[@id="IAMUsernameInputId"]/input')
    browser.waitAppear('//*[@id="IAMPasswordInputId"]/input')
    browser.wait(1)
    # 输入账号,用户名,密码
    browser.input('//*[@id="IAMAccountInputId"]/input', account)
    browser.input('//*[@id="IAMUsernameInputId"]/input', iam_name)
    browser.input('//*[@id="IAMPasswordInputId"]/input', pwd)
    browser.wait(1)
    # 点击登录
    browser.click('//*[@id="btn_submit"]')
    # 等待并点击'下次再说'
    browser.waitAppear('//*[@id="model.nextBind"]/div/span', timeout=5)
    for i in range(3):
        if browser.isElementPresent('//*[@id="model.nextBind"]/div/span'):
            browser.click('//*[@id="model.nextBind"]/div/span')
        else:
            browser.wait(1)


@log_level_select(func_name)
def select_area(area=Area.Guangzhou):
    """
    选择区域逻辑
    :param area:区域,默认广州
    :return:None
    """
    # 等待并点击'弹性云服务器 ECS'
    browser.waitAppear('//*[@id="myResources"]//div[text()="弹性云服务器 ECS"]')
    browser.click('//*[@id="myResources"]//div[text()="弹性云服务器 ECS"]')
    # 点击后等待区域出现
    browser.waitAppear('//*[@id="menu"]/div[1]/div[4]/cf-region/div/a[1]')
    browser.wait(1)
    # 点击区域单选框
    browser.click('//*[@id="menu"]/div[1]/div[4]/cf-region/div/a[1]')
    browser.wait(1)
    # 选择区域
    browser.click('//*[@id="menu"]/div[1]/div[4]//span[text()="%s"]' % area)
    # 等待界面加载完成
    browser.wait(3)
    # 如果出现'跳过'弹窗,就点击跳过
    if browser.isElementPresent('//span[text()="跳过"]'):
        browser.click('//span[text()="跳过"]')


@log_level_select(func_name)
def recording_time(func):
    """计算函数执行时间修饰器"""

    @wraps(func)
    def inner(*args, **kwargs):
        start_time = time.time()
        func(*args, **kwargs)
        end_time = time.time()
        print_log('%s 执行时间是:%0.2f' % (func.__name__, (end_time - start_time)))

    return inner


@log_level_select(func_name)
def kill_chrome():
    """强制关闭浏览器"""
    print_log(os.popen('taskkill /im chrome.exe /f').read())
    print_log(os.popen('taskkill /im chromedriver.exe /f').read())


@log_level_select(func_name)
def retry_condition(ecs_id):
    """重试标记逻辑"""
    current_area = browser.getAttribute('//*[@id="menu"]/div[1]/div[4]/cf-region/div/a[1]/span[2]', 'textContent')
    if current_area in Area.Beijing:
        print_log('无法在管理区域查询到当前ECS(id:%s),请注意!' % ecs_id)
    else:
        print_log('当前ECS(id:%s) 不在本区域内,稍后将在其他区域重试...' % ecs_id)
    return ecs_id, 0


@log_level_select(func_name)
def ok_condition(ecs_id):
    """成功标记逻辑"""
    print_log('当前ECS(id:%s) 磁盘挂载操作成功~' % ecs_id)
    return ecs_id, 1


@log_level_select(func_name)
def failed_condition(ecs_id):
    """失败标记逻辑"""
    print_warning('当前ECS(id:%s) 磁盘挂载操作失败!' % ecs_id)
    browser.print_screen(ecs_id)
    # 点击取消按钮
    browser.click('//*[@id="ecsAttachDivMsg"]//span[text()="取消"]')
    return ecs_id, 2


@log_level_select(func_name)
def net_error_condition(ecs_id):
    """网络延迟问题处理逻辑"""
    # 处理方法:截图
    print_warning('由于网络问题,当前ECS(id:%s) 磁盘挂载操作中断,请注意!' % ecs_id)
    browser.print_screen(ecs_id)
    return ecs_id, 3


@log_level_select(func_name)
def faulty_condition(ecs_id):
    """故障状态标记逻辑"""
    print_warning('当前ECS(id:%s) 处于异常状态!' % ecs_id)
    browser.print_screen(ecs_id)
    return ecs_id, 4


@log_level_select(func_name)
def search_ecs_id(ecs_id):
    """
    查询ecs,并执行挂载操作
    :param ecs_id: ecs的id
    :return: ecs_id 和 状态标记(0,1,2,3,4分别表示:重试,成功,失败,网络延迟导致失败,ECS故障)
    """
    # return的值由 ecs_id 和 标识flag组成,flag的值为0/1/2:
    # 0表示有不在广州区,1表示成功,2表示有多个或0个磁盘

    # 如果出现了'x',点击'x',清除输入的内容(2019年11月12日,新版本)
    if browser.isElementPresent('//*[@id="ecsListSearchbox_clearTag0"]'):
        browser.click('//*[@id="ecsListSearchbox_clearTag0"]')

    # 循环判断是否已选择 '云服务器ID:'
    for i in range(3):
        if browser.isElementPresent('//span[text()="云服务器ID:"]'):
            break
        else:
            # 点击'默认按照名称搜索',改为'云服务器ID:'
            browser.wait(3)
            browser.waitAppear('//*[@id="ecsListSearchbox_input"]')
            browser.click('//*[@id="ecsListSearchbox_input"]')
            browser.wait(1)
            # 点击'云服务器ID:'
            browser.click('//*[@id="ecsListSearchbox_prop_id"]')
    else:
        # 网络延迟问题处理
        return net_error_condition(ecs_id)

    # 输入ecs_id
    browser.input('//*[@id="ecsListSearchbox_input"]', ecs_id)
    # 点击搜索
    browser.click('//*[@id="ecsListSearchbox_search"]')
    # 搜索结果中显示的 ecsid 的xpath.
    ecs_xpath = '//div[@class="nowrap_hidden"]/span[text()="%s"]' % ecs_id
    browser.wait(3)
    # 先等待3s,如果出现ecs,则跳过等待,否则循环2次等待校验是否出现
    for i in range(2):
        if browser.isElementPresent(ecs_xpath):
            break
        else:
            browser.wait(3)
    else:
        # 重试状态标记
        return retry_condition(ecs_id)

    # 判断是否为故障状态
    if browser.isElementPresent('//td[@tip-content="故障"]'):
        # 故障状态处理/标记
        return faulty_condition(ecs_id)

    # 点击ecs的名称
    browser.click('//*[@id="vmList"]//span[text()="%s"]/../..//a[2]' % ecs_id)
    browser.wait(3)
    # 下拉滚动条,规避显示器尺寸问题
    # browser.send_space()

    # 判断是否出现'未挂载云硬盘'提示
    if browser.isElementPresent('//*[@id="detailRigthContent"]//span[text()="未挂载云硬盘"]'):
        # 点击挂载
        browser.click('//*[@id="detailRigthContent"]//span[text()="挂载"]')
        # 2019年12月19日版本,点击挂载后,在新界面点击'挂载磁盘'
        browser.waitAppear('//*[@id="ecs_detail_attach_disk_button"]/span/button/span')
        # 界面刚加载完成时,'挂载磁盘'按钮是置灰的,等待其变为可选
        browser.wait(2)
        browser.click('//*[@id="ecs_detail_attach_disk_button"]/span/button/span')
        # 获取云服务器名称
        browser.waitAppear('//*[@id="ecsAttachDiv"]//dl//div[@ng-bind="serverInfo.name"]')
        browser.wait(1)
        ecs_name = browser.getAttribute('//*[@id="ecsAttachDiv"]//dl//div[@ng-bind="serverInfo.name"]',
                                        'textContent')
        # 输入ECS名称
        browser.input('//*[@id="searchBox.id"]/div[2]/input', ecs_name)
        # 点击搜索
        browser.click('//*[@id="searchBox.id"]/div[2]/div[2]')
        browser.wait(3)

        # 获取云硬盘数量
        evs_count = int(
            browser.getElementCount('//*[@id="ecsAttachDiv"]//table/tbody//div[contains(text(),"%s")]' % ecs_name))

        # 分情况
        # 如果有1个或2个云硬盘,则选中第一个硬盘挂载
        if evs_count == 1 or evs_count == 2:
            # 点击第一个磁盘的复选框
            browser.click('//*[@id="ecsAttachDiv"]//table/tbody/tr[1]/td/label')
            browser.wait(1)
            # 点击最下面的确定
            browser.click('//*[@id="ecsAttachDivMsg"]/div[3]/div[1]/span/button/span')
            # 等待确定消失
            browser.waitDisappear('//*[@id="ecsAttachDivMsg"]/div[3]/div[1]/span/button/span')
            # 等待loading消失
            browser.waitDisappear('/html/body/div[19]')
            # 2019年12月新增'挂载流程尚未完成，还需初始化才能正常使用！'弹窗,点击确定
            confirm_btn_xpath = '//*[@id="ecs_detail_attach_disk_confirm_init_button"]/span/button/span[text()="确定"]'
            # 由于添加多进程操作,网络问题会导致按钮有时无法点击到,加循环,规避此类问题
            for i in range(3):
                if browser.isElementPresent(confirm_btn_xpath):
                    browser.wait(0.5)
                    browser.click(confirm_btn_xpath)
                else:
                    break
            else:
                browser.refresh()
            # 成功状态标记
            return ok_condition(ecs_id)

        # 否则点击取消按钮
        else:
            # 失败状态标记
            return failed_condition(ecs_id)
    else:
        # 成功状态标记
        return ok_condition(ecs_id)
