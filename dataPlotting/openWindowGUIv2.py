# -*- coding: utf-8 -*-
"""
Created on Mon Jun 27 11:30:45 2022

@author: Nathan.Montero
"""

import os
import pygubu
import pathlib
import fileDirectory
from tkinter.constants import DISABLED, NORMAL
import tkinter as tk
import csv
import numpy as np
import pandas as pd
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
from matplotlib.figure import Figure
from PIL import ImageTk, Image

PROJECT_PATH = pathlib.Path(__file__).parent
PROJECT_UI = PROJECT_PATH / "scanDataThresholdGUI.ui"

x1 = ["Stud Strength",]
x2 = ["Ratio", ]
x3 = ["Edge", ]

keystrokeListX = []
dfHeader = []
dfHeaderCheck = {}
dataframeDict = {}
fields = ["",]
rows = []
inputFile = ""
outputFile = "output.csv"
dataDirectory = ''
keystrokeCheck = False
pd.options.display.max_rows = 2000
lineSize = 1.5


#Builds the class for thresholdGUI.ui
class ThresholdAppGUI:
    def __init__(self, parent, pCmdDefinitions, master = None):
        self.parent = parent
        self.parentCmdDefinitions = pCmdDefinitions
        
        self.builder = builder = pygubu.Builder()
        builder.add_resource_path(PROJECT_PATH)
        builder.add_from_file(PROJECT_UI)
        # Main widget
        self.mainwindow = builder.get_object("Main", master)
        builder.connect_callbacks(self)
        
        #------------------------------------------------------# Plot
        fcontainer = builder.get_object('fcontainer')
        # Setup matplotlib canvas
        self.figure = fig = Figure(figsize=(6, 4), dpi=100)
        self.canvas = canvas = FigureCanvasTkAgg(fig, master=fcontainer)
        canvas.get_tk_widget().pack(side=tk.LEFT, fill=tk.BOTH, expand=1)
        #------------------------------------------------------#
        canva = builder.get_object("canvas2")
        fpath = os.path.join(PROJECT_PATH, "zirconImage.jpg")
        aux = Image.open(fpath)
        self.img = ImageTk.PhotoImage(aux)
        canva.create_image(0, 0, image =self.img, anchor='nw')
        
        #------------------------------------------------------#

    """ Window Button COMMANDS """
    #Runs the GUI window loop
    def run(self):
        self.mainwindow.mainloop()
        
    def _quit(self):
        root.quit()
        root.destroy()
        
    #--------------------------------------------------# Plotting functions
    def makeSubplot(self): #function for clearing figure and drawing subplot 
        self.figure.clf()
        global a
        global b
        a = self.figure.add_subplot(111)
        b = a.twinx()
        self.canvas.draw()
        
    def canvasDraw(self):
        self.figure.legend(bbox_to_anchor=(1, 1), ncol = len(dfHeaderCheck), fontsize = '8')
        self.canvas.draw()
        
    # def multiPlotDraw(self, dataFrame, columnS, fileNum):
    #     index = 0
    #     for button, status in buttonCheckList.items():
    #         if status == 1:
    #             a.plot(dataFrame[columnS[index]],linewidth=lineSize, label = f"{fileNum}")
    #         index += 1
        
    def on_plot_clicked(self):
        print(dfHeader)
        #---------#
        app.makeSubplot()
        #---------# plot lines based on button checklist
        
        for key, value in dataframeDict.items():
            a.plot(value, linewidth=lineSize)
        #---------# Temporary spot for main
        mainProgram()
        #---------#
        if keystrokeCheck == True:
            for xPos in keystrokeListX:
                a.axvline(x=xPos, color = 'b', linewidth=lineSize - 1.0)
        #---------#
        # index = 0
        # for button, status in buttonCheckList.items():
        #     if status == 1:
        #         if button != 'ratioCheck':
        #             a.plot(df[cols[index]],linewidth=lineSize, label = button[:-5])
        #         else:
        #             b.plot(df[cols[index]],linewidth=lineSize, label = button[:-5])
        #     index += 1
        #---------# Updating plot labels
        # label_A = self.builder.get_variable('txtXAxis')
        # label_B = self.builder.get_variable('txtYAxis')
        # label_C = self.builder.get_variable('txtTitleEntry')
        # label_A.set('xTest!')
        # label_B.set('yTest!')
        # label_C.set(fileSelected[25:-4])
        #---------#
        self.figure.legend(bbox_to_anchor=(1, 1), ncol = len(dfHeaderCheck), fontsize = '8')
        self.canvas.draw()
        #---------#
        
    def onClickClear(self):
        app.makeSubplot()
        for button in dfHeaderCheck:
            self.builder.tkvariables[button].set(False)
            dfHeaderCheck[button] = 0
            
    def savePlotImage(self):
        self.figure.savefig('PlotSave.jpg')
        print("Plot Saved")
        
    #--------------------------------------------------# Directory functions
        
    #Functions for opening specified folders and outputting setting the entry boxes as those directories.              
    def cmdOpenDataDir(self):
        global dataDirectory
        label_G = self.builder.get_variable('txtDataDir')
        p_text = self.parentCmdDefinitions.openDir()
        if p_text is None:
            p_text = "No file loaded."
        label_G.set(p_text)
        dataDirectory = p_text
        #-------# Create DataFrame
        app.dataframeCollect(0)
        #---------# Edit object States
        entryWidget = self.builder.get_object('dataDirEnt', master = 'dataDir')
        entryWidget.configure(state = NORMAL)
        entryWidget = self.builder.get_object('fileSelectEntry', master = 'fileSelect')
        entryWidget.configure(state = DISABLED)
        #---------#
        
    def cmdFindFile(self):
        global dataDirectory
        global df
        global cols
        
        label_G = self.builder.get_variable('txtFileSelect')
        p_text = self.parentCmdDefinitions.openFile()
        if p_text is None:
            p_text = "No file loaded."
        label_G.set(p_text)
        dataDirectory = p_text
        #-------# Create DataFrame
        app.dataframeCollect(1)
        #---------# Edit object States
        entryWidget = self.builder.get_object('fileSelectEntry', master = 'fileSelect')
        entryWidget.configure(state = NORMAL)
        entryWidget = self.builder.get_object('dataDirEnt', master = 'dataDir')
        entryWidget.configure(state = DISABLED)
        
    #--------------------------------------------------# Message Pop-ups
      
    def directoryWarning(self):
        tk.messagebox.showinfo("Warning", "No Directory Selected")
        
    #--------------------------------------------------# Functions to determine what to plot/ plot options
    def lineScale(self, lineWidth):
        global lineSize
        lineSize = lineWidth
    
    def keystrokeChecked(self):
        global keystrokeCheck
        if dataDirectory != '':
            if self.builder.tkvariables['keystrokeCheck'].get() == True:
                keystrokeCheck = True
            else:
                keystrokeCheck = False
        else:        
            self.builder.tkvariables['keystrokeCheck'].set(False)
            keystrokeCheck = False
            app.directoryWarning()
        
                  
    def ratioChecked(self):
        app.buttonCheck('ratio')

    def leftAmpChecked(self):
        app.buttonCheck('leftAmp')

    def rightAmpChecked(self):
        app.buttonCheck('rightAmp')

    def regionChecked(self):
        app.buttonCheck('region')

    def barStrChecked(self):
        app.buttonCheck('bar strength')

    def studStrChecked(self):
        app.buttonCheck('studStr')

    def metalChecked(self):
        app.buttonCheck('metal')

    def weakSignalChecked(self):
        app.buttonCheck('weakSignal')
            
    def buttonCheck(self, checkBox):
        if self.builder.tkvariables[checkBox].get() == True:
            dfHeaderCheck[checkBox] = 1
        else:
            dfHeaderCheck[checkBox] = 0
    #--------------------------------------------------# Sets up dataframe after directory selection
    def dataframeCollect(self, select):
        count = 0
        if select == 0:
            for filename in os.listdir(dataDirectory):
                f = os.path.join(dataDirectory, filename)
                count = count + 1
            
                if os.path.isfile(f):
                    if filename.endswith('.csv'):
                        print(f)
                        if filename != "output.csv":
                            tempDF = pd.read_csv(f)
                            dataframeDict[f'df{count}'] = tempDF
        elif select == 1:
            count = count + 1
            
            if os.path.isfile(dataDirectory):
                if dataDirectory.endswith('.csv'):
                    print(dataDirectory)
                    if dataDirectory != "output.csv":
                        tempDF = pd.read_csv(dataDirectory)
                        dataframeDict[f'df{count}'] = tempDF
                        
        dfHeader = list(dataframeDict['df1'].columns)
        for element in dfHeader:
            dfHeaderCheck[element] = 0
    #--------------------------------------------------#
    

'''Main Program'''
class scanDataInfo:
    
    def __init__(self, filename, personName, outlier): #Class Initialization
        self.filename = filename                       #Current Filename
        self.personName = personName                   #Name of person who took data in file
        self. outlier = outlier                        #Outlier values
        
        
    def filenameFieldAppend(self):
        letterCount = 0
        
        self.filename = self.filename[0:-4] #Removes .csv
        
        for element in self.filename:       
            letterCount = letterCount + 1
            if element == 'n':                              #Only concatenates once finding 'n' end of 'wall thickness' unit
                self.personName = self.filename[-7:-4]      #Takes name of person who took data
                self.filename = self.filename[0:letterCount] + " " + self.filename[-7:] + "   " #Concatenates wall thickness + 
                break                                                                           #personName + direction of scan
        
        if self.filename[-6:-4] == "LR": #Depending on scan direction appends correct edge to Stud Strength & Ratio Values
            x3.append("LE")
            x3.append("RE")
        
        else:
            x3.append("RE")
            x3.append("LE")
        
        fields.append(self.filename) #Append field to match data to filename
        fields.append(self.filename)
    
        
def outlierAlgorithm(listToSearch):
    convertToInt = []
    for element in listToSearch[1:-1]:
        convertToInt.append(int(element))
    #create the data and take the mean and standard deviation
    data = np.array(convertToInt)
    mean = np.mean(data)
    std_dev = np.std(data)
    #More than 3 standard deviations from the mean an outlier
    threshold = 2
    #create the condition to find outliers
    outliers = data[np.abs(data - mean) > threshold * std_dev]
    print(outliers)
    
def averageValue(listToAverage):
    averageReturn = 0
    avgCount = 0
    leftEdgeAvg = 0
    rightEdgeAvg = 0
    if listToAverage[0] == "Stud Strength":     #Determine data type
        for element in listToAverage[1:]:
                    avgCount = avgCount + 1
                    if x3[avgCount] == "LE":    #Determine edge and add to that average
                        leftEdgeAvg = leftEdgeAvg + int(element)
                    elif x3[avgCount] == "RE":
                        rightEdgeAvg = rightEdgeAvg + int(element)
    
    elif listToAverage[0] == "Ratio":           #Determine data type
        for element in listToAverage[1:]:
                    avgCount = avgCount + 1
                    if x3[avgCount] == "LE":    #Determine edge and add to that average
                        leftEdgeAvg = leftEdgeAvg + int(element)
                    elif x3[avgCount] == "RE":
                        rightEdgeAvg = rightEdgeAvg + int(element)
        
    rightEdgeAvg = round((rightEdgeAvg / (avgCount/2)),0) #Grabs sum of all edges and divides by number of (edges/2)
    leftEdgeAvg = round((leftEdgeAvg / (avgCount/2)), 0)
    averageReturn = f"LE {leftEdgeAvg}, RE {rightEdgeAvg}"
    return averageReturn

def splitTest(string):
    txt = string.split("_")
    print(txt)
        

def mainProgram():
    global fields
    outputFile = "output.csv"
   
    
    try: 
        
        #open our writing file for output, and then proceeds to iterate through the selected directory.
        outputFile = open(f"{outputFile}", "w", newline = '')
        writer = csv.writer(outputFile)
        
        if keystrokeCheck == True:
            for filename in os.listdir(dataDirectory):
                f = os.path.join(dataDirectory, filename)
                
                #check first if is a file, then if it is a csv, and then makes sure it isn't our output file currently writing in.
                if os.path.isfile(f):
                    if filename.endswith('.csv'):
                        print(f)
                        if filename != "output.csv":
                            #Opens the next file in directory and then proceeds to write in the currentFileName and fields selected
                            with open(f, "r") as csvfile: #f"{dataDirectory}\{filename}"
                                inputFile = csv.reader(csvfile)
                                # currentFileName = []
                                next(inputFile)
                                # currentFileName.append(filename)
                                splitTest(filename)
                                filename = scanDataInfo(filename, " ", 0)
                                filename.filenameFieldAppend()
                            
                                
                                #Iterate through the inputFile writing the needed data in new rows
                                x1count = 0
                                keysX = 0
    
                                for row in inputFile:
                                    keysX += 1
                                    if float(row[13]) == 500:
                                            x1.append(row[5])
                                            x2.append(row[0])
                                            x1count = x1count + 1
                                            keystrokeListX.append(keysX)
                                
                                    if x1count > 2:
                                        x1count = x1count - 1
                                        x1.remove(x1[-3])
                                        x2.remove(x2[-3])                            
                            csvfile.close()
            fields.append("Averages")       #Appending for Averages
            x1.append(averageValue(x1))
            x2.append(averageValue(x2))
            outlierAlgorithm(x1)
            
            writer.writerow(fields)         #Write all data/lists to output file
            writer.writerow(x1)
            writer.writerow(x2)
            writer.writerow(x3)
        else:     
            print("no keystroke")
   
    except: 
        print ("Something went wrong. - Try close output - Select DataDir")
    else:
        print("done")
        outputFile.close()


#"main" where it starts tkinter and creates the classes for GUI and then runs.
if __name__ == "__main__":
    root = tk.Tk()
    definitionsDev = fileDirectory.FileCode(root)
    app = ThresholdAppGUI(root, definitionsDev)
    app.run()
