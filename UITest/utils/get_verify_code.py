import pytesseract

from PIL import Image


# 二值化处理
def two_value(img):
    # 打开文件夹中的图片
    image = Image.open(img)
    # 灰度图
    lim = image.convert('L')
    # 灰度阈值设为165，低于这个值的点全部填白色
    threshold = 120
    table = []

    for j in range(256):
        if j < threshold:
            table.append(0)
        else:
            table.append(1)

    bim = lim.point(table, '1')

    bim = depoint(bim)
    bim = depoint(bim)
    bim = depoint(bim)
    bim = depoint(bim)
    bim = depoint(bim)
    bim = depoint(bim)

    bim.save(img + "tt.jpg")


def depoint(img):
    """传入二值化后的图片进行降噪"""

    pixdata = img.load()

    w, h = img.size

    for y in range(1, h - 1):

        for x in range(1, w - 1):
            count = 0

            if pixdata[x, y - 1] > 245:  # 上

                count = count + 1

            if pixdata[x, y + 1] > 245:  # 下

                count = count + 1

            if pixdata[x - 1, y] > 245:  # 左

                count = count + 1

            if pixdata[x + 1, y] > 245:  # 右

                count = count + 1

            if pixdata[x - 1, y - 1] > 245:  # 左上

                count = count + 1

            if pixdata[x - 1, y + 1] > 245:  # 左下

                count = count + 1

            if pixdata[x + 1, y - 1] > 245:  # 右上

                count = count + 1

            if pixdata[x + 1, y + 1] > 245:  # 右下

                count = count + 1

            if count > 1:
                pixdata[x, y] = 255

    return img


def hh(im):
    # 图像二值化
    w, h = im.size
    for x in range(1, w - 1):
        for y in range(1, h - 1):
            if x < 2 or y < 2:
                im.putpixel((x - 1, y - 1), 255)
            if x > w - 3 or y > h - 3:
                im.putpixel((x + 1, y + 1), 255)
    im.save(img + "tt.jpg")


def get_verify_code(page_path):
    image = Image.open(page_path)
    content = pytesseract.image_to_string(image)  # 解析图片
    return content


if __name__ == '__main__':
    img = r"C:\Users\admin\Pictures\test.jpg"
    two_value(img)
    print(get_verify_code(img))
