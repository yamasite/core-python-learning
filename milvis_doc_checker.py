# encoding utf-8
# using Python 3.5.1
# Crawls all doc pages and check if all links are valid

import urllib.request
from lxml import etree
from pathlib import Path
import os


class GetURLsFromSitemap(object):


    def __init__(self, url):
        self.url = url


    def get_url_list(url):

        file_name = "outputlinks.txt"

        def get_sitemap(url):
            try:
                response = urllib.request.urlopen(url, data=None)
            except urllib.request.URLError as e:
                print(e)
            xml_code = response.read()
            # print(type(xml_code))
            # Take URLs with the following format: <xhtml:link rel="alternate" hreflang="en" href="https://www.milvus.io/docs/en/aboutmilvus/overview"/>
            xml_root = etree.HTML(xml_code)
            # print(etree.tostring(xml_root))
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


GetURLsFromSitemap.get_url_list("https://milvus.io/sitemap.xml")
