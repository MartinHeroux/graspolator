import matplotlib.pyplot as plt
from random import random
from pathlib import Path
import numpy as np
from matplotlib.lines import Line2D

import utils




def plot_regression_widest_perceived(subject_IDs, all_subject_data, widest_lines):
    condition_names = ["day2_dominant_1", "day2_dominant_2"]
    subplot_indices = [1, 2]

    indices_to_pop, indices_to_replace = indices_subjects_without_10(subject_IDs, all_subject_data, widest_lines)
    repl_values = replacement_values(all_subject_data, indices_to_replace)

    d2_dom_1_at_10, d2_dom_2_at_10 = values_at_10(all_subject_data)

    for index in indices_to_pop:
        d2_dom_1_at_10.pop(index)
        d2_dom_2_at_10.pop(index)
        widest_lines.pop(index)

    for index, replacement_value in zip(indices_to_replace, repl_values):
        d2_dom_1_at_10[index] = replacement_value
        d2_dom_2_at_10[index] = replacement_value

    widest_lines_int = [int(str_value) for str_value in widest_lines]

    lengths_list = [len(d2_dom_1_at_10), len(d2_dom_2_at_10), len(widest_lines)]
    for item in lengths_list:
        if item is not (len(subject_IDs) - len(indices_to_pop)):
            print('error in popping values, uneven lists, exiting')
            exit()
        else:
            print('list length correct, continuing')

    values_at_10_lists = d2_dom_1_at_10, d2_dom_2_at_10

    plt.figure(figsize=(15, 5))
    plt.suptitle(str('Widest Grasp vs Perceived Grasp Width at 10cm Regressions'))

    legend_elements = [Line2D([0], [0], color='r', lw=2, label='Regression Line')]
                       #Line2D([0], [0], color='black', lw=2, label='Line of Reality')

    for subplot_index, condition_values, condition_name in zip(subplot_indices, values_at_10_lists, condition_names):
        plt.subplot(1, 2, subplot_index)
        length_data = len(condition_values)
        random_values = [random() / 3 for _ in range(length_data)]
        x_data = np.array(condition_values) + np.array(random_values)
        plt.scatter(x_data, widest_lines_int, marker='o', alpha = 0.5, color = 'royalblue')
        #plt.plot([5, 15], [5, 15], 'k--')

        intercept, slope = utils.calculate_regression_general(condition_values, widest_lines_int)
        print(intercept, slope)

        plt.text(6, 13, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)

        x5 = 5
        x15 = 15
        y0 = slope * x5 + intercept
        y14 = slope * x15 + intercept
        plt.plot([x5, x15], [y0, y14], color='r')
        plt.title(condition_name, loc='right')
        plt.xticks(range(4, 16))
        plt.xlim([4, 16])
        plt.ylabel('Perceived Widest Possible Grasp (cm)')
        plt.xlabel('Perceived Width at Actual Width 10cm')
        plt.grid()
        plt.legend(handles=legend_elements, loc='lower right')

    path = Path('./plots/group_plots/widest_line_regressions')
    plt.savefig(path)
    print(f'Saving widest perceived regressions')
    plt.close()

def values_at_10(all_subject_data):

    d2_dom_1_at_10, d2_dom_2_at_10 = [], []

    for current_subject_data in all_subject_data:
        d2_dom_1, d2_dom_2 = perceived_at_10(current_subject_data)

        d2_dom_1_at_10.append(d2_dom_1)
        d2_dom_2_at_10.append(d2_dom_2)

    return d2_dom_1_at_10, d2_dom_2_at_10

def perceived_at_10(current_subject_data):

    d2_dom_1 = average_at_10(current_subject_data[2])
    d2_dom_2 = average_at_10(current_subject_data[3])

    return d2_dom_1, d2_dom_2


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
    indices_to_replace = []

    for subject_ID, current_subject_data in zip(subject_IDs, all_subject_data):
        for block in current_subject_data:
            actual_widths = block.actual_widths

            if 10 not in actual_widths:
                print(subject_ID)
                subjects_with_10_removed.append(subject_ID)

    subjects_with_10_removed = list(set(subjects_with_10_removed))

    for subject in subjects_with_10_removed:
        index = subject_IDs.index(subject)
        indices_to_replace.append(index)

    for width in widest_lines:
        if width == '999':
            index = widest_lines.index(width)
            indices_to_pop.append(index)

    indices_to_pop = sorted(indices_to_pop)
    indices_to_pop.reverse()
    indices_to_replace = sorted(indices_to_replace)
    indices_to_replace.reverse

    return indices_to_pop, indices_to_replace


def replacement_values(all_subject_data, indices_to_replace):
    values_to_replace = []
    for index in indices_to_replace:
        data = all_subject_data[index]
        D2_dom_1, D2_dom_2 = data[2], data[3]
        intercept_1, slope_1 = utils.calculate_regression(D2_dom_1)
        intercept_2, slope_2 = utils.calculate_regression(D2_dom_2)
        x = 10
        value_at_10_a = (slope_1 * x) + intercept_1
        value_at_10_b = (slope_2 * x) + intercept_2
        value_at_10 = (value_at_10_b + value_at_10_a) / 2
        values_to_replace.append(value_at_10)
    return values_to_replace
