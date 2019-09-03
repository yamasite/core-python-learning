# coding utf-8
# Python 3.5.1

from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
from PIL import Image
import pytesseract

# Get validation code

# Use selenium web driver
def site_login(URL, username, password):
        driver.get(URL)

        driver.implicitly_wait(10)
        driver.maximize_window()

        driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPupilNo").send_keys(username)
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtWebPwd").send_keys(password)


        # Get the validation code img
        # 验证码输入框元素
        print("验证码输入框元素")
        imgelement = driver.find_element_by_id("ctl00_ContentPlaceHolder1_imgCode")

        location = imgelement.location  # 获取验证码x,y轴坐标
        size = imgelement.size  # 获取验证码的长宽
        rangle = (int(location['x']), int(location['y']), int(location['x'] + size['width']),
                  int(location['y'] + size['height']))  # 写成我们需要截取的位置坐标

        # 验证图片元素
        print("验证图片元素")
        imgElement = 'D:\\temp\\PythonPhoto\\captcha.png'

        # 2、截取屏幕内容，保存到本地
        print("截取屏幕内容，保存到本地")
        driver.save_screenshot("D:\\temp\\PythonPhoto\\captcha.png")

        # 3、打开截图，获取验证码位置，截取保存验证码
        print("打开截图，获取验证码位置，截取保存验证码")
        ran = Image.open("D:\\temp\\PythonPhoto\\captcha.png")
        print("获取验证码位置")

        ran.crop(rangle).save("D:\\temp\\PythonPhoto\\captcha2.png")

        print("获取验证码图片，读取验证码")
        # 4、获取验证码图片，读取验证码
        imageCode = Image.open("D:\\temp\\PythonPhoto\\captcha2.png")

        print(imageCode)
        code = pytesseract.image_to_string(imageCode).strip()
        print("收到验证码，进行输入验证")
        # 5、收到验证码，进行输入验证
        print(code.lower())

        driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtCode").send_keys(code)
        driver.find_element_by_id("ctl00_ContentPlaceHolder1_ibtnLogin").click()


# Need to use selenium because it is a dynamic web page. We use Firefox here.
driver = webdriver.Firefox()

site_login("http://117.74.136.118:8090/PupilWeb/logging/LoginUserDefault.aspx", "", "")




