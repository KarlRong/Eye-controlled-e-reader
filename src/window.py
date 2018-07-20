#!/usr/bin/env python
# -*- coding: utf-8 -*-

import os
import sys
import shutil

from PyQt5.QtCore import Qt
from PyQt5.QtCore import pyqtSignal as SIGNAL
from PyQt5.QtCore import pyqtSlot as SLOT
from PyQt5.QtWidgets import (QMainWindow, QDockWidget, QAction, QApplication,
                         QMessageBox, QFileDialog)

from src.library import LibraryTableWidget, insert_library
from src.bookview import BookView
from src.books import Book
from src.GazeThread import GazeThread

parentdir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
sys.path.insert(0, parentdir)

from constants import LIBRARY_DIR


class MainWindow(QMainWindow):

    def __init__(self):
        super(MainWindow, self).__init__()

        self.gazeThread = GazeThread()

        self.create_layout()
        self.create_actions()
        self.create_menus()
        self.create_connections()
        self.showMaximized()

    def create_layout(self):
        self.book = BookView(self)
        self.setCentralWidget(self.book)

        self.create_library_dock()

    def create_library_dock(self):
        if getattr(self, 'dock', None):
            self.dock.show()
            return

        self.dock = QDockWidget("Library", self)
        self.dock.setAllowedAreas(Qt.LeftDockWidgetArea|Qt.RightDockWidgetArea)
        self.library = LibraryTableWidget(self.book)
        self.dock.setWidget(self.library)
        self.addDockWidget(Qt.LeftDockWidgetArea, self.dock)

    def create_menus(self):
        file_menu = self.menuBar().addMenu("&File")
        help_menu = self.menuBar().addMenu("&Help")

        file_menu.addAction(self.library_action)
        file_menu.addAction(self.open_action)
        file_menu.addSeparator()
        file_menu.addAction(self.quit_action)

        help_menu.addAction(self.help_action)
        help_menu.addAction(self.about_action)

    def create_actions(self):
        self.library_action = QAction("&Library", self)
        self.open_action = QAction("&Open", self)
        self.quit_action = QAction("&Quit", self)

        self.help_action = QAction("Help", self)
        self.about_action = QAction("&About", self)


    def create_connections(self):
        self.library_action.triggered.connect(self.create_library_dock)
        self.open_action.triggered.connect(self.open_book)
        self.quit_action.triggered.connect(self.close())
        self.connect(self.about_action, SIGNAL("triggered()"), self.about)
        self.connect(self.help_action, SIGNAL("triggered()"), self.help)
        self.gazeThread.signal_timeStamp.connect(self.receive_gaze)
        self.gazeThread.start()

    def about(self):
        QMessageBox.about(self, "QtBooks", "An ebook reader")


    def help(self):
        QMessageBox.information(self, 'Help', 'Nothing yet!')

    def open_book(self):
        book_path = QFileDialog.getOpenFileName(self, u'打开Epub格式电子书', ".", "(*.epub)")

        print(u"in open_book, book_name is:" + str(book_path))
        print(u"in open_book, bookdata path:" + str(LIBRARY_DIR))
        print(os.path.dirname(str(book_path)))

        if os.path.dirname(str(book_path))+os.sep != str(LIBRARY_DIR):
            shutil.copy(str(book_path), LIBRARY_DIR)

        file_name = os.path.basename(str(book_path))
        book_id = file_name.split('.epub')[0]
        book = Book(book_id)
        insert_library(book)
        self.library.refresh()

    def receive_gaze(self, text, bScroll):
        print("receive: " + str(bScroll))
        currentValue = self.book.webFrame.scrollBarValue(2)
        if bScroll:
            self.book.webFrame.setScrollBarValue(2, currentValue + 850)
        else:
            self.book.webFrame.setScrollBarValue(2, currentValue - 850)


