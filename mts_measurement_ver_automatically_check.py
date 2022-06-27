import py7zr
import os
from os import listdir
from os.path import isfile, join
import shutil
from cartica_utilities.utilities import os_utilities
# import subprocess

"""
Agenda - 
    to check a recc file for errors using diffrent mts_measurement versions that
    stored in folder as 7z format, automatically. 
notes:
    * Folder "mypath" shall contain only 7z files 
    * first delete mts_measurement from origin because delete function does now work onb windows 
    * use extractor_vers2.cfg configuration
what it does:
    1. extract new mts_measurement from 7z file
    2. Run MTS session
    3. cut new files to the new MTS session.
"""

mts_measurement_7z_folder = r'C:\MTS_TEST_SCRIPT\MTS_MEAS_VER' #folder with all mts_measurement as 7z format
mts_measurement_original_path = r'C:\MFC520_Cartex\06_Deliverables\MTS' #location of the mts_measurement folder
CONFIG_PATH = r"C:\MTS_TEST_SCRIPT\extractor_vers2.cfg"
recording_path = r"C:\MTS_TEST_SCRIPT\2022.06.07_at_20.48.26_camera-mi_804_truck_with_trailer.rrec"
MTS_DIR = r"C:\CARTICA\MTS_21"

mts_path = os.path.join(MTS_DIR, "MTS", "mts_system", "measapp.exe")
MTS_CMD = [mts_path, f"-lc{CONFIG_PATH}", f"-lr{recording_path}", "-pal", "-eab", "-silent", "-eoe"]

#get 7z file name from directory:
onlyfiles = [f for f in listdir(mts_measurement_7z_folder) if isfile(join(mts_measurement_7z_folder, f))]
print("fileslist" , onlyfiles)

# Delete current folder and extrtact 7z files
for onlyfile in onlyfiles:
    # extract new files:
    my_path_file = mts_measurement_7z_folder + '\\' + onlyfile
    print("debug:*********** my_path_file:", my_path_file)
    print("current:", my_path_file)
    with py7zr.SevenZipFile(my_path_file,mode='r') as z:
        z.extractall(mts_measurement_original_path )
    #run MTS session
    os_utilities.run_cmd(MTS_CMD)
    #cut current folder after script finishes:
    source_dir = mts_measurement_original_path + '\\' + 'mts_measurement'
    destination_dir = os.path.splitext ( mts_measurement_7z_folder+ '\\' + onlyfile)[0] + 'copy'
    print("destination_dir", destination_dir)
    shutil.move(source_dir, destination_dir)











