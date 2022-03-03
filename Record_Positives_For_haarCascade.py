
"""
Created on Tue Feb 15 19:13:22 2022

Cooper Myers 
Based on: https://www.youtube.com/watch?v=dZ4itBvIjVY&t=322s
"""

import cv2

path="./cascade.xml"
cameraNo=0
objectName="Beads"
frameWidth=1920
frameHeight=1080
color=(255,0,255)
###################



cap = cv2.VideoCapture(cameraNo)
cap.set(3,frameHeight)
cap.set(4,frameWidth)

def empty(a):
    pass

count = 2000

cv2.namedWindow("Result")
#cv2.resizeWindow("Result",frameWidth,frameHeight+100)
cv2.createTrackbar("Scale","Result",400,1000,empty)
cv2.createTrackbar("Neig","Result",8,20,empty)
cv2.createTrackbar("Min Area","Result",0,100000,empty)
#cv2.createTrackbar("Brightness","Result",150,255,empty)

cascade=cv2.CascadeClassifier(path)


count = 0

while True:
    #cameraBrightness=cv2.getTrackbarPos("Brightness","Result")
    #cap.set(10,cameraBrightness)
    
    success,img = cap.read()
    #img = cv2.rotate(source, cv2.cv2.ROTATE_90_COUNTERCLOCKWISE)
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    #canny = cv2.Canny(img,150,255)
        
    scaleVal = 1+(cv2.getTrackbarPos("Scale","Result")/1000)
    neig = cv2.getTrackbarPos("Neig","Result")
    objects = cascade.detectMultiScale(img,scaleVal,neig)
    #objects = []
        #Record First count Positive Images to Positives folder.
    #if len(objects)==0 and (count+2)%3==0:
        #output_name = "./positives/output" + str(count) + ".jpg"
        #canny_output_name = "./canny_positives/output" + str(count//3) + ".jpg"
        #cv2.imwrite(output_name,img)

    count += 1
    #Draw Boxes around Objects
    for (x,y,w,h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area","Result")
        if area > minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
            cv2.putText(img,objectName,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            roi_color = img[y:y+h,x:x+w]
            


    #cv2.imshow("canny",canny)
    cv2.imshow("Result",img)
    
    
    
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
    