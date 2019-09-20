# encoding utf-8
# using Python 3.5.1
# Crawls all doc pages and check if all links are valid

import urllib.request
from lxml import etree
from pathlib import Path
import os
import requests


class GetURLsFromSitemap(object):


    def __init__(self, url):
        self.url = url


    def get_url_list(self, url):

        file_name = "outputlinks.txt"

        # Gets the sitemap file per the URL
        def get_sitemap(url):

            try:
                response = urllib.request.urlopen(url, data=None)
                xml_code = response.read()
                # print(type(xml_code))
                # Take URLs with the following format: <xhtml:link rel="alternate" hreflang="en" href="https://www.milvus.io/docs/en/aboutmilvus/overview"/>
                xml_root = etree.HTML(xml_code)
                # print(etree.tostring(xml_root))
            except urllib.request.URLError as e:
                xml_root = etree.HTML("")
                print(e)

            return xml_root

        xml_root = get_sitemap(url)
        # Find all links in href attributes
        link_elements = xml_root.findall(".//link[@href]")
        links = []
        for link_element in link_elements:
            # print(type(link_element))
            link_href = link_element.get("href")
            # print(type(link_href))
            links.append(link_href)

        # Find all links in <loc> tags
        link_elements_loc = xml_root.findall(".//loc")
        for link_element_loc in link_elements_loc:
            link_loc = etree.tostring(link_element_loc, method="text")
            # Remove b' prefixes by changing byte literals to strings
            links.append(link_loc.decode('utf-8'))

        #print(links)

        # Writes the URL list to a text file
        text_file = Path(file_name)
        if text_file.is_file():
            os.remove(file_name)

        with open(file_name,'a') as f:
            for link in links:
             f.write(link + "\n")

        return file_name



class CheckLinkStatus(object):

    def __init__(self, file_name):
        self.file_name = file_name

    def check_link_status(self, file_name):

        report_name="link_report.txt"

        with open(file_name,'r') as f:
            links = f.readlines()

        text_file = Path(report_name)
        if text_file.is_file():
            os.remove(report_name)

        for link in links:
            try:
                print(link)
                print(type(link))
                r = requests.head(link)
                status_code = r.status_code

                """
                Informational responses (100–199),
                Successful responses (200–299),
                Redirects (300–399),
                Client errors (400–499),
                and Server errors (500–599).
                """

                with open(report_name,'a') as f:
                    if status_code in range(100-199):
                        f.write("Status code: " + str(status_code) + " " + str(link) + " has no errors." + "\n")
                    if status_code in range(200,299):
                        f.write("Status code: " + str(status_code) + " " + str(link) + " has no errors." + "\n")
                    elif status_code in range(300,399):
                        f.write("Status code: " + str(status_code) + " " + str(link) + " has a redirect." + "\n")
                    elif status_code in range(400,599):
                        f.write("Status code: " + str(status_code) + " " + str(link) + " has errors." + "\n")


            except requests.ConnectionError:
                print("Failed to connect.")


SitemapURLMilvus = GetURLsFromSitemap("https://milvus.io/sitemap.xml")
SitemapURLMilvus.get_url_list("https://milvus.io/sitemap.xml")
CheckLinkStatusMilvus = CheckLinkStatus("outputlinks.txt")
CheckLinkStatusMilvus.check_link_status("outputlinks.txt")


