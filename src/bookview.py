#!/usr/bin/env python
# -*- coding: utf-8 -*-

from PyQt5.QtWidgets import *
from PyQt5.QtWebEngineWidgets import QWebEnginePage, QWebEngineView
from PyQt5 import QtCore
from src.books import Book


class BookView(QSplitter):
    def __init__(self, parent=None):
        super(BookView, self).__init__(parent=parent)
        self.create_layout()
        self.create_connections()

    def create_layout(self):
        self.web_view = QWebEngineView()
        self.chapter_list = QListWidget()
        self.next_button = QPushButton("Next chapter")
        self.previous_button = QPushButton("Previous chapter")

        hbox = QHBoxLayout()
        hbox.addStretch()
        hbox.addWidget(self.previous_button)
        hbox.addWidget(self.next_button)

        vbox = QVBoxLayout()
        vbox.addWidget(QLabel("Chapters"))
        vbox.addWidget(self.chapter_list)
        vbox.addLayout(hbox)

        widget = QWidget()
        widget.setLayout(vbox)
        self.web_view.setUrl(QtCore.QUrl("http://"))
        self.webPage = self.web_view.page()

        self.addWidget(self.web_view)
        self.addWidget(widget)

    def create_connections(self):
        chlist = self.chapter_list
        self.next_button.clicked.connect(lambda:
                                         chlist.setCurrentRow(0
                                                              if chlist.currentRow() == chlist.count() - 1
                                                              else chlist.currentRow() + 1))
        self.previous_button.clicked.connect(lambda:
                                             chlist.setCurrentRow(chlist.count() - 1
                                                                  if chlist.currentRow() == 0
                                                                  else chlist.currentRow() - 1))
        self.chapter_list.currentRowChanged[int].connect(self.set_chapter)

    def set_chapter(self, num=None):
        if num is None:
            num = self.chapter_list.currentRow()
        if num < 0:
            num = len(self.book.chapters) - 1
        elif num >= len(self.book.chapters):
            num = 0
        self.web_view.setHtml(self.book.get_chapter(num).decode(encoding="utf-8"))
        self.webPage = self.web_view.page()
        self.webPage.setZoomFactor(2)

    def load_book(self, book_id):
        self.book = Book(book_id)
        self.chapter_list.clear()
        for chapter in self.book.chapters:
            self.chapter_list.addItem(chapter[0])
        self.chapter_list.setCurrentRow(0)
