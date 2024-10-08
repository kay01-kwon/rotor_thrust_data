import os, fnmatch
import rosbag
from load_cell_msg.msg import weight_msg
from ros_libcanard.msg import cmd_raw
from ros_libcanard.msg import actual_rpm
import numpy as np
import scipy.io

def find_files(directory):
    file_names = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            if fnmatch.fnmatch(name, '*.bag'):
                file_names.append(directory + '/' + name)
                print(directory+'/'+name)

    return file_names

def get_data(file_name):
    bag = rosbag.Bag(file_name)

    # Load cell data to store
    load_cell_time = []
    load_cell_time_secs = []
    load_cell_time_nsecs = []
    load_cell_weight_data = []

    for idx, (topic, msg, time) in enumerate(bag.read_messages(topics=['/loadcell/weight'])):
        time.to_time()
        load_cell_time.append(time)
        load_cell_time_secs.append(msg.stamp.secs)
        load_cell_time_nsecs.append(msg.stamp.nsecs)
        load_cell_weight_data.append(msg.weight)

    load_cell_dict = {'load_cell_secs': load_cell_time_secs,
                      'load_cell_nsecs': load_cell_time_nsecs,
                      'load_cell_weight': load_cell_weight_data}

    # ESC cmd_raw data to store
    cmd_raw_time = []
    cmd_raw_secs = []
    cmd_raw_nsecs = []
    cmd_raw_data = []

    for topic, msg, time in bag.read_messages(topics = ['/cmd_raw']):
        cmd_raw_time.append(time.to_time())
        cmd_raw_secs.append(msg.stamp.secs)
        cmd_raw_nsecs.append(msg.stamp.nsecs)
        cmd_raw_data.append(msg.raw)

    cmd_raw_dict = {'cmd_raw_secs': cmd_raw_secs,
                    'cmd_raw_nsecs': cmd_raw_nsecs,
                    'cmd_raw_data': cmd_raw_data}

    # ESC Actual rpm data to store
    actual_rpm_time = []
    actual_rpm_secs = []
    actual_rpm_nsecs = []
    actual_rpm_data = []

    for topic, msg, time in bag.read_messages(topics=['/actual_rpm']):
        actual_rpm_time.append(time.to_time())
        actual_rpm_secs.append(msg.stamp.secs)
        actual_rpm_nsecs.append(msg.stamp.nsecs)
        actual_rpm_data.append(msg.rpm)

    actual_rpm_dict = {'actual_rpm_secs': actual_rpm_secs,
                       'actual_rpm_nsecs': actual_rpm_nsecs,
                       'actual_rpm': actual_rpm_data}

    bag.close()

    return load_cell_dict, cmd_raw_dict, actual_rpm_dict


if __name__ == '__main__':

    directory = 'thrust_bag'

    dir_str_len = len(directory)

    mat_folder_directory = directory + '/' + 'mat_folder'

    file_names = find_files(directory)

    # os.mkdir(mat_folder_directory)

    for file_name in file_names:
        load_cell_dict = []
        cmd_raw_dict = []
        actual_rpm_dict = []
        load_cell_dict, cmd_raw_dict, actual_rpm_dict = get_data(file_name)
        bag_name = file_name.replace(directory, '')
        bag_name = bag_name.replace('.bag', '')
        mat = scipy.io.savemat(mat_folder_directory + '/' + bag_name + '.mat',
                               {'dict_array': [load_cell_dict,
                                actual_rpm_dict,
                                cmd_raw_dict]})
