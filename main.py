'''
    Realsenseの動作テスト

    録画: py main.py rec
    再生: py main.py play
  ライブ: py main.py live

    -----

    Realsense D400-Series, https://www.mouser.com/pdfdocs/Intel_D400_Series_Datasheet.pdf
    librealsense example, 
        https://dev.intelrealsense.com/docs/python2,
        https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/python-tutorial-1-depth.py,
        https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/opencv_viewer_example.py,

'''

import os
import sys
import cv2
import time
import numpy as np
import pyrealsense2 as rs

class Settings():
    def __init__(self):
        self.V_SIZE = (640, 480)        # 画面サイズ
        self.FPS = 30                   # フレームレート
        self.HEATMAP = True             # ヒートマップ表示
        self.F_NAME = 'realsense_b.bag' # ファイル名

        desktop = os.path.expanduser('~/Desktop')
        self.FULL_NAME = os.path.join(desktop, self.F_NAME)

class Realsense_test():
    def __init__(self):
        self.config = rs.config()
        self.config.enable_stream(rs.stream.infrared, 1, *settings.V_SIZE, rs.format.y8, settings.FPS)
        self.config.enable_stream(rs.stream.depth, *settings.V_SIZE, rs.format.z16, settings.FPS)
        self.config.enable_stream(rs.stream.color, *settings.V_SIZE, rs.format.bgr8, settings.FPS)

    def rec(self, settings):
        self.config.enable_record_to_file(settings.FULL_NAME)

        pipeline = rs.pipeline()
        pipeline.start(self.config)
        start = time.time()
        frame_no = 1
        try:
            while True:
                frames = pipeline.wait_for_frames()
                color_frame = frames.get_color_frame()
                ir_frame = frames.get_infrared_frame()

                if frame_no%settings.FPS == 0:
                    fps  = settings.FPS / (time.time() - start)
                    start = time.time()
                    print(f'FPS: {fps}')
                frame_no += 1

                if not ir_frame or not color_frame:
                    ir_image = np.asanyarray(ir_frame.get_data())
                    color_image = np.asanyarray(color_frame.get_data())
        except Exception as e:
            print(e)
        finally:    
            pipeline.stop()

    def live(self, settings):
        pipeline = rs.pipeline()
        self._pw(pipeline)

    def play(self, settings):
        self.config.enable_device_from_file(settings.FULL_NAME)

        pipeline = rs.pipeline()
        profile = pipeline.start(self.config)
        self._pw(pipeline)

    def _pw(self, pipeline):
        ''' フレームの表示 '''
        try:
            while True:
                frames = pipeline.wait_for_frames()
                ir_frame = frames.get_infrared_frame()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                if not depth_frame or not color_frame or not ir_frame:
                    continue

                ir_image = np.asanyarray(ir_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())

                cv2.namedWindow('ir_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('ir_image', self._heat(ir_image))
                cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('color_image', color_image)
                cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('depth_image', self._heat(depth_image))
                cv2.waitKey(1)
        except Exception as e:
            print(e)
        finally:
            pipeline.stop()

    def _heat(self, np_img):
        ''' ヒートマップに変換 '''
        if not settings.heatmap: return
        return cv2.applyColorMap(
            cv2.convertScaleAbs(np_img, alpha=0.3),
            cv2.COLORMAP_JET,
        )
        # heatmap = None
        # heatmap = cv2.normalize(
        #     np_img,
        #     heatmap,
        #     alpha=0,
        #     beta=255,
        #     norm_type=cv2.NORM_MINMAX,
        #     dtype=cv2.CV_8U)
        # heatmap = cv2.applyColorMap(heatmap, cv2.COLORMAP_JET)
        # return heatmap

if __name__ == "__main__":
    settings = Settings()
    tester = Realsense_test()
    if len(sys.argv) >= 2:
        opt = str(sys.argv[1])
        if opt == 'rec':
            tester.rec(settings)
        elif opt == 'live':
            tester.live(settings)
        else:
            tester.play(settings)
    else:
        print(f'----- option -----\nrecode: py main.py rec\nlive  : py main.py live\nplay  : py main.py play')
