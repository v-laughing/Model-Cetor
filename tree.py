# -*- coding:utf-8 -*-
# __author__ = 'Shanks'

# this file introduce file tree, which is shown in QTreeWidget of EditorWindow
import sys
from PyQt5.QtGui import QImageReader, QIcon, QKeySequence
from PyQt5.QtWidgets import *
from PyQt5.QtCore import *
from action import Action

class FileTreeWidget(QTreeWidget):
    NODE_NAME = 0
    FILE_PATH = 1
    NODE_TYPE = 2
    DIR = 'dir'
    IMAGE = 'image'
    TEXT = 'text.c'

    def __init__(self, file_path, parent=None):
        super(FileTreeWidget, self).__init__(parent)
        self.file_path = file_path
        self.setHeaderItem(self.headerItem())
        self.addTopLevelItem(self.init_tree_root(file_path))

        self.index_top_item = self.topLevelItemCount() - 1
        # action


    def headerItem(self):
        header = QTreeWidgetItem()
        header.setText(self.NODE_NAME, 'Project')
        header.setIcon(self.NODE_NAME, QIcon('images/tree/project.png'))
        return header

    def init_tree_root(self, file_path):
        if not file_path:
            return
        root_node = self.init_tree_node(file_path)
        # put off current dir and parent dir
        list_info = QDir(file_path).entryInfoList()[2:]

        if list_info:
            for info in list_info:
                if info.isFile():
                    root_node.addChild(self.init_tree_node(info.absoluteFilePath()))
                if info.isDir():
                    root_node.addChild(self.init_tree_root(info.absoluteFilePath()))
        return root_node

    def init_tree_node(self, file_path):
        file_info = QFileInfo(file_path)

        if file_info.isDir():
            tree_item = self.new_dir_node(file_info.fileName())
        else:
            file_type = file_info.suffix()
            image_types = ['%s' % str(format, 'utf-8')
                          for format in QImageReader.supportedImageFormats()]
            if file_type in image_types:
                tree_item = self.new_image_node(file_info.fileName())
            else:
                tree_item = self.new_text_node(file_info.fileName())
                
        return tree_item

    def new_text_node(self, file_name):
        text_node = QTreeWidgetItem()
        fname = file_name
        if '.' not in file_name:
            fname = file_name + '.txt'
        text_node.setText(self.NODE_NAME, fname)
        text_node.setText(self.NODE_TYPE, self.TEXT)
        text_node.setIcon(self.NODE_NAME, QIcon('images/tree/text.c.png'))
        return text_node
    
    def new_image_node(self, file_name):
        image_node = QTreeWidgetItem()
        image_node.setText(self.NODE_NAME, file_name)
        image_node.setText(self.NODE_TYPE, self.IMAGE)
        image_node.setIcon(self.NODE_NAME, QIcon('images/tree/image.png'))
        return image_node

    def new_dir_node(self, file_name):
        dir_node = QTreeWidgetItem()
        dir_node.setText(self.NODE_NAME, file_name)
        dir_node.setText(self.NODE_TYPE, self.DIR)
        dir_node.setIcon(self.NODE_NAME, QIcon('images/tree/dir.png'))
        return dir_node

    def node_path(self, tree_item):

        path = tree_item.text(self.NODE_NAME)
        if tree_item == self.topLevelItem(self.index_top_item):
            return self.file_path
        parent = tree_item.parent()
        path = self.node_path(parent) + '\\' + path
        return path

    def node_type(self, treenode):
        return treenode.text(self.NODE_TYPE)
































