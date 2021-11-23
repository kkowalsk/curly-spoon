#
# todo
#

import sys
import time
import traceback
from typing import Annotated, TypeVar
from goprocam import GoProCamera, constants

# constants
AP_MAC_KEY = 'ap_mac'
AP_MAC_VALUE = None

# globals
DEBUG = True
GOPRO_CAM = Annotated[GoProCamera.GoPro, 'global GoPro camera handle']  #TypeVar('GOPRO_CAM', GoProCamera.GoPro, None)

def init_camera():
    global GOPRO_CAM
    GOPRO_CAM = GoProCamera.GoPro(mac_address='AA:BB:CC:DD:EE:FF') # the default mac address is fine but for documentation purposes init with
    GOPRO_CAM.power_on()
    print("...")
    info = GOPRO_CAM.infoCamera()
    AP_MAC_VALUE = info[AP_MAC_KEY]
    print("...")

def is_camera_ready():
    return GOPRO_CAM != None

def start_video_capture():
    GOPRO_CAM.shoot_video()
    if DEBUG:
        print("is recording {}".format(GOPRO_CAM.IsRecording()))
        sys.stdout.flush()

def end_video_capture():
    GOPRO_CAM.shutter(constants.stop)
    time.sleep(3)
    if DEBUG:
        print("is recording {}".format(GOPRO_CAM.IsRecording()))
        sys.stdout.flush()

def download_last_video():
    GOPRO_CAM.downloadLastMedia(custom_filename="download_test.mp4") # will override existing filenames

def video_test():
    init_camera()
    if is_camera_ready():
        start_video_capture()
        time.sleep(5)
        end_video_capture()
        download_last_video()

def main():
    try:
        video_test()
    except KeyboardInterrupt:
        print("Closing")
    except:
        print(traceback.format_exc())
    finally:
        if is_camera_ready:
            GOPRO_CAM.power_off()
        sys.exit()

if __name__ == "__main__":
    main()