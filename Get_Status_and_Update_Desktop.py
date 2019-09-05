# coding=utf-8

from bs4 import BeautifulSoup
import urllib.request
from PIL import Image, ImageDraw, ImageFont
from ctypes import windll, WinError
import os
import struct

def get_html_text(url):
    response = urllib.request.urlopen(url, data=None)
    # print(response)
    html_code = response.read()


    def check_pass_fail(tr):
        passed = "Passed"
        status = ""
        if passed not in tr:
            status = "The LVHelpBuild_CHStringExport succeeded today."
        else:
            status = "The LVHelpBuild_CHStringExport failed today"
        img = Image.new('RGB', (3000, 2000), color=(73, 109, 137))
        fnt = ImageFont.truetype('C://Windows//Fonts//Arial.ttf', 80)
        d = ImageDraw.Draw(img)
        d.text((500, 1000), status, font=fnt, fill=(255, 255, 0))
        img.save('pil_text.bmp')
        abs_path = os.path.abspath('pil_text.bmp')

        SPI_SETDESKWALLPAPER = 20
        r = windll.user32.SystemParametersInfoW(SPI_SETDESKWALLPAPER, 0, abs_path, 0)
        print(r)
        if not r:
            raise WinError()

    soup = BeautifulSoup(html_code, 'html.parser')
    td_string = soup.find(string="LVHelpBuild_CHStringExport")
    # print(td_string)
    table = td_string.find_parent("table")
    # print(table)
    result_table = table.find_next_sibling("table")
    # print(result_table)
    # print(result_table.children)
    table_trs = result_table.children
    table_trs_new = []
    for tr in table_trs:
        table_trs_new.append(tr)
    # print(table_trs_new)
    first_tr = table_trs_new[3]
    # print("----------------------------------------------------")
    # print(first_tr)
    check_pass_fail(first_tr)


get_html_text("URL")

