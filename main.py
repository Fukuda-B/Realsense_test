'''
    Realsenseの動作テスト

    録画: py main.py rec
    再生: py main.py play
  ライブ: py main.py live

    -----

    Realsense D400-Series,
        https://www.mouser.com/pdfdocs/Intel_D400_Series_Datasheet.pdf,
        https://store.intelrealsense.com/buy-intel-realsense-depth-camera-d435.html,

    librealsense example, 
        https://dev.intelrealsense.com/docs/python2,
        https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/python-tutorial-1-depth.py,
        https://github.com/IntelRealSense/librealsense/blob/master/wrappers/python/examples/opencv_viewer_example.py,

    filtering depth image, https://qiita.com/keoitate/items/efe4212b0074e10378ec#%E5%BE%8C%E5%87%A6%E7%90%86%E3%82%92%E3%81%99%E3%82%8B
'''

import os
import sys
import cv2
import time
import numpy as np
import pyrealsense2 as rs

class Settings():
    def __init__(self):
        # ----- 映像設定
        self.V_SIZE_RGB = (640, 480)    # RGB 画面サイズ
        self.V_SIZE_D = (1280, 720)     # Depth 画面サイズ (USB 3)
        self.FPS = 30                   # フレームレート
        self.HEATMAP = False            # ヒートマップ表示
        self.NOISE_FILTER = False       # ノイズフィルタ

        # ----- BAGファイル保存ディレクトリ
        self.F_NAME = 'realsense_b.bag' # ファイル名
        desktop = os.path.expanduser('~/Desktop')
        self.FULL_NAME = os.path.join(desktop, self.F_NAME)

        # ----- 画像での保存
        self.WRITE_IMG = True          # 保存するか
        self.WRITE_DIR = 'tmp'         # 保存するディレクトリ

        # ----- フィルタ設定
        self.decimate = rs.decimation_filter()
        self.decimate.set_option(rs.option.filter_magnitude, 1)
        self.spatial = rs.spatial_filter()
        self.spatial.set_option(rs.option.filter_magnitude, 1)
        self.spatial.set_option(rs.option.filter_smooth_alpha, 0.25)
        self.spatial.set_option(rs.option.filter_smooth_delta, 50)
        self.hole_filling = rs.hole_filling_filter()
        self.depth_to_disparity = rs.disparity_transform(True)
        self.disparity_to_depth = rs.disparity_transform(False)

class Realsense_test():
    def __init__(self):
        self.config = rs.config()
        # self.config.enable_stream(rs.stream.infrared, 1, *settings.V_SIZE, rs.format.y8, settings.FPS)
        self.config.enable_stream(rs.stream.depth, *settings.V_SIZE_D, rs.format.z16, settings.FPS)
        self.config.enable_stream(rs.stream.color, *settings.V_SIZE_RGB, rs.format.bgr8, settings.FPS)

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
                # ir_frame = frames.get_infrared_frame()

                if frame_no%settings.FPS == 0:
                    fps  = settings.FPS / (time.time() - start)
                    start = time.time()
                    print(f'FPS: {fps}')
                frame_no += 1

                # if not ir_frame or not color_frame:
                #     ir_image = np.asanyarray(ir_frame.get_data())
                #     color_image = np.asanyarray(color_frame.get_data())
        except Exception as e:
            print(e)
        finally:    
            pipeline.stop()

    def live(self, settings):
        ''' カメラのデータをリアルタイムで表示 '''
        pipeline = rs.pipeline()
        profile = pipeline.start(self.config)
        self._pw(pipeline)

    def play(self, settings):
        ''' 録画したデータの再生 '''
        self.config.enable_device_from_file(settings.FULL_NAME)
        pipeline = rs.pipeline()
        profile = pipeline.start(self.config)
        self._pw(pipeline)

    def _pw(self, pipeline):
        ''' フレームの表示 '''
        try:
            start = time.time()
            frame_no = 0
            while True:
                # ----- 画像取得
                frames = pipeline.wait_for_frames()
                depth_frame = frames.get_depth_frame()
                color_frame = frames.get_color_frame()
                # ir_frame = frames.get_infrared_frame()
                # if not depth_frame or not color_frame or not ir_frame:
                if not depth_frame or not color_frame:
                    continue
                # ir_image = np.asanyarray(ir_frame.get_data())
                depth_image = np.asanyarray(depth_frame.get_data())
                color_image = np.asanyarray(color_frame.get_data())
                depth_colormap = cv2.applyColorMap(cv2.convertScaleAbs(depth_image, alpha=0.08), cv2.COLORMAP_JET)

                # ----- FPS 計算
                if frame_no%settings.FPS == 0:
                    fps  = settings.FPS / (time.time() - start)
                    start = time.time()
                    print(f'FPS: {fps}')
                frame_no += 1


                # ----- 深度カメラのノイズ除去
                if settings.NOISE_FILTER:
                    ff = settings.decimate.process(depth_image)
                    ff = settings.depth_to_disparity.process(ff)
                    ff = settings.spatial.process(ff)
                    ff = settings.disparity_to_depth.process(ff)
                    ff = settings.hole_filling.process(ff)
                    depth_image = ff.as_depth_frame()

                # ----- 表示
                # cv2.namedWindow('ir_image', cv2.WINDOW_AUTOSIZE)
                # cv2.imshow('ir_image', self._heat(ir_image))
                cv2.namedWindow('color_image', cv2.WINDOW_AUTOSIZE)
                cv2.imshow('color_image', color_image)
                cv2.namedWindow('depth_image', cv2.WINDOW_AUTOSIZE)
                depth_colormap = depth_colormap[120:620, 150:960]
                cv2.imshow('depth_image', depth_colormap)
                # cv2.imshow('depth_image', self._heat(depth_image))

                if settings.WRITE_IMG:
                    cv2.imwrite(f'{settings.WRITE_DIR}/color_{frame_no}.png', color_image)
                    cv2.imwrite(f'{settings.WRITE_DIR}/depth_{frame_no}.png', depth_colormap)

                if cv2.waitKey(1) &0xff == 27:
                    cv2.destroyAllWindows()
                    break
        except Exception as e:
            print(e)
        finally:
            pipeline.stop()

    def _heat(self, np_img):
        ''' ヒートマップに変換 '''
        if not settings.HEATMAP: return np_img
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
