import cv2
import numpy as np
from operator import floordiv

vc = cv2.VideoCapture(0)
cv2.namedWindow("top")
cv2.namedWindow("bottom")

if vc.isOpened():
    rval, frame = vc.read()

    height = len(frame)
    width = len(frame[0])
else:
    rval = False

lights = (16,9)
history = 5

top    = np.zeros((lights[0],   1, 3), dtype = "uint8")
bottom = np.zeros((lights[0],   1, 3), dtype = "uint8")
left   = np.zeros((lights[1]-2, 1, 3), dtype = "uint8")
right  = np.zeros((lights[1]-2, 1, 3), dtype = "uint8")

topHistory    = np.zeros((lights[0],   history, 3), dtype = "uint8")
bottomHistory = np.zeros((lights[0],   history, 3), dtype = "uint8")
leftHistory   = np.zeros((lights[1]-2, history, 3), dtype = "uint8")
rightHistory  = np.zeros((lights[1]-2, history, 3), dtype = "uint8")

currIndex = 0
prevIndex = history - 1

while rval:
    rval, frame = vc.read()
    smaller = cv2.resize(frame, lights)

    for x in range(0,lights[0]-1):
        top[x][0]    = top[x][0]    - topHistory[x][currIndex]
        bottom[x][0] = bottom[x][0] - bottomHistory[x][currIndex]

        topHistory[x][currIndex]    = smaller[0][x] / history
        bottomHistory[x][currIndex] = smaller[lights[1]-1][x] / history

        top[x][0]    = top[x][0]    + topHistory[x][currIndex]
        bottom[x][0] = bottom[x][0] + bottomHistory[x][currIndex]

    for y in range(1,lights[1]-2):
        left[y][0]  = left[y][0]  - leftHistory[y][currIndex]
        right[y][0] = right[y][0] - rightHistory[y][currIndex]
        
        leftHistory[y][currIndex]  = smaller[y][0] / history
        rightHistory[y][currIndex] = smaller[y][lights[0]-1] / history

        left[y][0]  = left[y][0]  + leftHistory[y][currIndex]
        right[y][0] = right[y][0] + rightHistory[y][currIndex]

    prevIndex = currIndex
    currIndex = currIndex + 1
    if currIndex >= history:
        currIndex = 0

    topLarger = cv2.resize(cv2.transpose(top), (width, int(height/lights[1])), interpolation=cv2.INTER_AREA)
    cv2.imshow("top",topLarger)
    
    bottomLarger = cv2.resize(cv2.transpose(bottom), (width, int(height/lights[1])), interpolation=cv2.INTER_AREA)
    cv2.imshow("bottom",bottomLarger)

    
    key = cv2.waitKey(15)
    if key == 27: # ESC key
        break

cv2.destroyAllWindows()