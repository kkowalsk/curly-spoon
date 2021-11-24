#
# todo
#

import os
import sys
import time
import typing
import traceback
import subprocess

from goprocam import GoProCamera, constants

# constants
AP_MAC_KEY = 'ap_mac'
GOPRO_WIFI_SSID = 'go_dg_pro'

# globals
DEBUG = True
IS_CAMERA_CONNECTED = False
AP_MAC_VALUE = None
GOPRO_CAM = typing.Annotated[GoProCamera.GoPro, 'global GoPro camera handle']

def show_usage():
    print("usage:\n{} [-h || --help]".format(os.path.basename(__file__)))

def is_connected_gopro_wifi():
    result = subprocess.check_output(['netsh', 'wlan', 'show', 'interfaces'])
    return GOPRO_WIFI_SSID in str(result)

def connect_gopro_wifi():
    if not is_connected_gopro_wifi():
        if DEBUG:
            print("connecting to SSID {}".format(GOPRO_WIFI_SSID))
        result = os.system('cmd /c \"netsh wlan connect name={}\"'.format(GOPRO_WIFI_SSID))
        if DEBUG:
            print("netsh result: {}".format(result))
            sys.stdout.flush()
        time.sleep(3)
    else:
        if DEBUG:
            print("already connected to gopro wifi")

def open_camera_connection():
    global GOPRO_CAM, IS_CAMERA_CONNECTED, AP_MAC_VALUE

    GOPRO_CAM = GoProCamera.GoPro(mac_address='AA:BB:CC:DD:EE:FF') # the default mac address is fine but for documentation purposes init with
    GOPRO_CAM.power_on()
    IS_CAMERA_CONNECTED = True
    print("...")
    info = GOPRO_CAM.infoCamera()
    AP_MAC_VALUE = info[AP_MAC_KEY]
    print("...")

def close_camera_connection():
    global IS_CAMERA_CONNECTED
    GOPRO_CAM.power_off()
    IS_CAMERA_CONNECTED = False

def is_camera_ready():
    return IS_CAMERA_CONNECTED

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
    connect_gopro_wifi()
    open_camera_connection()
    if is_camera_ready():
        start_video_capture()
        time.sleep(5)
        end_video_capture()
        download_last_video()

def main(argv):
    if len(argv) == 2 and ( argv[1] == '-h' or argv == '--help' ):
        show_usage()
    else:
        try:
            video_test()
        except KeyboardInterrupt:
            print("Closing")
        except:
            print(traceback.format_exc())
        finally:
            pass

    program_exit()

def program_exit():
    if is_camera_ready():
        close_camera_connection()
    sys.exit()

if __name__ == "__main__":
    main(sys.argv)