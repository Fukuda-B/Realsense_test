import pyrealsense2 as rs
import numpy as np
import cv2
import time

def rec():
    config = rs.config()
    config.enable_stream(rs.stream.infrared, 1, 640, 480, rs.format.y8, 30)
    config.enable_stream(rs.stream.depth, 640, 480, rs.format.z16, 30)
    config.enable_stream(rs.stream.color, 640, 480, rs.format.bgr8, 30)

    dt = time.datetime.datetime.now()
    ut = dt.timestamp()
    ddt = list(str(ut)).remove('.')
    config.enable_record_to_file(f'realsese_{ddt}.bag')

    pipeline = rs.pipeline()
    pipeline.start(config)
    start = time.time()
    frame_no = 1
    try:
        while True:
            frames = pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            ir_frame = frames.get_infrared_frame()
            fps  = frame_no / (time.time() - start)  
            print(fps)
            frame_no = frame_no+1  
            if not ir_frame or not color_frame  :   
                ir_image = np.asanyarray(ir_frame .get_data())    
                color_image = np.asanyarray(color_frame.get_data()) 

    finally:    
        pipeline.stop()

if __name__ == "__main__":
    rec()
