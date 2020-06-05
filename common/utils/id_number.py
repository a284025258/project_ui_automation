"""
身份证生成
"""
import linecache
import os
import random
import time

from config import STATIC_DIR

id_code_file_path = os.path.join(STATIC_DIR, 'idcode.txt')

_count = None
# 校验码
weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
cheack_code = ['1', '0', 'X', '9', '8', '7', '6', '5', '4', '3', '2']  # 校验码映射


def generate_id():
    """
    :return: 身份证号码
    """
    global _count
    if _count is None:
        _count = len(open(id_code_file_path, encoding="utf8").readlines())
    # 6位地址码
    count = _count  # 获取行数
    id_location = linecache.getline(id_code_file_path, random.randint(1, count))[:6]  # 随机读取某行
    # 8位生日编码
    date_start = time.mktime((1971, 1, 1, 0, 0, 0, 0, 0, 0))
    date_end = time.mktime((2019, 8, 1, 0, 0, 0, 0, 0, 0))
    date_int = random.randint(date_start, date_end)
    id_date = time.strftime("%Y%m%d", time.localtime(date_int))
    # 3位顺序码，末尾奇数-男，偶数-女
    id_order = f"{random.randint(0, 999):03}"
    # 前17位相加
    id_former = id_location + id_date + id_order

    total = 0
    for index, num in enumerate(id_former):
        total += int(num) * weight[index]
    id_check = cheack_code[total % 11]
    return id_former + id_check


if __name__ == '__main__':
    for i in range(1000):
        print(generate_id())
