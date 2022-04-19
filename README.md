# Realsense_test
realsense test

## quick start (amd64)
0. clone this repo
   ```
   git clone https://github.com/Fukuda-B/Realsense_test.git
   cd Realsense
   ```
1. create Virtual environment
   ```
   $env:PIPENV_VENV_IN_PROJECT = "true" (for Windows)
   export PIPENV_VENV_IN_PROJECT="true" (for Linux)
   ```
2. run shell (require python 3.9)
   ```
   pipenv install
   ```
3. start script
   ```
   pipenv run rec
   pipenv run play
   pipenv run live
   ```

## raspberry pi 4 (arm Architecture)
1. raspberry pi imager flash to ubuntu server 20.04 LTS
2. boot raspberry pi 4
3. set ntp server (chenge to academic ntp) cf. ntp.akita-pu.ac.jp
4. install GUI
   ```
   sudo apt update && sudo apt upgrade
   sudo apt install ubuntu-desktop
   ```
5. build librealsense and add path
   ```
   git clone https://github.com/IntelRealSense/librealsense
   cd librealsense
   sudo apt install git libssl-dev libusb-1.0-0-dev pkg-config libgtk-3-dev
   sudo apt install libglfw3-dev libgl1-mesa-dev libglu1-mesa-dev cmake
   ./scripts/setup_udev_rules.sh
   ./scripts/patch-realsense-ubuntu-lts.sh
   mkdir build && cd build
   cmake ../ -DBUILD_PYTHON_BINDINGS=true # python include
   sudo make clean && make && sudo make install # about 1 hour
   ls /usr/lib/python3/dist-packages/pyrealsense2/
   export PYTHONPATH=$PYTHONPATH:/usr/lib/python3/dist-packages/pyrealsense2/
   ```
6. clone this repo
7. install opencv-python and numpy
8. start script
   ```
   python3 main.py live
   ```