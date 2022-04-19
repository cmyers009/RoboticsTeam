
"""
Created on Tue Feb 15 19:13:22 2022

Cooper Myers 
Based on: https://www.youtube.com/watch?v=dZ4itBvIjVY&t=322s
"""
#Imports
import cv2
import pyrealsense_test as rs_test
import time
import numpy as np

def empty(a):
    pass
def mask_net(img):
    white_lower_thres=np.array((100,100,100),dtype="uint8")
    white_lowermiddle_thres=np.array((125,125,125),dtype="uint8")
    white_middle_thres=np.array((150,150,150),dtype="uint8")
    white_middleupper_thres = np.array((175,175,175),dtype="uint8")
    white_upper_thres=np.array((200,200,200),dtype="uint8")
    white_max_thres = np.array((255,255,255),dtype="uint8")
    
    mask1= cv2.inRange(img,white_lower_thres-(5,5,5),white_lowermiddle_thres+(5,5,5))
    mask2 = cv2.inRange(img,white_lowermiddle_thres-(5,5,5),white_middle_thres+(5,5,5))
    mask3 = cv2.inRange(img,white_middle_thres-(5,5,5),white_middleupper_thres+(5,5,5))
    mask4 = cv2.inRange(img,white_middleupper_thres-(5,5,5),white_upper_thres+(5,5,5))
    mask5 = cv2.inRange(img,white_upper_thres-(5,5,5),white_max_thres-(0,0,0))
    
    mask12 = cv2.bitwise_or(mask1,mask2)
    mask34 = cv2.bitwise_or(mask3,mask4)
    mask = cv2.bitwise_or(mask12,mask34)
    return mask


def detect_objects(img, cascade, scale_val=100, neig=4, min_area=0,max_distance=0.5):

    objects = cascade.detectMultiScale(img,scale_val,neig)
    valid_objects_list = []
    for (x,y,w,h) in objects:
        area = w*h
        if area < min_area:
            pass
        
        distance = rs_test.main(x+w//2,y+h//2)
        print(f'Found object at {x+w//2},{y+h//2} with distance of: {distance}')
        if distance < max_distance and distance != 0:
            print("Distance is less than max distance but not undefined. VALID")
            valid_objects_list.append({'x':x,'y':y,'w':w,'h':h,'center':[x+w//2,y+h//2],'distance':distance})
        elif distance > max_distance:
            pass
            #print("Distance > max so invalid.")
        else:
            pass
            #print("Distance == 0 so undefined aka invalid")
    return valid_objects_list

#Draw Boxes around Objects
def draw_objects(img,valid_objects_list,object_name,color=(255,0,255)):
    for item in valid_objects_list:
        x=item['x']
        y=item['y']
        w=item['w']
        h=item['h']
        cv2.rectangle(img,(x,y),(x+w,y+h),color,3)
        cv2.putText(img,object_name,(x,y-5),cv2.FONT_HERSHEY_COMPLEX_SMALL,1,color,2)
        roi_color = img[y:y+h,x:x+w]
    

    
    
def main():

    
    #Settings
    bead_path="./bead_cascade.xml"
    net_path = './masked_net_cascade.xml'

    cameraNo=1
    frameWidth=640
    frameHeight=480
    color=(255,0,255)
###################
    #Set up camera with settings
    cap = cv2.VideoCapture(cameraNo)
    cap.set(3,frameHeight)
    cap.set(4,frameWidth)
    
    #Set up classifier
    bead_cascade=cv2.CascadeClassifier(bead_path)
    net_cascade=cv2.CascadeClassifier(net_path)
    
    #Create Window
    cv2.namedWindow("Result")
#    cv2.createTrackbar("Scale","Result",400,1000,empty)
#    cv2.createTrackbar("Neig","Result",8,20,empty)
#    cv2.createTrackbar("Min Area","Result",0,100000,empty)
    
    #While loop
    while True:
        
        #Capture video
        success,img = cap.read()

        valid_beads_list = detect_objects(img, bead_cascade, scale_val=1.4, neig=6, min_area=0,max_distance=0.5)
        draw_objects(img,valid_beads_list,"Beads",color=(255,0,255))
        
        mask=mask_net(img)
        valid_nets_list = detect_objects(mask, net_cascade, scale_val=1.4, neig=150, min_area=0,max_distance=0.5)
        draw_objects(img,valid_nets_list,"Net",color=(0,255,255))
        
        
        #Show image
        cv2.imshow("Result",img)
        
        #4 Frames / Second
        time.sleep(.05)
    
        #Quit loop when q is pressed
        if cv2.waitKey(1)& 0xFF == ord('q'):
            break


main()

