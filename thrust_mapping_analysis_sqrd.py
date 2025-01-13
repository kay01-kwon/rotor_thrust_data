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


def custom_poly(rpm, C_t):
    return C_t * rpm**2

if __name__ == '__main__':

    directory = 'bag/rotor_test_24_6C/thrust_rpm'

    dir_str_len = len(directory)

    file_names = find_files(directory)

    g = 9.81

    # Sorting file name list
    file_names.sort()
    sorted_file_names = sorted(file_names)

    # Get the number of bag files
    num_files = len(file_names)

    # Storage for the average of rpm and torque
    actual_rpm_avg = np.zeros(num_files)
    thrust_avg = np.zeros(num_files)

    i = 0
    for file_name in sorted_file_names:
        print(file_name)
        torque_dict = []
        actual_rpm_dict = []
        weight_dict, actual_rpm_dict = get_data(directory + '/' + file_name)

        # Get average rpm and torque
        actual_rpm_avg[i] = np.sum(actual_rpm_dict['actual_rpm'])/len(actual_rpm_dict['actual_rpm'])
        thrust_avg[i] = np.sum(weight_dict['load_cell_weight'])/len(weight_dict['load_cell_weight'])*g
        i = i + 1

    print('RPM avg: ', actual_rpm_avg)
    print('Thrust avg: ', thrust_avg, 'N')

    # Initial guess for the C_m parameter
    initial_guess = 1e-9

    param_opt, param_cov = curve_fit(custom_poly,
                                     actual_rpm_avg,
                                     thrust_avg,
                                     p0=initial_guess,
                                     method='lm')

    print('************ Thrust mapping result ************')
    print('The optimal of thrust of coefficient is : ', param_opt)
    print('The variance between predicted thrust and thrust data is : ', param_cov)

    test_rpm = np.linspace(2000,8000, 10)
    test_thrust = param_opt * test_rpm**2

    plt.plot(actual_rpm_avg, thrust_avg, "*", label="Raw data")
    plt.plot(test_rpm, test_thrust, label="Predicted thrust")
    plt.legend(loc='best')
    plt.title("Thrust - Rotor speed (24.6°C)")
    plt.xlabel("Rotor speed (RPM)")
    plt.ylabel("Thrust (N)")
    plt.grid(True)
    plt.savefig('thrust_mapping.png',dpi=600)