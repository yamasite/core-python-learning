# coding utf-8
# Python 3.5.1

from tkinter import Tk, Text, TOP, BOTH, X, N, LEFT
from tkinter.ttk import Frame, Label, Entry, Button
from tkinter import *
from bs4 import BeautifulSoup
from selenium import webdriver
import urllib.request
from colorama import Fore
import subprocess


class Example(Frame):

    def __init__(self):
        super().__init__()

        self.initUI()


    def initUI(self):

        self.master.title("Info Code Link Checker for Confluence Page")
        self.pack(fill=BOTH, expand=True)

        usernametxt=StringVar()
        passwordtxt=StringVar()
        URLtxt=StringVar()

        def check():
            username=usernametxt.get()
            password=passwordtxt.get()
            URL=URLtxt.get()
            def site_login(URL, username, password):
                driver.get(URL)
                driver.find_element_by_id("os_username").send_keys(username)
                driver.find_element_by_id("os_password").send_keys(password)
                driver.find_element_by_id("loginButton").click()

            # Need to use selenium because it is a dynamic web page
            driver = webdriver.Chrome()
            site_login(URL, username, password)
            driver.get(URL)
            # page_source is a variable created by Selenium
            html_code = driver.page_source

            # Extract all external links from the Confluence web page using BeautifulSoup
            soup = BeautifulSoup(html_code, 'html.parser')
            all_link = soup.find_all('a', class_='external-link', href=True)

            # Get href attributes
            all_href = []
            for link in all_link:
                href = link['href']
                all_href.append(href)

            # Get info codes
            info_codes = []
            for link in all_link:
                info_code = link.text
                info_codes.append(info_code)

            # retrieve all links from the HTML source code
            # str1 = "\n".join(str(x) for x in all_href)

            # print to file
            # with open("URLListOutput.txt","wb") as text_file:
            #     text_file.write(str1.encode("utf-8"))

            # Check if the links are broken
            def check_link(address):
                try:
                    req = urllib.request.Request(url=address)
                    resp = urllib.request.urlopen(req)
                    if resp.status in [400, 404, 403, 408, 409, 501, 502, 503]:
                        print(Fore.RED + resp.status + "-" + resp.reason + "-->" + address)
                    else:
                        print(Fore.GREEN + "no problem in-->" + address)

                except Exception as e:
                    print(Fore.YELLOW + "{}-{}".format(e, address))
                    pass

            # Check all external links on the page
            for href in all_href:
                check_link(href)

            # Get info code links and check if all info codes are directed to the correct location
            # Old info code links have this format: http://digital.ni.com/express.nsf/bycode/[code]
            # New info code links have this format: http://www.ni.com/r/[code]
            info_code_links = []
            for info_code in info_codes:
                info_code_link = 'http://www.ni.com/r/' + info_code
                info_code_links.append(info_code_link)

            # Check new info code links
            for info_code_link in info_code_links:
                check_link(info_code_link)


        frame1 = Frame(self)
        frame1.pack(fill=X)

        lbl1 = Label(frame1, text="Username", width=10)
        lbl1.pack(side=LEFT, padx=10, pady=10)

        entry1 = Entry(frame1, textvariable=usernametxt)
        entry1.pack(fill=X, padx=10, expand=True)

        frame2 = Frame(self)
        frame2.pack(fill=X)

        lbl2 = Label(frame2, text="Password", width=10)
        lbl2.pack(side=LEFT, padx=10, pady=10)

        entry2 = Entry(frame2, show="*", textvariable=passwordtxt)
        entry2.pack(fill=X, padx=10, expand=True)

        frame3 = Frame(self)
        frame3.pack(fill=X)

        lbl3 = Label(frame3, text="URL", width=10)
        lbl3.pack(side=LEFT, padx=10, pady=10)

        entry3 = Entry(frame3, textvariable=URLtxt)
        entry3.pack(fill=X, padx=10, expand=True)

        frame4 = Frame(self)
        frame4.pack()

        button1 = Button(frame4, text="Check", command=check)
        button1.pack(side=LEFT)

        button2 = Button(frame4, text="QUIT", command=quit)
        button2.pack(side=LEFT)

        frame5 =Frame(self)
        frame5.pack()

        lbl4 = Label(frame5, text="Link Check Result", width=30)
        lbl4.pack(side=LEFT, padx=30, pady=30)

        frame6 = Frame(self)
        frame6.pack()

        textbox = Text(frame6, borderwidth=3, relief="sunken")
        textbox.config(state=DISABLED, font=("consolas",12), wrap="word")
        textbox.grid(row=0, column=1, sticky='nsew')
        textbox.pack()

        scrollb = Scrollbar(textbox, command=textbox.yview)
        scrollb.grid(row=0, column=1, sticky='nsew')
        textbox['yscrollcommand'] = scrollb.set

def main():

    root = Tk()
    root.geometry("600x600+600+600")
    app = Example()
    root.mainloop()

if __name__ == '__main__':
    main()
