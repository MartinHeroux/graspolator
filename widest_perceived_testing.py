import matplotlib.pyplot as plt
from random import random
from pathlib import Path
import numpy as np

import utils


def plot_regression_widest_perceived(subject_IDs, all_subject_data, widest_lines):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    subplot_indices = [1, 2, 3, 4]

    indices_to_pop = indices_subjects_without_10(subject_IDs, all_subject_data, widest_lines)

    d1_dom_at_10, d1_non_dom_at_10, d2_dom_1_at_10, d2_dom_2_at_10 = values_at_10(all_subject_data)

    for index in indices_to_pop:
        d1_dom_at_10.pop(index)
        d1_non_dom_at_10.pop(index)
        d2_dom_1_at_10.pop(index)
        d2_dom_2_at_10.pop(index)
        widest_lines.pop(index)

    widest_lines_int = [int(str_value) for str_value in widest_lines]

    lengths_list = [len(d1_dom_at_10), len(d1_non_dom_at_10), len(d2_dom_1_at_10), len(d2_dom_2_at_10), len(widest_lines)]
    for item in lengths_list:
        if item is not (len(subject_IDs) - len(indices_to_pop)):
            print('error in popping values, uneven lists, exiting')
            exit()
        else:
            print('list length correct, continuing')

    values_at_10_lists = d1_dom_at_10, d1_non_dom_at_10, d2_dom_1_at_10, d2_dom_2_at_10

    plt.figure(figsize=(15, 5))
    plt.suptitle(str('Widest Grasp vs Perceived Grasp Width at 10cm Regressions'))

    for subplot_index, condition_values, condition_name in zip(subplot_indices, values_at_10_lists, condition_names):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_values)
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_values) + np.array(random_values)
        plt.plot(x_data, widest_lines, 'o', alpha=0.5, color='royalblue')
        #condition_values_float = ([condition_values], np.dtype('float'))
        if len(condition_values) is not len(widest_lines):
            print("unequal lists for regression, exiting")
            exit()

        intercept, slope = utils.calculate_regression_general(condition_values, widest_lines_int)

        x2 = 2
        x10 = 10
        y2 = slope * x2 + intercept
        y10 = slope * x10 + intercept
        plt.plot([x2, x10], [y2, y10], color='royalblue')
        plt.title(condition_name, loc='right')

    path = Path('./plots/group_plots/widest_line_regressions')
    plt.savefig(path)
    print(f'Saving widest perceived regressions')
    plt.close()

def values_at_10(all_subject_data):

    d1_dom_at_10, d1_non_dom_at_10, d2_dom_1_at_10, d2_dom_2_at_10 = [], [], [], []

    for current_subject_data in all_subject_data:
        d1_dom, d1_non_dom, d2_dom_1, d2_dom_2 = perceived_at_10(current_subject_data)

        d1_dom_at_10.append(d1_dom)
        d1_non_dom_at_10.append(d1_non_dom)
        d2_dom_1_at_10.append(d2_dom_1)
        d2_dom_2_at_10.append(d2_dom_2)

    return d1_dom_at_10, d1_non_dom_at_10, d2_dom_1_at_10, d2_dom_2_at_10

def perceived_at_10(current_subject_data):

    d1_dom = average_at_10(current_subject_data[0])
    d1_non_dom = average_at_10(current_subject_data[1])
    d2_dom_1 = average_at_10(current_subject_data[2])
    d2_dom_2 = average_at_10(current_subject_data[3])

    return d1_dom, d1_non_dom, d2_dom_1, d2_dom_2


def average_at_10(block):
    actual_widths = block.actual_widths
    perceived_widths = block.perceived_widths

    perceived_at_10 = []

    for actual_width, perceived_width in zip(actual_widths, perceived_widths):
        if actual_width == 10:
            perceived_at_10.append(perceived_width)

    average_at_10 = np.mean(perceived_at_10)

    return average_at_10

def indices_subjects_without_10(subject_IDs, all_subject_data, widest_lines):
    subjects_with_10_removed = []
    indices_to_pop = []

    for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
        for block in current_subject_data:
            actual_widths = block.actual_widths

            if 10 not in actual_widths:
                print(subject_ID)
                subjects_with_10_removed.append(subject_ID)

    subjects_with_10_removed = list(set(subjects_with_10_removed))

    for subject in subjects_with_10_removed:
        index = subject_IDs.index(subject)
        indices_to_pop.append(index)

    for width in widest_lines:
        if width == '999':
            index = widest_lines.index(width)
            indices_to_pop.append(index)

    indices_to_pop = sorted(indices_to_pop)
    indices_to_pop.reverse()

    return indices_to_pop