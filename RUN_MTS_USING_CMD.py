import os
import shutil

from cartica_utilities.utilities import os_utilities

CONFIG_PATH = r"C:\MTS_TEST_SCRIPT\recording_validator.cfg"
recording_path = r"C:\MTS_TEST_SCRIPT\2022.06.07_at_20.48.26_camera-mi_804_truck_with_trailer.rrec"
measapp_path = r"C:\MFC520_Cartex\MTS\05_Testing\MTS\mts_system\measapp.exe"
log_dir = r"C:\MFC520_Cartex\MTS\05_Testing\MTS\mts_measurement\log"

os_utilities.delete_path(log_dir)
MTS_CMD = [measapp_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent", "-eoe"]
os_utilities.run_cmd(MTS_CMD)


