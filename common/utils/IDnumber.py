"""
身份证生成
todo 选择地区
"""
import os
import time
import random

from config import STATIC_DIR


def __get_districtcodes():
    districtcodes = []
    with open(os.path.join(STATIC_DIR,'idcode.txt'), mode='r', encoding='utf-8') as f:
        for l in f.readlines():
            districtcodes.append(l.strip()[:6])
    return districtcodes


def generate_ID(gender=None):
    """
    :param gender: 控制性别，None为随机, 1:男，0：女
    :return: 身份证号码
    """

    # 6位地址码
    codelist = __get_districtcodes()
    id_location = codelist[random.randint(0, len(codelist) - 1)]  # randint为闭区间，注意-1

    # 8位生日编码
    date_start = time.mktime((1971, 1, 1, 0, 0, 0, 0, 0, 0))
    date_end = time.mktime((2019, 8, 1, 0, 0, 0, 0, 0, 0))

    date_int = random.randint(date_start, date_end)
    id_date = time.strftime("%Y%m%d", time.localtime(date_int))

    # 3位顺序码，末尾奇数-男，偶数-女
    id_order = 0
    if not gender:
        id_order = random.randint(0, 999)
    elif gender == 1:
        id_order = random.randint(0, 499) * 2 + 1
    elif gender == 0:
        id_order = random.randint(0, 499) * 2

    if id_order >= 100:
        id_order = str(id_order)
    elif id_order >= 10:
        id_order = "0" + str(id_order)
    else:
        id_order = "00" + str(id_order)

    # 前17位相加
    ID_former = id_location + id_date + id_order

    # 验证码
    weight = [7, 9, 10, 5, 8, 4, 2, 1, 6, 3, 7, 9, 10, 5, 8, 4, 2]  # 权重项
    cheack_code = {
        '0': '1',
        '1': '0',
        '2': 'X',
        '3': '9',
        '4': '8',
        '5': '7',
        '6': '6',
        '7': '5',
        '8': '5',
        '9': '3',
        '10': '2'}  # 校验码映射

    sum = 0
    for i, num in enumerate(ID_former):
        sum += int(num) * weight[i]
    ID_check = cheack_code[str(sum % 11)]

    ID = ID_former + ID_check
    return ID


if __name__ == '__main__':
    for i in range(10):
        print(generate_ID(gender=1))
