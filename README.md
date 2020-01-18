
# Mount_disk
批量挂载华为云ECS同名磁盘.



### Background

**起因:**

![起因](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/origin.png)

然后给我发了一封邮件介绍了操作流程,如下:

- **先打开网页:[华为云控制台登录](https://auth.huaweicloud.com/ )**
- **选择IAM登录,输入用户信息登录**

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/select_iam.png)

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/login.png)

- **1.切换到广州区,点击弹性云服务器ECS**

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/select_GZ_enter_ECS.png)

- **2.选择云服务ID,输入ecs id**

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/select_input_ecsid.png)

- **3.点击ecs name**

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/click_ecs_name.png)

- **4.查看ecs 信息:**

    如下图1:显示"未挂载云硬盘",就点击"挂载"按钮,接着执行下一步;

    如下图2:显示云硬盘信息,就返回,跳到步骤2.

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/ecs_detail.png)
![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/return_input_ecsid.png)

- **5.点击"挂载磁盘",在弹窗中的"云服务器名称"复制,然后粘贴到下面的输入框中,接着点击搜索:**

    未查询到云硬盘,点击取消,跳到步骤2;

    查询到1个云硬盘,勾选后,点击确定;
    
    查询到多个云硬盘,勾选任意一个,点击确定.

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/mount_disk.png)


- **6.第5步执行完后,如果出现弹窗,点击确定,接着执行步骤2.**

![](https://github.com/qqpzp1995/Mount_disk/blob/master/pic4md/init_tips.png)



**最开始写的版本由于未用到多进程,效率太低,执行完200多个磁盘挂载任务,需要5000多秒.
经过几次代码迭代优化,逐步新增了如下功能：**
- 日志记录
- 错误截图
- 异常处理
- 多任务

**此版本极大提高了效率(可选进程数量,在特定前提下,进程越多效率越高),功能也更加更加友好**

****

 *欢迎各位留言,提出问题,指出不足之处*
