import os
from collections import namedtuple

def get_filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames

def get_directory_list(directory):
    directories = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directories.append(directory)
    return directories

def remove_missing_data(actual_list, perceived_list, subject_ID, name):
    indices_to_remove = []
    for trial in perceived_list:
        if trial == "":
            indices_to_remove.append(perceived_list.index(trial))
            print(f'missing data at index {perceived_list.index(trial)}, {subject_ID}, condition {name}')
    indices_to_remove.reverse()
    for index in indices_to_remove:
        actual_list.pop(index)
        perceived_list.pop(index)
        print(f'removed missing data at index {index}, {subject_ID}, condition {name}')
    return actual_list, perceived_list

def condition_plot_inputs(subject_data):
    plot_inputs = namedtuple('INPUTS', 'NAME ACTUAL PERCEIVED PLOT_INDEX')
    line_width_inputs = plot_inputs(NAME='SHow Line Pick Width', ACTUAL=subject_data.LINE_WIDTH.ACTUAL,
                                    PERCEIVED=subject_data.LINE_WIDTH.PERCEIVED, PLOT_INDEX=1)
    width_line_inputs = plot_inputs(NAME='Present Width Pick Line', ACTUAL=subject_data.WIDTH_LINE.ACTUAL,
                                    PERCEIVED=subject_data.WIDTH_LINE.PERCEIVED, PLOT_INDEX=2)
    width_width_inputs = plot_inputs(NAME='Present Width Pick Width', ACTUAL=subject_data.WIDTH_WIDTH.ACTUAL,
                                    PERCEIVED=subject_data.WIDTH_WIDTH.PERCEIVED, PLOT_INDEX=3)
    tuples = line_width_inputs, width_line_inputs, width_width_inputs
    return tuples