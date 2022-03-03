# -*- coding: utf-8 -*-
"""
Created on Tue Mar  1 18:41:44 2022

@author: student
"""

import pyrealsense2 as rs
import numpy as np
import matplotlib.pyplot as plt

def set_min_distance():
        pipeline = rs.pipeline()
        config = rs.config()
        config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
        profile = pipeline.start(config) # Start streaming
        sensor_dep = profile.get_device().first_depth_sensor()
        if sensor_dep.supports(rs.option.min_distance):
            print ("Trying to set min_distance")
            dist = sensor_dep.get_option(rs.option.min_distance)
            print("min_distance = %d" % dist)
            print("Setting min_distance to new value")
            dist = sensor_dep.set_option( rs.option.min_distance, 0)
            #max_dist = sensor_dep.set_option( rs.option.max_distance, 10)
            dist = sensor_dep.get_option(rs.option.min_distance)
            print("New min_distance = %d" % dist)
        profile = pipeline.stop
        return pipeline
    
def get_depth_frame():
        global pipeline
        frames = pipeline.wait_for_frames()
        depth_frame = frames.get_depth_frame()   
        return depth_frame
def find_distance(x,y,depth_frame):

        # Create a context object. This object owns the handles to all connected realsense devices
    depth = depth_frame.get_distance(x,y)
    print(x,y,str(depth))   


def colorize_lidar(depth_frame):
    colorizer = rs.colorizer()
    colorized_depth = np.asanyarray(colorizer.colorize(depth_frame).get_data())
    plt.imshow(colorized_depth)


pipeline = set_min_distance()
depth_frame = get_depth_frame()
find_distance(100,100,depth_frame)
colorize_lidar(depth_frame)

