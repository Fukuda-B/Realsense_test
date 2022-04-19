import cv2
import RPi.GPIO as GPIO
import numpy as np
import pyrealsense2 as rs
import os
import sys
import time
import datetime

LED_GPIO = 4
TACT_GPIO = 17

GPIO.setmode(GPIO.BCM)
GPIO.setup(LED_GPIO, GPIO.OUT)
GPIO.setup(TACT_GPIO, GPIO.IN)

# ----- LED test
GPIO.output(LED_GPIO, GPIO.HIGH)
time.sleep(1.0)
GPIO.output(LED_GPIO, GPIO.LOW)

# ----- Realsense class
class _realsense():
    def __init__(self):
        self.save_dir = '/media/realsense/CA78AC5478AC40D5/Realsense_rec' # save dir
        self.video_size = (1280, 720) # video size
        self.fps = 30                 # frame rate
        self.config = rs.config()
        self.config.enable_stream(rs.stream.infrared, 1, *self.video_size, rs.format.y8, self.fps)
        self.config.enable_stream(rs.stream.depth, *self.video_size, rs.format.z16, self.fps)
        self.config.enable_stream(rs.stream.color, *self.video_size, rs.format.rgb8, self.fps)
        os.makedirs(self.save_dir, exist_ok=True)

    def recode(self):
        dt = datetime.datetime.now()
        filename = '/recorded_' + dt.strftime('%Y%m%d_%H%M%S') + '.bag' # file name
        self.config.enable_record_to_file(self.save_dir+filename)
        self.pipeline = rs.pipeline()
        self.pipeline.start(self.config)
        self.frame_no = 1
        while True:
            frames = self.pipeline.wait_for_frames()
            color_frame = frames.get_color_frame()
            ir_frame = frames.get_infrared_frame()
            self.frame_no += 1
            if not ir_frame or not color_frame:
                ir_image = np.asanyarray(ir_frame .get_data())
                color_image = np.asanyarray(color_frame.get_data())
            if GPIO.input(TACT_GPIO) == GPIO.HIGH:
                GPIO.output(LED_GPIO, GPIO.LOW)
                break

    def stop(self):
        self.pipeline.stop()

# ----- Timer class
class _timer():
    def __init__(self):
        self.quit_intv = 3 # hold recognition time (s)
        self.b_push = False
        self.cnt = 0

    def _diff_t(self):
        self.cnt += 1
        if not self.b_push: # first exec
            self.b_push = datetime.datetime.now()
            return False
        return (datetime.datetime.now()-self.b_push).seconds > self.quit_intv

# ----- main function
def main():
    ex_flag = False
    while True:
        print('--- start program ---')
        tt = _timer()
        if ex_flag: break
        while True:
            if ex_flag: break
            if GPIO.input(TACT_GPIO) == GPIO.HIGH:
                if tt._diff_t():    # hold button
                    for i in range(6):
                        GPIO.output(LED_GPIO, GPIO.LOW if i%2==0 else GPIO.HIGH)
                        time.sleep(0.1)
                    GPIO.cleanup()
                    print('--- stop program ---')
                    ex_flag = True
            elif tt.cnt > 0: break  # push button

        print('--- start recoding ---')
        GPIO.output(LED_GPIO, GPIO.HIGH)
        rs_mod = _realsense()
        rs_mod.recode()

        print('--- stop recoding ---')
        rs_mod.stop()

if __name__ == '__main__':
    main()
