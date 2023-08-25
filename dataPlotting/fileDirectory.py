# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:49:42 2022

@author: Nathan.Montero
"""

from tkinter import filedialog #, messagebox
import os

class FileCode():

    def __init__(self, parent):
        self.parent = parent
        self.folder_path = str()
        self.parent.filename = str()

    def openDir(self):
            self.folder_path = filedialog.askdirectory(initialdir=os.getcwd(), title="Find Folder") #filetype=("CSV files", "*.csv")
            return self.folder_path
        
    def openFile(self):
        self.parent.filename = filedialog.askopenfilename(initialdir=os.getcwd(), title="Open File", filetype=(("CSV files", "*.csv"),("ALL Files", "*.*")))
        return self.parent.filename
                           
    def closeFile(self):
            if self.file is not None:
                self.file.close()
                self.parent.filename = ''
                self.file= None
                return True
            return None                                        


    # def newFile(self,filename=''):
    #     if filename == '':
    #         filename = filedialog.asksaveasfilename(initialdir=os.getcwd(), title="Create New File",
    #                                                 defaultextension="*.txt",
    #                                                 filetype=(("TXT files", "*.txt"), ("CSV files", "*.csv"),
    #                                                           ("ALL Files", "*.*")))
    #     if filename != '':
    #         self.parent.filename = filename
    #         # if os.path.isfile(filename):
    #         #     if messagebox.askyesno(
    #         #        message='Confirm Destruction of previous file ?',
    #         #        icon='question', title='Destroying'):
    #         #         os.remove(filename)
    #         try:
    #             self.file = open(self.parent.filename, encoding='utf-8', mode='w')
    #         except IOError:
    #             print("error in opening file")
    #             self.file.close()
    #             return None
    #         return self.file
    #     return None

    
 