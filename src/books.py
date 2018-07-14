#!/usr/bin/env python
# -*- coding: UTF-8 -*-

import os
import zipfile
import sys

from lxml import etree
from bs4 import BeautifulSoup

# from bs4.BeautifulSoup import BeautifulStoneSoup
parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from constants import LIBRARY_DIR

# LIBRARY_DIR = os.path.abspath('.') + os.sep

RECOVER_PARSER = etree.XMLParser(recover=True, no_network=True)
NAMESPACES = {
    'dc': 'http://purl.org/dc/elements/1.1/',
}


class Book(object):
    u"""
    需要主动调用open方法才能获得相应的属性
    """
    _FILE = LIBRARY_DIR + '%s.epub'

    def __init__(self, book_id=None):
        if book_id:
            self.open(book_id)

    def fromstring(self, raw, parser=RECOVER_PARSER):
        return etree.fromstring(raw, parser=parser)

    def read_doc_props(self, raw):
        u"""

        :param raw: raw string of xml
        :return:
        """
        root = self.fromstring(raw)
        self.title = root.xpath('//dc:title', namespaces={'dc': NAMESPACES['dc']})[0].text
        self.author = root.xpath('//dc:creator', namespaces={'dc': NAMESPACES['dc']})[0].text

    def open(self, book_id=None):
        if book_id:
            self.book_id = book_id
        if not self.book_id:
            raise Exception('Book id not set')

        self.f = zipfile.ZipFile(self._FILE % self.book_id, 'r')
        print(self._FILE)
        soup = BeautifulSoup(self.f.read('META-INF/container.xml'), 'lxml')
        oebps = soup.findAll('rootfile')[0]['full-path']
        folder = oebps.rfind('/')
        self.oebps_folder = '' if folder == -1 else oebps[:folder + 1]  # 找到oebps的文件夹名称
        oebps_content = self.f.read(oebps)
        self.read_doc_props(oebps_content)
        opf_bs = BeautifulSoup(oebps_content, 'lxml')
        ncx = opf_bs.findAll('item', {'id': 'ncx'})[0]
        ncx = self.oebps_folder + ncx['href']  # 找到ncx的完整路径
        ncx_bs = BeautifulSoup(self.f.read(ncx), "lxml")

        self.chapters = [(nav.navlabel.text, nav.content['src']) for
                         nav in ncx_bs.findAll('navmap')[0].findAll('navpoint')]

    def get_chapter(self, num):
        return self.f.read(self.oebps_folder + self.chapters[num][1])


if __name__ == '__main__':
    book = Book('莎士比亚全集')
    print(book.oebps_folder)

    print(book.title)
    print(book.author)

    print(str(book.chapters).decode("unicode-escape").encode("utf-8"))
