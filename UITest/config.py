import os

from config import DRIVER_CHROME, STATIC_DIR, Have_Window, WEB_ROLE_CONF

# Start_Url = "https://125.70.9.114:41111/"
Start_Url = "https://125.70.9.114:31443/"
Driver_Path = DRIVER_CHROME
HandLess = not Have_Window
UploadImg = os.path.join(STATIC_DIR, "img", "testUpload.jpg")

