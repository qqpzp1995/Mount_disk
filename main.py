"""
 *Title: The Script To Mounting Disk Of Ecs(Multiprocess Version).
 *Created in: 2020-01
 *Author: Gu Wanli
"""
import time
import multiprocessing
from functools import partial
from driver import browser
from logfunc import print_log, print_warning
from public_data import console_url, pending_list, Area, UserInfo
from public import search_ecs_id, login, select_area, kill_chrome, net_error_condition

# 成功的list
ok_list = list()
# 失败的list
faild_list = list()
# 重试的list
retry_list = list()
# 网络原因导致失败的list
net_error_list = list()
# ECS故障 的list
faulty_list = list()
# 存放执行完成,也无法找到此ecs的list
inexistent_list = list()
# retry list for Beijing
retry_list_beijing = list()


def main(ecs_id, pwd, area=Area.Guangzhou):
    try:
        # 用于判断浏览器是否已启动
        if not browser.isElementPresent('//*[@id="cfDefaultLogo"]'):
            browser.open(console_url)
            # 1.登录
            login(UserInfo.account, UserInfo.iam_name, pwd)
            # 2.选择区域
            select_area(area)
        # 用于返回到输入ecs_id 的地方
        if browser.isElementPresent('//*[@id="mianbao"]/div[1]/div[1]'):
            browser.wait(1)
            browser.click('//*[@id="mianbao"]/div[1]/div[1]')
        # 查询,然后执行挂载
        return search_ecs_id(ecs_id)
    except:
        # 处理异常(刷新界面,以免影响后续操作)
        browser.refresh()
        return net_error_condition(ecs_id)


if __name__ == '__main__':
    pwd = input('请输入密码 :\n')
    cpu_count = multiprocessing.cpu_count()
    while True:
        child_process_num = int(input('请输入子进程数量(处于2-%s之间的正整数):\n' % cpu_count))
        if not 2 <= child_process_num < cpu_count:
            print_warning('您输入的多任务数为%s,不符合要求,请重新输入!' % child_process_num)
        else:
            break
    print_log('即将启动,多任务:%s' % child_process_num)
    # 开始时间
    start_time = time.time()
    # 记录一下本次操作list的长度
    length = len(pending_list)
    # 创建进程池
    pool = multiprocessing.Pool(child_process_num)
    # 用于存放子进程
    jobs = list()

    # 广州区操作
    for it in pending_list:
        # 将函数的返回值给p
        p = pool.apply_async(main, args=(it, pwd))
        # 存放函数返回值
        jobs.append(p)
    pool.close()
    pool.join()
    for job in jobs:
        print_log(job.get())
        ecs_id, flag = job.get()
        if flag == 1:
            ok_list.append(ecs_id)
        # 重试的list
        elif flag == 0:
            retry_list.append(ecs_id)
        # 失败的list
        elif flag == 2:
            faild_list.append(ecs_id)
        # 非id原因,执行失败
        elif flag == 3:
            net_error_list.append(ecs_id)
        # 故障的机器
        elif flag == 4:
            faulty_list.append(ecs_id)
    # 关闭浏览器
    kill_chrome()

    # 上海区操作
    # 用偏函数传值
    partial_func = partial(main, pwd=pwd, area=Area.Shanghai)
    with multiprocessing.Pool(child_process_num) as p:
        # 获取执行结果
        res = p.map(partial_func, retry_list)
    for ecs_id, flag in res:
        if flag == 1:
            ok_list.append(ecs_id)
        elif flag == 0:
            retry_list_beijing.append(ecs_id)
        elif flag == 2:
            faild_list.append(ecs_id)
        elif flag == 3:
            net_error_list.append(ecs_id)
        elif flag == 4:
            faulty_list.append(ecs_id)
    kill_chrome()

    # 北京区操作
    # 用偏函数传值
    partial_func_beijing = partial(main, pwd=pwd, area=Area.Beijing)
    with multiprocessing.Pool(child_process_num) as p:
        # 获取执行结果
        res_beijing = p.map(partial_func_beijing, retry_list_beijing)
    for ecs_id, flag in res_beijing:
        if flag == 1:
            ok_list.append(ecs_id)
        elif flag == 0:
            inexistent_list.append(ecs_id)
        elif flag == 2:
            faild_list.append(ecs_id)
        elif flag == 3:
            net_error_list.append(ecs_id)
        elif flag == 4:
            faulty_list.append(ecs_id)
    kill_chrome()

    # 结束时间
    end_time = time.time()

    print_log('\n***************操作完成,情况如下: ***************\n'
              '共%s个ecs id,耗时:%.2fs\n'
              '多任务:%s\n'
              '操作成功的(%s个):%s\n'
              '不在服务区的(%s个):%s\n'
              '操作失败的(%s个):%s\n'
              '网络问题的(%s个):%s\n'
              '故障的ECS(%s个):%s\n'
              '************************************************' %
              (length, (end_time - start_time), child_process_num, len(ok_list), ok_list, len(inexistent_list),
               inexistent_list, len(faild_list), faild_list, len(net_error_list), net_error_list, len(faulty_list),
               faulty_list))
