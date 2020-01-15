"""
公共数据
"""
import os


class Area:
    """区域"""
    Guangzhou = "华南-广州"
    Shanghai = "华东-上海二"
    Beijing = "华北-北京一"


class UserInfo:
    """用户信息"""
    # 测试账号信息
    account = ''
    iam_name = ''


class ProjectPath:
    """项目目录"""
    project_path = os.path.abspath('.')


console_url = "https://auth.huaweicloud.com/"

# 特别选取了4个ecs id用于测试
# (正常情况每次需要执行200个左右的ecs id,单进程需要5000多秒,多进程能极大的提高效率)
pending_list = [
    '061e659b-2d6c-4de0-8fc0-2f191a7f1fb0',  # 操作成功
    '89ac20ee-6a8c-4bed-8928-a2bbf17c8891',  # 不在服务区
    '00ff309d-3b85-4ce3-8feb-1de954230132',  # 操作失败(无磁盘)
    '4bd45b27-6c42-49fa-aebe-4cee4c5dc45e'   # 故障
]
