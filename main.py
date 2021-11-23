
AP_MAC_KEY = 'ap_mac'
AP_MAC_VALUE = None

from goprocam import GoProCamera, constants
import time
gpCam = GoProCamera.GoPro(mac_address='AA:BB:CC:DD:EE:FF') # the default mac address is fine but for documentation purposes init with
gpCam.power_on()
print("...")
info = gpCam.infoCamera()
AP_MAC_VALUE = info[AP_MAC_KEY]
print("...")
gpCam.power_off()
