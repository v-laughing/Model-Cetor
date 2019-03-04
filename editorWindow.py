# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

# this file is a editor window

from PyQt5.QtWidgets import*
from PyQt5.QtCore import *
from PyQt5.QtGui import *
import textedit
from tree import FileTreeWidget
from action import Action


class EditorWindow(QMainWindow):
    def __init__(self, dir_path, parent=None):
        super(EditorWindow, self).__init__(parent)
        self.setWindowTitle('IDE')
        self.resize(600, 600)

        self.edit_tab = QTabWidget()
        self.info_area = QTextEdit()
        self.info_area.setEnabled(False)
        self.file_tree = FileTreeWidget(dir_path)
        self.add_tree_node_action()
        self.main_layout()
        # add file and edit bar
        self.file_menu = self.menuBar().addMenu("&File")
        self.add_file_menu_action()
        self.edit_menu = self.menuBar().addMenu('&Edit')
        self.add_edit_menu_action()

        # status bar
        status = self.statusBar()
        status.setSizeGripEnabled(False)
        status.showMessage("Ready", 5000)

    def main_layout(self):
        # main edit area
        edit_frame = QFrame()
        edit_frame.setFrameStyle(QFrame.Plain)
        desk = QDesktopWidget()
        edit_layout = QVBoxLayout()
        edit_layout.addWidget(self.edit_tab)
        edit_layout.addWidget(desk)
        edit_frame.setLayout(edit_layout)
        # info display area
        edit_scroll = QScrollArea()
        edit_scroll.setWidget(self.info_area)

        edit_splitter = QSplitter(Qt.Vertical)
        edit_splitter.addWidget(edit_frame)
        edit_splitter.addWidget(edit_scroll)
        edit_splitter.setStretchFactor(0, 20)
        edit_splitter.setStretchFactor(1, 1)
        # file display area
        file_splitter = QSplitter(Qt.Horizontal)
        file_splitter.addWidget(self.file_tree)
        file_splitter.addWidget(edit_splitter)
        file_splitter.setStretchFactor(0, 1)
        file_splitter.setStretchFactor(1, 3)

        self.setCentralWidget(file_splitter)

    def create_action(self, text, slot=None, shortcut=None, icon=None,
                      tip=None, checkable=False, signal="triggered()"):
        action = QAction(text, self)
        if icon is not None:
            action.setIcon(QIcon("images/{}".format(icon)))
        if shortcut is not None:
            action.setShortcut(shortcut)
        if tip is not None:
            action.setToolTip(tip)
            action.setStatusTip(tip)
        if slot is not None and signal == 'triggered()':
            action.triggered.connect(slot)
        if slot is not None and signal == 'toggled(bool)':
            action.toggled[bool].connect(slot)
        if checkable:
            action.setCheckable(True)
        return action

    def add_file_menu_action(self):
        new_file = self.create_action("&New File", self.file_new, QKeySequence.New,
                                      "new.png", "Create a file")
        new_dir = self.create_action("New &Dir", self.file_new_dir, "Ctrl+F",
                                     'dir.png', "Create a file dir")
        new_pro = self.create_action("New &Pro", self.file_new_pro, "Ctrl+P",
                                     'pro.png', "Create a project")
        open = self.create_action("&Open...", self.file_open, QKeySequence.Open,
                                  "open.png", "Open an file")
        save = self.create_action("&Save", self.file_save, QKeySequence.Save,
                                  "save.png", "Save the file")
        save_all = self.create_action("Save A&ll", self.file_save_all, "Ctrl+L",
                                      "save.png", "Save all the files")
        close_tap = self.create_action("Close &Tab", self.file_close_tap, QKeySequence.Close,
                                       "close.png", "Close the active tab")
        quit = self.create_action("&Quit", self.quit, "Ctrl+Q",
                                  "quit.png", "Quit the application")

        new_menu = self.file_menu.addMenu('&New')
        new_menu.addActions((new_file, new_dir, new_pro))
        self.file_menu.addActions((open, save, save_all, close_tap))
        self.file_menu.addSeparator()
        self.file_menu.addAction(quit)

    def add_edit_menu_action(self):
        copy = self.create_action("&Copy", self.edit_copy, QKeySequence.Copy,
                                  "copy.png", "Copy text.c to the clipboard")
        cut = self.create_action("Cu&t", self.edit_cut, QKeySequence.Cut,
                                 "cut.png", "Cut text.c to the clipboard")
        paste = self.create_action("&Paste", self.edit_paste, QKeySequence.Paste,
                                   "paste", "Paste in the clipboard's text.c")
        self.edit_menu.addActions((copy, cut, paste))

    def add_tree_node_action(self):
        self.file_tree.itemClicked.connect(self.clicked)
        self.file_tree.itemDoubleClicked.connect(self.double_clicked)

    def clicked(self):
        node = self.file_tree.currentItem()

    def double_clicked(self):
        node = self.file_tree.currentItem()
        if self.file_tree.node_type(node) == self.file_tree.TEXT:
            file_path = self.file_tree.node_path(node)
            self.file_open(file_path)

    def file_new(self):
        Action.new_file(self.file_tree)

    def file_new_dir(self):
        Action.new_dir(self.file_tree)

    def file_new_pro(self):
        pass

    def file_open(self, filepath=''):
        if filepath is None:
            filepath = QFileDialog.getOpenFileName(self, 'Open File')[0]
        if filepath:
            for i in range(self.edit_tab.count()):
                text_edit = self.edit_tab.widget(i)
                if text_edit.file_path == filepath:
                    self.edit_tab.setCurrentWidget(text_edit)
                    return

            self.file_load(filepath)

    def file_load(self, file_path):
        text_edit = textedit.TextEdit(file_path)
        filename = text_edit.file_name
        try:
            text_edit.load()
        except EnvironmentError as e:
            QMessageBox.warning(self, "Load Error", "Failed to load {}: {}".format(filename, e))
            text_edit.close()
            del text_edit
        else:
            self.edit_tab.addTab(text_edit, filename)
            self.edit_tab.setCurrentWidget(text_edit)

    def file_save(self):       
        text_edit = self.edit_tab.currentWidget()
        if text_edit is None or not isinstance(text_edit, QTextEdit):
            return 
        try:
            text_edit.save()
            self.edit_tab.setTabText(self.edit_tab.currentIndex(), text_edit.file_name)
        except EnvironmentError as e:
            QMessageBox.warning(self, "Save Error!", "Failed to save {}: {}".format(text_edit.file_name, e))

    def file_save_all(self):
        pass

    def file_close_tap(self):
        text_edit = self.edit_tab.currentWidget()
        if text_edit is None or not isinstance(text_edit, QTextEdit):
            return
        text_edit.close()

    def quit(self):
        sured = QMessageBox.question(self, 'QUIT!', 'Are you sure quit?', QMessageBox.Yes | QMessageBox.No)
        if sured == QMessageBox.Yes:
            self.close()

    def edit_copy(self):
        text_edit = self.edit_tab.currentWidget()
        if text_edit is None or not isinstance(text_edit, QTextEdit):
            return
        cursor = text_edit.textCursor()
        text = cursor.selectedText()
        if text:
            clipboard = QApplication.clipboard()
            clipboard.setText(text)

    def edit_paste(self):
        text_edit = self.edit_tab.currentWidget()
        if text_edit is None or not isinstance(text_edit, QTextEdit):
            return
        clipboard = QApplication.clipboard()
        text_edit.insertPlainText(clipboard.text())

    def edit_cut(self):
        text_edit = self.edit_tab.currentWidget()
        if text_edit is None or not isinstance(text_edit, QTextEdit):
            return
        cursor = text_edit.textCursor()
        text = cursor.selectedText()
        if text:
            cursor.removeSelectedText()
            clipboard = QApplication.clipboard()
            clipboard.setText(text)






























































