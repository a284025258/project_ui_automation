import os

from config import DRIVER_CHROME, STATIC_DIR

# Start_Url = "https://125.70.9.114:41111/"
Start_Url = "http://125.70.9.114:30080/"
Driver_Path = DRIVER_CHROME

UploadImg = os.path.join(STATIC_DIR, "img/testUpload.jpg")
WEB_ROLE_CONF = {
    "S": ("S51", "Sceea@123"),  # 省级账号
    "D": ("D5101", "Sceea@123"),  # 市级账号
    "X": ("X511702", "Sceea@123"),  # 区县级账号
    "Z": ("Z511702002", "Sceea@123"),  # 考点级账号
    "G": ("G510112101", "Sceea@123"),  # 大学级账号
}
