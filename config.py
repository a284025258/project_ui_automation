import os

# 项目路径
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
# 静态文件路径
STATIC_DIR = os.path.join(BASE_DIR, 'static')
# 放置driver的路径
DRIVER_DIR = os.path.join(STATIC_DIR, 'driver')
# 放置错误截图的路径
IMG_DIR = os.path.join(STATIC_DIR, 'img')
# ChromeDriver的对路径
DRIVER_CHROME = os.path.join(DRIVER_DIR, 'chromedriver.exe')

if not os.path.exists(DRIVER_DIR):
    os.mkdir(DRIVER_DIR)
if not os.path.exists(IMG_DIR):
    os.mkdir(IMG_DIR)

# DATABASES = {
#     'NAME': 'apitest',
#     'USER': 'root',
#     'PASSWORD': '',
#     'HOST': '127.0.0.1',
#     'PORT': '3306',
#     'ENCODING': 'utf8',
#     'OPTIONS': {
#         "init_command": "SET default_storage_engine='INNODB'"
#     }
# }
