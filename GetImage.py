from typing import ItemsView
import cv2
cv2.namedWindow("preview")
vc = cv2.VideoCapture(0)

if vc.isOpened():
    rval, frame = vc.read()
    # cv2.imshow("preview",frame)

    height = len(frame)
    width = len(frame[0])

else:
    rval = False

while rval:
    rval, frame = vc.read()
    key = cv2.waitKey(15)

    #smaller = cv2.resize(frame, (16,9), interpolation=cv2.INTER_CUBIC)
    #smaller = cv2.blur(smaller, (2,2), borderType=cv2.BORDER_REFLECT)

    # print(smaller[1][1], smaller[1][2], smaller[1][3])

    #larger = cv2.resize(smaller, (640, 480), interpolation=cv2.INTER_AREA)


    larger = cv2.GaussianBlur(frame, (10,10), 0)

    cv2.rectangle(larger, (11,11), (630, 470), (0,0,0), -1)

    cv2.imshow("preview",larger)

    if key == 27: # ESC key
        break

cv2.destroyWindow("preview")