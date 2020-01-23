import cv2
import time
from dollarpy import Recognizer, Template, Point
tmpl_1 = Template('X', [
    Point(0, 0, 1),
    Point(1, 1, 1),
    Point(0, 1, 2),
    Point(1, 0, 2)])
tmpl_2 = Template('line', [
    Point(0, 0),
    Point(1, 0)])
recognizer = Recognizer([tmpl_1, tmpl_2])
cap = cv2.VideoCapture(0)####### 0 indicates primary camera as for me i use my secondary
circle=True
prevx=0
prevy=0
framect=0
result=list()
laserpoints=list()
while(True):
    ret, frame = cap.read()
    blur = cv2.GaussianBlur(frame,(5,5),0)
    height, width, channels = frame.shape
    gray = cv2.cvtColor(blur, cv2.COLOR_BGR2GRAY)##############han3ml Gray Scaling n3rf aktar no2ta bright we deh hatob2a red dot######
    (minVal, maxVal, minLoc, maxLoc) = cv2.minMaxLoc(gray)
    x , y = maxLoc
    intensity= gray[y,x]
    if intensity<254:
        circle=False
    for i in range(-1,1):
        for k in range(-1,1):
            if x!=0 and y!=0:
                if y+i>=0 and x+k>=0 and y+i<gray.shape[0] and x+k<gray.shape[1]:
                    if intensity<gray[y+i,x+k]:
                        circle=False
                        break
        if not circle:
            break
    #for i in range(-1,1):
    #    for k in range(-1,1):
    #if prevx==x and prevy==y:
    #    circle=False
    prevx=x
    prevy=y
    if circle:
        cv2.circle(gray, maxLoc, 20, (255,105,97), 3)
        laserpoints.append((x,y))
    circle=True
    cv2.imshow("gray", gray)
    #cv2.imshow('frame',frame)
    if framect>=60:
        framect=0
        for i in range(0,len(laserpoints)-3):
            x1,y1=laserpoints[i]
            x2,y2=laserpoints[i+1]
            x3,y3=laserpoints[i+2]
            x4,y4=laserpoints[i+3]
            #print("X1 is "+str(x1)+"  Y1 is "+str(y1))
            try:
                result2 = recognizer.recognize([
                    Point(x1, y1, 1),
                    Point(x2, y2, 1),
                    Point(x3, y3, 1),
                    Point(x4, y4, 1),
                    Point(x1, y1, 2),
                    Point(x2, y2, 2),
                    Point(x3, y3, 2),
                    Point(x4, y4, 2), ])
                #print(result)  # Output: ('X', 0.733770116545184)
                result2,zzzz=result2
                result.append(result2)
            except ZeroDivisionError:
                print("")
        laserpoints.clear()
        if 'X' in result:
                print('X')
        elif len(result)!=0:
                print('Line')
        result.clear()
    if cv2.waitKey(1) & 0xFF == ord('e'):
        break
    framect+=1
cap.release()
cv2.destroyAllWindows()