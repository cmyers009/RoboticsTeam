
"""
Created on Tue Feb 15 19:13:22 2022

Cooper Myers 
Based on: https://www.youtube.com/watch?v=dZ4itBvIjVY&t=322s
"""

import cv2
import numpy as np
import pyrealsense_test as prt


def mask_net(img):
    j = 5
    start = 115
    end = 160
    gap = 15
    for i in range(start,end-j,j):
        lower = np.array([i,i,i])
        upper = np.array([i+j+gap,i+j+gap,i+j+gap])
        temp_mask = cv2.inRange(img,lower,upper)
        if i == start:
            mask = temp_mask
        else:
            mask = cv2.bitwise_or(mask,temp_mask)
    return mask

def mask_red_bead(hsv):
    red_thres = [
                 [[0,13,118],[0,33,198]],
                 [[0,151,39],[1,171,119]],
                 [[0,155,22],[1,175,102]],
                 [[0,162,34],[1,182,114]],
                 [[0,164,23],[1,184,103]],
                 [[0,168,16],[1,188,96]],
                 [[0,169,25],[1,190,114]],
                 [[0,175,48],[1,195,128]],        
                 [[0,187,78],[1,207,158]],
                 [[0,203,64],[0,223,144]],
                 [[93,255,0],[113,255,0]],
                 [[158,164,32],[178,184,112]],  
                 [[179,138,25],[180,213,188]],
                 
                 
                 ]
    
    for index,thres in enumerate(red_thres):
        lower = np.array(thres[0])
        upper = np.array(thres[1])
        temp_mask = cv2.inRange(hsv,lower,upper)
        if index == 0:
            mask = temp_mask
        else:
            mask = cv2.bitwise_or(mask,temp_mask)
    return mask

def mask_green_bead(hsv):
    green_thres = [[[76,176,49],[96,196,129]],
                   [[76,227,61],[96,247,141]],
                   [[71,255,19],[91,255,99]],
                   [[73,255,1],[93,255,81]],
                   [[77,255,85],[97,255,165]],
                   [[75,136,0],[95,156,0]],
                   [[68,211,0],[90,254,0]],
                   [[73,235,12],[93,255,92]]]
    for index,thres in enumerate(green_thres):
        lower = np.array(thres[0])
        upper = np.array(thres[1])
        temp_mask = cv2.inRange(hsv,lower,upper)
        if index == 0:
            mask = temp_mask
        else:
            mask = cv2.bitwise_or(mask,temp_mask)
    return mask

def getBordered(image, width):
    bg = np.zeros(image.shape)
    contours, _ = cv2.findContours(image, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
    biggest = 0
    bigcontour = None
    for contour in contours:
        area = cv2.contourArea(contour) 
        if area > biggest:
            biggest = area
            bigcontour = contour
    return cv2.drawContours(bg, [bigcontour], 0, (255, 255, 255), width).astype(bool) 

#Works Perfect
def mask_blue_bead(hsv):
    blue_thres = [[[95,215,55],[115,235,135]],
                  [[96,113,0],[116,133,0]],
                  [[95,228,50],[115,248,130]],
                  [[95,115,65,],[115,255,145]],
                  [[94,143,5],[114,163,85]]
]
    for index,thres in enumerate(blue_thres):
        lower = np.array(thres[0])
        upper = np.array(thres[1])
        temp_mask = cv2.inRange(hsv,lower,upper)
        if index == 0:
            mask = temp_mask
        else:
            mask = cv2.bitwise_or(mask,temp_mask)
    return mask
def mask_purple_bead(hsv):
    purple_thres = [[[118,144,79],[138,164,159]],
                    [[118,108,40],[138,128,120]],
                    [[121,113,22],[141,133,102]],
                    [[124,164,1],[144,184,81]],
                    [[120,107,10],[140,127,90]],
                    [[120,127,27],[140,147,107]],
                    [[116,133,19],[136,153,99]],
                    [[114,104,58],[134,124,138]]]
    for index,thres in enumerate(purple_thres):
        lower = np.array(thres[0])
        upper = np.array(thres[1])
        temp_mask = cv2.inRange(hsv,lower,upper)
        if index == 0:
            mask = temp_mask
        else:
            mask = cv2.bitwise_or(mask,temp_mask)
    return mask




def merge_all_masks(masks):
    for index,mask in enumerate(masks):
        if index==0:
            merge = mask
        else:
            merge = cv2.bitwise_or(merge,mask)
    
    return merge


def get_bead_output(img,distance_mask):
    global bead_cascade
    objectName="Beads"
    color=(255,0,255)
    
    hsv = cv2.cvtColor(img,cv2.COLOR_BGR2HSV) 
    
    red_bead_mask = mask_red_bead(hsv)
    green_bead_mask = mask_green_bead(hsv)
    blue_bead_mask = mask_blue_bead(hsv)
    purple_bead_mask = mask_purple_bead(hsv)
    
    bead_mask = merge_all_masks([distance_mask,red_bead_mask,green_bead_mask,blue_bead_mask,purple_bead_mask])
   
    bead_color_mask = cv2.bitwise_and(img, img, mask=bead_mask)
    
    #cv2.imshow("Bead Color Mask",bead_color_mask)
    
    scaleVal = 1+(cv2.getTrackbarPos("Scale","Detect_Beads")/1000)
    neig = cv2.getTrackbarPos("Neig","Detect_Beads")
    objects = bead_cascade.detectMultiScale(bead_color_mask,scaleVal,neig)
    
        #Draw Boxes around Objects
    for (x,y,w,h) in objects:
        area = w*h
        minArea = cv2.getTrackbarPos("Min Area","Detect_Beads")
        if area > minArea:
            cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
            cv2.putText(img,objectName,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
            roi_color = img[y:y+h,x:x+w]
            
    #cv2.imshow("Detect_Beads",img)
    
    
    return bead_color_mask

def get_net_output(img,distance_mask):
    path="./masked_net_cascade.xml"
    objectName="Net"
    color=(255,0,255)
    
    net_color_mask = mask_net(pre_img)
    net_mask = merge_all_masks([net_color_mask,distance_mask])
    #cv2.imshow("Net Mask",net_mask)
    
    return net_mask

def save_images(bead_output,net_output,count):
    bead_output_name = "./bead_output/output" + str(count) + ".jpg"
    net_output_name = "./net_output/output"+str(count)+".jpg"
    cv2.imwrite(bead_output_name,bead_output)
    cv2.imwrite(net_output_name,net_output)
   
def get_image(camera_no):
    if camera_no == 0:
        global cap0
        success,img = cap0.read()
        return img
    elif camera_no ==1:
        success,img = cap1.read()
        return img
   


bead_path="./masked_bead_cascade.xml"
cameraNo=1
objectName="Beads"
frameWidth=640
frameHeight=480
color=(255,0,255)

cap0 = cv2.VideoCapture(0)
cap0.set(3,frameHeight)
cap0.set(4,frameWidth)

cap1 = cv2.VideoCapture(1)
cap1.set(3,frameHeight)
cap1.set(4,frameWidth)



def empty(a):
    pass


cv2.namedWindow("Detect_Beads")
cv2.resizeWindow("Detect_Beads",frameWidth,frameHeight+100)
cv2.createTrackbar("Scale","Detect_Beads",400,1000,empty)
cv2.createTrackbar("Neig","Detect_Beads",1000,2000,empty)
cv2.createTrackbar("Min Area","Detect_Beads",0,100000,empty)
cv2.createTrackbar("Brightness","Detect_Beads",150,255,empty)

bead_cascade=cv2.CascadeClassifier(bead_path)


count = 0

while True:

    
    success,pre_img = cap0.read()
    distance_binary = prt.colorize_lidar(prt.get_depth_frame())
    

    img = pre_img

    bead_output = get_bead_output(pre_img, distance_binary)
    net_output = get_net_output(pre_img, distance_binary)

    #save_images(bead_output,net_output,count)

    
    
    
    cv2.imshow("test",img)
    

    count += 1

    
    
    if cv2.waitKey(1)& 0xFF == ord('q'):
        break
    
    
    
