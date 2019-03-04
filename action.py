# -*- coding:utf-8 -*-
# __author__ = 'Shanks'
from PyQt5.QtCore import QFile, QIODevice, QDir
from PyQt5.QtGui import QIcon
from PyQt5.QtWidgets import QAction
from dialogbox import NewFileDialog, NewDirDialog


class Action:

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

    @staticmethod
    def new_file(filetree):
        file_dialog = NewFileDialog()
        fname = None
        if file_dialog.exec_():
            fname = file_dialog.file_name()
        if not fname:
            return
        new_node = filetree.new_text_node(fname)
        Action.add_node(filetree, new_node)
        # add file to system
        file_path = filetree.node_path(new_node)
        file = QFile(file_path)
        file.open(QIODevice.ReadWrite)
        file.close()

    @staticmethod
    def new_dir(filetree):
        dir_dialog = NewDirDialog()
        dname = None
        if dir_dialog.exec_():
            dname = dir_dialog.dir_name()

        if not dname:
            return
        new_node = filetree.new_dir_node(dname)
        Action.add_node(filetree, new_node)
        # add dir to system
        dir_path = filetree.node_path(new_node)
        QDir.mkpath(dir_path)

    @staticmethod
    def add_node(filetree, newnode):
        current_node = filetree.currentItem()
        if current_node is None:
            filetree.topLevelItem(filetree.index_top_item).addChild(newnode)
        else:
            if filetree.node_type(newnode) == filetree.DIR:
                current_node.addChild(newnode)
            else:
                current_node.parent().addChild(newnode)




            
            
            
            
            
            
            
            
            
        
        
        

