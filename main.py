'''
    Realsenseの動作テスト

    録画: py main.py rec
    再生: py main.py play
'''

import os
import sys
import cv2
import time
import numpy as np
import pyrealsense2 as rs

class Settings():
    def __init__(self):
        self.V_SIZE = (640, 480) # 画面サイズ
        self.FPS = 30 # フレームレート

        desktop = os.path.expanduser('~/Desktop')
        self.F_NAME = 'realsense_b.bag'
        self.FULL_NAME = os.path.join(desktop, self.F_NAME)

class Realsense_test():
    def rec(settings):
        config = rs.config()
        config.enable_stream(rs.stream.infrared, 1, *settings.V_SIZE, rs.format.y8, settings.FPS)
        config.enable_stream(rs.stream.depth, *settings.V_SIZE, rs.format.z16, settings.FPS)
        config.enable_stream(rs.stream.color, *settings.V_SIZE, rs.format.bgr8, settings.FPS)
        config.enable_record_to_file(settings.FULL_NAME)

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
                frame_no += 1
                if not ir_frame or not color_frame:
                    ir_image = np.asanyarray(ir_frame.get_data())
                    color_image = np.asanyarray(color_frame.get_data())
        except Exception as e:
            print(e)
        finally:    
            pipeline.stop()

    def play(settings):
        config = rs.config()
        config.enable_device_from_file(settings.FULL_NAME)
        config.enable_stream(rs.stream.color, *settings.V_SIZE, rs.format.bgr8, settings.FPS)
        config.enable_stream(rs.stream.depth, *settings.V_SIZE, rs.format.z16, settings.FPS)
        config.enable_stream(rs.stream.infrared, 1, *settings.V_SIZE, rs.format.y8, settings.FPS)

        pipeline = rs.pipeline()
        profile = pipeline.start(config)

        try:
            while True:
                frames = pipeline.wait_for_frames()
                ir_frame = frames.get_infrared_frame()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame or not ir_frame:
                    continue

                ir_image = np.asanyarray(ir_frame .get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                cv2.namedWindow('ir_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('ir_image', ir_image)
                cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('color_image', color_image)
                cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('depth_image', depth_image)
                cv2.waitKey(1)
        except Exception as e:
            print(e)
        finally:
            pipeline.stop()

if __name__ == "__main__":
    settings = Settings()
    tester = Realsense_test()
    if len(sys.argv) >= 2:
        if str(sys.argv[1]) == 'rec':
            tester.rec(settings)
        else:
            tester.play(settings)
    else:
        print(f'----- option -----\nrecode: py main.py rec\nplay  : py main.py play')
