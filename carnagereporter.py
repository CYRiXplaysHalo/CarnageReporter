from os import listdir
from os.path import isfile, join
from os import getenv
import time
import datetime
from shutil import copyfile
import os.path, time

def getModifiedTimes(mcc_temp_path, fileList, fileModifiedList):
    for file in fileList:
        fileModifiedList.append(time.ctime(os.path.getmtime(mcc_temp_path + "\\" + file)))

output_path = r"D:\\MCCStats\\"
app_data_path = getenv('APPDATA')
mcc_temp_path = app_data_path.replace('Roaming','LocalLow') + r'\MCC\Temporary'
prev_files = [f for f in listdir(mcc_temp_path) if (isfile(join(mcc_temp_path, f)) and f.endswith('.xml'))]
prev_files_modified_times = []
getModifiedTimes(mcc_temp_path, prev_files, prev_files_modified_times)

print("MCC Carnage Reporter running.")
while(True):
    files = [f for f in listdir(mcc_temp_path) if isfile(join(mcc_temp_path, f))]
    files_modified_times = []
    getModifiedTimes(mcc_temp_path, files, files_modified_times)
    if prev_files_modified_times != files_modified_times:
        print("New file(s) found at " + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S'))
        #print(files)
        for file in files:
            try:
                copyfile(mcc_temp_path + "\\" + file, output_path + datetime.datetime.now().strftime('%Y-%m-%d-%H-%M-%S') + "-" + file)
            except:
                print("Error saving file.")
    prev_files = files
    prev_files_modified_times = files_modified_times
    time.sleep(60)
