# -*- coding: utf-8 -*-
"""
Created on Thu Feb 17 15:16:00 2022

@author: student
"""

import cv2

image_name = "N ("
image_folder_path = "../cascade/N/"
output_folder_path = "./output/"
index = 1
temp_name = image_folder_path + image_name + str(index) + ").jpg"
temp_output_name = output_folder_path + image_name + str(index) + ").jpg"
image = cv2.imread(temp_name)
while len(image) >0:
    
    gray = cv2.cvtColor(image,cv2.COLOR_BGR2GRAY)
    cv2.imwrite(temp_output_name,gray)
    index += 1
    temp_name = image_folder_path + image_name + str(index) + ").jpg"
    temp_output_name = output_folder_path + image_name + str(index) + ").jpg"
    image = cv2.imread(temp_name)
    
        