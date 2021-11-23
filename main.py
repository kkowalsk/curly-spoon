#
# todo
#

import sys
import time
from goprocam import GoProCamera, constants

# constants
AP_MAC_KEY = 'ap_mac'
AP_MAC_VALUE = None

# globals
GOPRO_CAM = None

def init_camera():
    global GOPRO_CAM
    GOPRO_CAM = GoProCamera.GoPro(mac_address='AA:BB:CC:DD:EE:FF') # the default mac address is fine but for documentation purposes init with
    GOPRO_CAM.power_on()
    print("...")
    info = GOPRO_CAM.infoCamera()
    AP_MAC_VALUE = info[AP_MAC_KEY]
    print("...")


def main():
    try:
        init_camera()
    except KeyboardInterrupt:
        print("Closing")
    except:
        pass
    finally:
        GOPRO_CAM.power_off()
        sys.exit()

if __name__ == "__main__":
    main()