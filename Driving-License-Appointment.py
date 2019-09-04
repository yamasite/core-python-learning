# coding utf-8
# Python 3.5.1

from bs4 import BeautifulSoup
from selenium import webdriver
from PIL import Image
import pytesseract
import cv2

# Get validation code


def site_login(URL, username, password):
    driver.get(URL)

    driver.implicitly_wait(10)
    driver.maximize_window()

    driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtPupilNo").send_keys(username)
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtWebPwd").send_keys(password)

    def binarization(img):
        """传入image对象进行灰度、二值处理"""
        img = img.convert("L")  # 转灰度
        pixdata = img.load()
        w, h = img.size
        # 遍历所有像素，大于阈值的为黑色
        for y in range(h):
            for x in range(w):
                if pixdata[x, y] < 100:
                    pixdata[x, y] = 0
                else:
                    pixdata[x, y] = 255
        return img


    def noise_remove_cv2(image_name, k):
        """
        8邻域降噪
        Args:
            image_name: 图片文件命名
            k: 判断阈值

        Returns:

        """

        def calculate_noise_count(img_obj, w, h):
            """
            计算邻域非白色的个数
            Args:
                img_obj: img obj
                w: width
                h: height
            Returns:
                count (int)
            """
            count = 0
            width, height = img_obj.shape
            for _w_ in [w - 1, w, w + 1]:
                for _h_ in [h - 1, h, h + 1]:
                    if _w_ > width - 1:
                        continue
                    if _h_ > height - 1:
                        continue
                    if _w_ == w and _h_ == h:
                        continue
                    if img_obj[_w_, _h_] < 230:  # 二值化的图片设置为255
                        count += 1
            return count

        img = cv2.imread(image_name, 1)
        # 灰度
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        w, h = gray_img.shape
        for _w in range(w):
            for _h in range(h):
                if _w == 0 or _h == 0:
                    gray_img[_w, _h] = 255
                    continue
                # 计算邻域pixel值小于255的个数
                pixel = gray_img[_w, _h]
                if pixel == 255:
                    continue

                if calculate_noise_count(gray_img, _w, _h) < k:
                    gray_img[_w, _h] = 255

        return gray_img


    # Use selenium web driver

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
    # 图片的DPI不能过低，否则会导致无法识别
    ran.crop(rangle).save("D:\\temp\\PythonPhoto\\captcha2.png", dpi=(3000.0, 3000.0))

    print("获取验证码图片，读取验证码")
    # 4、获取验证码图片，读取验证码
    imageCode = Image.open("D:\\temp\\PythonPhoto\\captcha2.png")
    image = noise_remove_cv2("D:\\temp\\PythonPhoto\\captcha2.png", 4)
    print(pytesseract.image_to_string(Image.fromarray(image)).strip())
    code = pytesseract.image_to_string(Image.fromarray(image)).strip()
    print("收到验证码，进行输入验证")
    # 5、收到验证码，进行输入验证
    print(code.lower())

    driver.find_element_by_id("ctl00_ContentPlaceHolder1_txtCode").send_keys(code.lower())
    driver.find_element_by_id("ctl00_ContentPlaceHolder1_ibtnLogin").click()

    driver.implicitly_wait(10)

    driver.get('http://117.74.136.118:8802/PupilWeb/logging/BookingCarStudy.aspx')
    html_code = driver.page_source
    soup = BeautifulSoup(html_code, 'html.parser')

    print(soup)
    # Need to use selenium because it is a dynamic web page. We use Firefox here.

    file = open('info.html', 'w', encoding='utf-8')
    file.write(str(soup))
    file.close

driver = webdriver.Firefox()

site_login("http://117.74.136.118:8090/PupilWeb/logging/LoginUserDefault.aspx", "", "")




