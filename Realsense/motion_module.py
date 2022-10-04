# https://github.com/IntelRealSense/librealsense/issues/3409

import pyrealsense2 as rs
import numpy as np
import time
import matplotlib.pyplot as plt

def initialize_camera():
    # start the frames pipe
    p = rs.pipeline()
    conf = rs.config()
    conf.enable_stream(rs.stream.accel)
    conf.enable_stream(rs.stream.gyro)
    prof = p.start(conf)
    return p

def gyro_data(gyro):
    return np.asarray([gyro.x, gyro.y, gyro.z])

def accel_data(accel):
    return np.asarray([accel.x, accel.y, accel.z])

p = initialize_camera()

dt_start = time.perf_counter() # 処理開始時間
dt = dt_start # 1回あたりの処理時間
data_arr = [[0], [0], [0], [0], [0], [0], [0]] # 経過時間, x角度, y角度, z角度, x移動, y移動, z移動
try:
    while True:
        f = p.wait_for_frames()
        accel = accel_data(f[0].as_motion_frame().get_motion_data())
        gyro = gyro_data(f[1].as_motion_frame().get_motion_data())
        dt_n = time.perf_counter()
        df = dt_n - dt
        data_arr[0].append(dt_n-dt_start)   # 経過時間
        data_arr[1].append(gyro[0]*df)      # x角度
        data_arr[2].append(gyro[1]*df)      # y角度
        data_arr[3].append(gyro[2]*df)      # z角度
        data_arr[4].append(accel[0]*df)     # x移動
        data_arr[5].append(accel[1]*df)     # y移動
        data_arr[6].append(accel[2]*df)     # z移動
        dt = dt_n
        print("accelerometer: ", accel)
        print("gyro: ", gyro)
except Exception as e: print(e)
finally:
    p.stop()
    # print(len(data_arr[0]))
    # print(data_arr[0])

    fig = plt.figure(figsize=(12, 6))
    ax1 = fig.add_subplot(121)
    ax1.plot(data_arr[0], data_arr[1], label="roll")
    ax1.plot(data_arr[0], data_arr[2], label="pitch")
    ax1.plot(data_arr[0], data_arr[3], label="yaw")
    ax1.set_xlabel('t (s)')

    ax2 = fig.add_subplot(122)
    ax2.plot(data_arr[0], data_arr[4], label="x pos")
    ax2.plot(data_arr[0], data_arr[5], label="y pos")
    ax2.plot(data_arr[0], data_arr[6], label="z pos")
    ax2.set_xlabel('t (s)')
    plt.legend()
    plt.show()
