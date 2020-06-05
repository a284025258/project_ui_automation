import re

m = dict(zip("0123456789", "零一二三四五六七八九"))
quantifier = ["", "十", "百", "千", ]
second_class_quantifier = ["万", "亿", "万亿", "兆"]


def _num_to_zh(num):
    num = str(num)
    long = len(num)
    measure_words = quantifier[:long][::-1]
    chars = list(map(lambda _: m[_], num))
    l = []
    for char_num, measure_word in zip(chars, measure_words):
        l.append(char_num)
        if char_num == "零":
            continue
        l.append(measure_word)

    res = "".join(l)
    res = re.sub(r"零+", "零", res)
    res = re.sub(r"一十", "十", res)

    return res.rstrip("零")


def num_split(num, num_list=None):
    num = str(num)
    if num_list is None:
        num_list = []
    if len(num) > 4:
        num_list.append(num[-4:])
        return num_split(num[:-4], num_list)
    else:
        num_list.append(num)
        return list(reversed(num_list))


def num_to_zh(num):
    nums = list(map(_num_to_zh, num_split(num)))
    scq = second_class_quantifier[::-1]
    while True:
        s = scq.pop().join([nums.pop(), nums.pop()][::-1])
        nums.append(s)
        if len(nums) == 1:
            break

    return "".join(nums)


if __name__ == '__main__':
    print(num_to_zh(1234005))
    print(num_to_zh(12560009))
    print(num_to_zh(10100101010100))
