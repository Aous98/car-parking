import numpy as np
import cv2
import pickle

# h,w,_ = img.shape
positions = []

width, height = 107, 47

def drawRec():
    event = cv2.setMouseCallback()
    if event == cv2.EVENT_LBUTTONDOWN:
        positions.append((x,y))
    if event == cv2.EVENT_RBUTTONDOWN:
        for i, pos in enumerate(positions):
            x1,y1 = pos
            if x1 < x < x1 + width and y1 < y < y1 + height:
                positions.pop(i)


img = cv2.imread('carParkImg.png')
cv2.imshow('image',img)
cv2.setMouseCallback("image", drawRec)

while True:
    img = cv2.imread('carParkImg.png')
    for pos in positions:
        cv2.rectangle(img, pos, (pos[0] + width, pos[1] + height), (0,0,255),2)

    cv2.imshow('image',img)
    drawRec()
    # cv2.setMouseCallback()
    cv2.waitKey(1)