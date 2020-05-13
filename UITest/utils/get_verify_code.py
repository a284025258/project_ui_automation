"""
https://blog.csdn.net/qq_38161040/article/details/90668765
https://blog.csdn.net/weixin_43697214/article/details/103007015
https://blog.csdn.net/u014630987/article/details/76713814

"""
import cv2
from pytesseract import pytesseract


def get_verify_code(img_path):
    content = pytesseract.image_to_string(__process_image(img_path),
                                          config="--psm 6 --oem 3 -c tessedit_char_whitelist=0123456789")  # 解析图片
    return content


def __process_image(img_path, out_path=None):
    """
    图像处理
    @param img_path: 图片地址
    @param out_path: 处理后的图片位置
    @return:
    """
    if out_path is None:
        out_path = img_path + "result.jpg"
    img = cv2.imread(img_path)
    # 将图片灰度化处理,降维,加权进行灰度化c
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    _, gray2 = cv2.threshold(gray, 200, 255, cv2.THRESH_BINARY)
    result = __remove_noise(gray2)
    cv2.imwrite(out_path, result)
    return result


def __remove_noise(img, k=4):
    """降噪"""
    img2 = img.copy()
    #   img处理数据，k过滤条件
    w, h = img2.shape

    def get_neighbors(img3, r, c):
        count = 0
        for i in [r - 1, r, r + 1]:
            for j in [c - 1, c, c + 1]:
                if img3[i, j] > 10:  # 纯白色
                    count += 1
        return count

    #   两层for循环判断所有的点
    for x in range(w):
        for y in range(h):
            if x == 0 or y == 0 or x == w - 1 or y == h - 1:
                img2[x, y] = 255
            else:
                n = get_neighbors(img2, x, y)  # 获取邻居数量，纯白色的邻居
                if n > k:
                    img2[x, y] = 255
    return img2


if __name__ == '__main__':
    i_path = r"C:\Users\admin\Pictures\test.jpg"
    print(get_verify_code(i_path))
