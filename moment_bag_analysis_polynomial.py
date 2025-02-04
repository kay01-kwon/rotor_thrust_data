import os, fnmatch
import rosbag
import numpy as np
import matplotlib.pyplot as plt
from scipy.optimize import curve_fit

def find_files(directory):
    file_names = []

    for root, dirs, files in os.walk(directory):
        for name in files:
            if fnmatch.fnmatch(name, '*.bag'):
                file_names.append(name)
                # print(directory+'/'+name)

    return file_names

def extract_string(file_name):
    return int(file_name.split('RPM')[0])

def get_data(file_name):
    bag = rosbag.Bag(file_name)

    # Load cell data to store
    load_cell_time = []
    load_cell_time_secs = []
    load_cell_time_nsecs = []
    load_cell_moment_data = []

    for idx, (topic, msg, time) in enumerate(bag.read_messages(topics=['/loadcell/torque'])):
        time.to_time()
        load_cell_time.append(time)
        load_cell_time_secs.append(msg.stamp.secs)
        load_cell_time_nsecs.append(msg.stamp.nsecs)
        load_cell_moment_data.append(-msg.torque)

    load_cell_dict = {'load_cell_secs': load_cell_time_secs,
                      'load_cell_nsecs': load_cell_time_nsecs,
                      'load_cell_moment': load_cell_moment_data}

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

    return load_cell_dict, actual_rpm_dict


def custom_poly(rpm, a, b, c):
    return a * rpm**2 + b * rpm + c

if __name__ == '__main__':

    directory = 'bag/rotor_test_24_6C/moment_rpm'

    dir_str_len = len(directory)

    file_names = find_files(directory)


    # Sorting file name list
    file_names.sort()
    sorted_file_names = sorted(file_names)

    # Get the number of bag files
    num_files = len(file_names)

    # Storage for the average of rpm and torque
    actual_rpm_avg = np.zeros(num_files)
    torque_avg = np.zeros(num_files)

    i = 0
    for file_name in sorted_file_names:
        print(file_name)
        torque_dict = []
        actual_rpm_dict = []
        torque_dict, actual_rpm_dict = get_data(directory + '/' + file_name)

        # Get average rpm and torque
        actual_rpm_avg[i] = np.sum(actual_rpm_dict['actual_rpm'])/len(actual_rpm_dict['actual_rpm'])
        torque_avg[i] = np.sum(torque_dict['load_cell_moment'])/len(torque_dict['load_cell_moment'])
        i = i + 1

    print('RPM avg: ', actual_rpm_avg)
    print('Moment avg: ', torque_avg)

    # Initial guess for the C_m parameter
    initial_guess = [1, 1, 1]

    param_opt, param_cov = curve_fit(custom_poly,
                                     actual_rpm_avg,
                                     torque_avg,
                                     p0=initial_guess,
                                     method='lm')

    print('The optimal of moment of coefficient is : ', param_opt)
    print('The covariance of moment is : ', param_cov)

    test_rpm = np.linspace(2000,7600, 10)
    test_torque = param_opt[0] * test_rpm**2 + param_opt[1] * test_rpm + param_opt[2]

    plt.plot(actual_rpm_avg, torque_avg, "*", label="Raw data")
    plt.plot(test_rpm, test_torque, label="Regression")
    plt.legend(loc='best')
    plt.title("Moment - Rotor speed (24.6°C)")
    plt.xlabel("Rotor speed (RPM)")
    plt.ylabel("Moment (Nm)")
    plt.grid(True)
    plt.show()