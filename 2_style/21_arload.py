#******************************************************************************************************************************

#content       = Assignment 

#date          = November 7, 2024

#to do         = Update style

#author        = Elizabeth Guan <yijie.beth.guan@gmail.com>

#******************************************************************************************************************************

import os
import re
import sys
import shutil
import getpass
import datetime
import subprocess

from Qt import QtWidgets, QtGui, QtCore, QtCompat

import libLog
import libData
import libFunc
import arNotice
import arSaveAs

from tank import Tank
from arUtil import ArUtil

TITLE = "load"
LOG = libLog.init(script=TITLE)

class ArLoad(ArUtil):
    """Handles UI and file loading operations."""

    def __init__(self):
        super(ArLoad, self).__init__()
        path_ui         = os.path.join(os.path.dirname(__file__), "ui", f"{TITLE}.ui")
        self.wgLoad     = QtCompat.loadUi(path_ui)
        self.load_dir   = ''
        self.load_file  = ''
    
        self.software_format = {y:x.upper() for x,y in self.data['software']['EXTENSION'].items()}
        self.software_keys   = list(self.software_format.keys())

        self.wgLoad.lstScene.clear()
        self.wgLoad.lstStatus.clear()
        self.wgLoad.lstSet.clear()

        self.clear_meta()
        self.resize_widget(self.wgLoad)
        self.wgLoad.show()

        LOG.info('START : ArLoad')
   
    def press_btnAccept(self):
        """Check if load file exists; log error if not."""

        if not os.path.exists(self.load_file):
            error_message = f"FAILED LOADING : Path doesn't exist: {self.load_file}"
            self.set_status(error_message, msg_type = 3)
            return False
  
    def press_menuItemAddFolder(self):
        """add folder"""

        self.save_as = arSaveAs.start(new_file = False)
   
    def press_menuSort(self, list_widget, reverse = False):
        """sort items in list_widget"""

        file_list = []

        for index in range(list_widget.count()):
             file_list.append(list_widget.item(index).text())
        list_widget.clear()
        list_widget.addItems(sorted(file_list, reverse = reverse))
    
    def change_lstScene(self):
        """toggle visibility of lstScene based one scene depth, and generate content for lstSet"""

        self.load_dir    = self.data['project']['PATH'][self.wgLoad.lstScene.currentItem().text()]
        tmp_content      = libFunc.get_file_list(self.load_dir)
        self.scene_steps = len(self.data['rules']['SCENES'][self.wgLoad.lstScene.currentItem().text()].split('/'))

        if self.scene_steps < 5:
            self.wgLoad.lstAsset.hide()

        else:
            self.wgLoad.lstAsset.itemSelectionChanged.connect(self.change_lstAsset)
            self.wgLoad.lstAsset.show()

        self.wgLoad.lstSet.clear()
        
        if tmp_content:
            self.wgLoad.lstSet.addItems(sorted(tmp_content))
            self.wgLoad.lstSet.setCurrentRow(0)
  
    def change_lstSet(self):
        """choose between lstTask and lstAsset for items in lstSet"""

        new_path    = os.path.join(self.load_dir, self.wgLoad.lstSet.currentItem().text())
        tmp_content = libFunc.get_file_list(new_path)

        if self.scene_steps < 5:
            self.wgLoad.lstTask.clear()

            if tmp_content:
                self.wgLoad.lstTask.addItems(sorted(tmp_content))
                self.wgLoad.lstTask.setCurrentRow(0)

        else:
            self.wgLoad.lstAsset.clear()

            if tmp_content:
                self.wgLoad.lstAsset.addItems(sorted(tmp_content))
                self.wgLoad.lstAsset.setCurrentRow(0)
    
    def change_lstAsset(self):
        """populate lstTask based on assets in lstAsset"""

        new_path = os.path.join(
        self.load_dir,
        self.wgLoad.lstSet.currentItem().text(),
        self.wgLoad.lstAsset.currentItem().text()
    )
        tmp_content = libFunc.get_file_list(new_path)

        self.wgLoad.lstTask.clear()
        
        if tmp_content:
            self.wgLoad.lstTask.addItems(sorted(tmp_content))
            self.wgLoad.lstTask.setCurrentRow(0)
    
    def fill_meta(self):
        """fill metadata fields in wgPreview with file info"""
        self.wgPreview.lblTitle.setText(self.file_name)
        last_modified  = datetime.datetime.fromtimestamp(os.path.getmtime(self.load_file))
        formatted_date = str(last_modified).split(".")[0]  

        self.wgPreview.lblDate.setText(formatted_date)
        file_size_mb = os.path.getsize(self.load_file) / (1024 * 1024.0)
        self.wgPreview.lblSize.setText(f"{file_size_mb:.2f} MB")
    
    def clear_meta(self):
        """clear metadata fields in wgPreview"""

        self.wgPreview.lblUser.setText('')
        self.wgPreview.lblTitle.setText('')
        self.wgPreview.lblDate.setText('')

def execute_the_class_ar_load():
    """initialize the main widget"""
    
    global main_widget
    main_widget = ArLoad()
