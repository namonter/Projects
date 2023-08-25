# -*- coding: utf-8 -*-
"""
Created on Fri Aug 11 16:17:39 2023

@author: Nathan.Montero
"""

import cv2
import numpy as np
import csv
import pandas as pd
############### Tracker Types #####################

#tracker = cv2.TrackerBoosting_create()
#tracker = cv2.TrackerMIL_create()
#tracker = cv2.TrackerKCF_create()
# tracker = cv2.legacy.TrackerTLD_create()
#tracker = cv2.TrackerMedianFlow_create()
#tracker = cv2.TrackerCSRT_create()
# tracker = cv2.legacy.TrackerMOSSE_create()

###################################################

webcam = True
# path = '1.jpg'
# videoPath = 'C:\\Users\\Nathan.Montero\\Videos\\Captures\\jagDotTest.mp4'
# cap = cv2.VideoCapture(videoPath)
cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
# cap = cv2.VideoCapture(0)

cap.set(10,160) #Cam brightness
cap.set(3,854)
cap.set(4,480)

outputFile = "output.csv"
coordDict = {"baseCenter":[], "devCenter":[]}
fields = ['Device','LeftRamp','LeftEnter','LeftExit','','CenterExit','CenterExit','','RightEnter','RightExit','RightRamp']
deviceOutput = []
# deviceRegion = []

#------------------------------------------------------------# My functions

def onTrack1(val):
    global hueLow
    hueLow=val
    # print('Hue Low',hueLow)
def onTrack2(val):
    global hueHigh
    hueHigh=val
    # print('Hue High',hueHigh)
def onTrack3(val):
    global satLow
    satLow=val
    # print('Sat Low',satLow)
def onTrack4(val):
    global satHigh
    satHigh=val
    # print('Sat High',satHigh)
def onTrack5(val):
    global valLow
    valLow=val
    # print('Val Low',valLow)
def onTrack6(val):
    global valHigh
    valHigh=val
    # print('Val High',valHigh)
    
cv2.namedWindow('myTracker')
cv2.moveWindow('myTracker',640,0)

def drawBox(img,bbox):
    x, y, w, h = int(bbox[0]), int(bbox[1]), int(bbox[2]), int(bbox[3])
    cv2.rectangle(img, (x, y), ((x + w), (y + h)), (255, 0, 255), 1, 1)
    cv2.circle(img, (int(x + (w/2)), int(y + (h/2))), radius=0, color=(0, 0, 255), thickness=2)
    # cv2.putText(img, "Tracking", (100, 75), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (0, 255, 0), 2)
    
def createLine(img, boxL, boxR):
    x1, y1, w1, h1 = int(boxL[0]), int(boxL[1]), int(boxL[2]), int(boxL[3])
    x2, y2, w2, h2 = int(boxR[0]), int(boxR[1]), int(boxR[2]), int(boxR[3])
    cv2.line(img, (int(x1 + (w1/2)), int(y1 + (h1/2))), (int(x2 + (w2/2)), int(y2 + (h2/2))), (0, 0, 255), 1)
    cv2.line(img, (int((x1 + (w1/2) + x2 + (w2/2))/2), int((y1 + (h1/2) + y2 + (h2/2))/2)+10), (int((x1 + (w1/2) + x2 + (w2/2))/2),int((y1 + (h1/2) + y2 + (h2/2))/2)-10), (0, 0, 255), 1)
    pixels = int((x2 + (w2/2)) - (x1 + (w1/2)))
    cv2.putText(img, f"200mm & {pixels} Pixels", (int((x1 + (w1/2) + x2 + (w2/2))/2)+10, int(y1 + (h1/2))-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1);
    coordDict['baseCenter'] = [int((x1 + (w1/2) + x2 + (w2/2))/2), int(y1 + (h1/2))]
    return round((pixels/200), 2) #Increase round places for more clarity

#------------------------------------------------------------#


#------------------# Yellow Start Settings, these values change w/ trackbar.
hueLow=142
hueHigh=175
satLow=0
satHigh=255
valLow=241
valHigh=255
#------------------# Green Settings
hueLowG=72
hueHighG=89
satLowG=68
satHighG=255
valLowG=241
valHighG=255

overObject = 0
#------------------# trackbar creation, ROI selection, and open output file
 
cv2.createTrackbar('Hue Low','myTracker',142,179,onTrack1)
cv2.createTrackbar('Hue High','myTracker',175,179,onTrack2)
cv2.createTrackbar('Sat Low','myTracker',0,255,onTrack3)
cv2.createTrackbar('Sat High','myTracker',255,255,onTrack4)
cv2.createTrackbar('Val Low','myTracker',241,255,onTrack5)
cv2.createTrackbar('Val High','myTracker',255,255,onTrack6)

wg = 0
hg = 0
yg = 0
xg = 0

success, frame = cap.read()
leftSelect = cv2.selectROI("Tracking",frame, True, fromCenter = True)
drawBox(frame,leftSelect)
rightSelect = cv2.selectROI("Tracking",frame, True, fromCenter = True)
# tracker.init(frame, rightSelect)

outputFile = open(f"{outputFile}", "w", newline = '')
writer = csv.writer(outputFile)

while True:
    timer = cv2.getTickCount()
    
    if webcam:
        # # Load image
        success,img = cap.read()
        
        #---------------------# Draw boxes/line for ROI
        # success, rightSelect = tracker.update(img)
        drawBox(img,leftSelect)
        drawBox(img,rightSelect)
        PixToMil = createLine(img,leftSelect,rightSelect)
        
        #---------------------#
#------------------------------------------------------------#Green Arrow Detection 
        # Convert BGR to HSV
        hsvGreen = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lowerBoundGreen=np.array([hueLowG,satLowG,valLowG])
        upperBoundGreen=np.array([hueHighG,satHighG,valHighG])
        # Threshold the HSV image to get bounds
        maskGreen=cv2.inRange(hsvGreen,lowerBoundGreen,upperBoundGreen)
        colorCntsGreen = cv2.findContours(maskGreen.copy(),
                                  cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(colorCntsGreen)>0:
            min_area = 100
            max_area = 600
            for c in colorCntsGreen:
               area = cv2.contourArea(c)
               if area > min_area and area < max_area:
                    color_area = max(colorCntsGreen, key=cv2.contourArea)
                    (xg,yg,wg,hg) = cv2.boundingRect(color_area)
                    cv2.rectangle(img,(xg,yg),(xg+wg, yg+hg),(255, 0, 0),1)
                    
                    overObject = 1
                    cv2.putText(img, "On", (int(xg+2), int(yg+(hg/2))), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,0,0), 1);
               else:
                   overObject = 0
        # cv2.putText(img, f"{overObject}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2);
            

#------------------------------------------------------------# Pink Color Detection       
        # Convert BGR to HSV
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        # define range of blue color in HSV
        lowerBound=np.array([hueLow,satLow,valLow])
        upperBound=np.array([hueHigh,satHigh,valHigh])
        # Threshold the HSV image to get bounds
        mask=cv2.inRange(hsv,lowerBound,upperBound)
        colorCnts = cv2.findContours(mask.copy(),
                                  cv2.RETR_EXTERNAL,
                                  cv2.CHAIN_APPROX_SIMPLE)[-2]

        if len(colorCnts)>0:
            color_area = max(colorCnts, key=cv2.contourArea)
            (xg,yg,wg,hg) = cv2.boundingRect(color_area)
            
            cv2.rectangle(img,(xg,yg),(xg+wg, yg+hg),(241, 82, 240),1)
            cv2.line(img, (int(xg+(wg/2)), int(yg+10)), (int(xg+(wg/2)), int(yg-10)), (241, 82, 240), 1)
            
            coordDict["devCenter"] = [int(xg+(wg/2)), yg]
            currentPosX = coordDict["devCenter"][0] - coordDict["baseCenter"][0]
            currentPosX = int(currentPosX / PixToMil)#, 0) #For more resolution on mm change rounding
            cv2.putText(img, f"{currentPosX}", (int(xg+(wg/2)+15), int(yg-10)), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1);
            
#------------------------------------------------------------# File Generation
        cv2.putText(img, f"{overObject}", (20, 80), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2);
        if overObject:
            if currentPosX > -8 and currentPosX < 8:
                deviceOutput.append(currentPosX)


#------------------------------------------------------------# Image filtering

        blur = cv2.medianBlur(img, 5)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        
        ROI= np.array([[(xg, yg+hg),(xg,yg),(xg+wg,yg),(xg+wg, yg+hg)]], dtype= np.int32)
        blank= np.zeros_like(gray)
        region_of_interest= cv2.fillPoly(blank, ROI,255)
        region_of_interest_image= cv2.bitwise_and(gray, region_of_interest)
        
        thresh = cv2.threshold(region_of_interest_image,160,255, cv2.THRESH_BINARY_INV)[1]     # If cant see circle change 1st float higher

        kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (3,3))
        opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=2)
        
        # #Countours
        # cnts = cv2.findContours(opening, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        # cnts = cnts[0] if len(cnts) == 2 else cnts[1]
        # # print (cnts[0][0][0])
        # min_area = 10
        # max_area = 50
        # black_dots = []
        # for c in cnts:
        #    area = cv2.contourArea(c)
        #    if area > min_area and area < max_area:
        #         cv2.drawContours(img, [c], -1, (36, 255, 12), 2)
        #         black_dots.append(c)
        #         cv2.putText(img, f"{c[0][0]}", c[0][0], cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1);

#------------------------------------------------------------# Text/Coords generation
   
        # if len(black_dots) > 1:
        #     xMid = round((black_dots[1][0][0][0] + black_dots[0][0][0][0]) / 2)
        #     yMid = round((black_dots[1][0][0][1] + black_dots[0][0][0][1]) / 2)
        #     if (black_dots[1][0][0][0] - black_dots[0][0][0][0]) != 0:
        #         slope = ((black_dots[1][0][0][1] - black_dots[0][0][0][1]) / (black_dots[1][0][0][0] - black_dots[0][0][0][0]))
        #     else:
        #         slope = 999999
        #     # cv2.putText(img, f"({xMid}, {yMid}+10)", (xMid, yMid-10), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (0,0,255), 1);
        #     if slope < 0.2 and slope > -0.2:
        #         cv2.line(img, black_dots[0][0][0], black_dots[1][0][0], (0, 0, 255), 1)  
        #         cv2.line(img, (xMid, yMid+5), (xMid, yMid-20), (0, 0, 255), 1)
                
#------------------------------------------------------------# FPS       
        cv2.putText(img, "Fps:", (20, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, (255,0,0), 2);
        fps = cv2.getTickFrequency() / (cv2.getTickCount() - timer);
        if fps>60: myColor = (20,230,20)
        elif fps>20: myColor = (230,20,20)
        else: myColor = (20,20,230)
        cv2.putText(img,str(int(fps)), (75, 40), cv2.FONT_HERSHEY_SIMPLEX, 0.7, myColor, 2);
        
#------------------------------------------------------------# Show Windows     

        cv2.imshow('Region of Interest', region_of_interest_image)       
        cv2.imshow('thresh', thresh)
        cv2.imshow('blur', blur)
        cv2.imshow('opening', opening)
        cv2.imshow('image', img)
        cv2.imshow('gray', gray)
        cv2.imshow('mask',mask)
        
#------------------------------------------------------------# Break windows & end processes       
        
        if cv2.waitKey(1) & 0xFF == ord('q'):
            break
try:    
    leftCenter = min(deviceOutput)
    rightCenter = max(deviceOutput)
except ValueError:
    print('error')
# deviceRegion.append(leftCenter)
# deviceRegion.append(leftCenter)

print(PixToMil)

writer.writerow(fields)
writer.writerow(['','','','','', leftCenter, rightCenter])
writer.writerow(deviceOutput)

outputFile.close()
cap.release()
cv2.destroyAllWindows()