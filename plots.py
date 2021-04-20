import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from random import random
import random as rd
import numpy as np
import random
import os

import utils
import regression_calcs


def plot_and_store(subject_ID, subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_domimant_1", "day2_dominant_2"]

    path = Path('./subject_folders_exp1/' + subject_ID)
    subject_txt_file = open('{}/{}_m_and_b.txt'.format(path, subject_ID), 'a')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))
    for subplot_index, (condition_data, name) in enumerate(zip(subject_data, condition_names), start=1):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_data.perceived_widths)
        random_values = [random()/4 for _ in range(length_data)]
        x_data = np.array((condition_data.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        intercept, slope = utils.calculate_regression(condition_data)
        text_to_write = [f'{name}', '\n', f'Intercept: {intercept:4.2f}', '\n' , f'Slope: {slope:4.2f}', '\n']
        subject_txt_file.writelines(text_to_write)

        x2 = 2
        x10 = 10
        y2 = slope*x2 + intercept
        y10 = slope*x10 + intercept
        plt.plot([x2, x10], [y2, y10], color='royalblue')
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks([0.5] + list(range(1, 14)))
        plt.ylim([0, 14])
        plt.grid()
        plt.title(name, loc = 'right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    subject_txt_file.close()
    plt.savefig('{}/{}'.format(path, subject_ID))
    print(f'Saving scatter plots and regressions for {subject_ID}')
    plt.close()


def random_plot(plot, subject_ID, subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_domimant_1", "day2_dominant_2"]

    path_1 = Path('./randomised_plots_with_id/')
    path_2 = Path('./randomised_plots_no_id/')

    subplot_indices = [1, 2, 3, 4]
    rd.shuffle(subplot_indices)

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))

    for subplot_index, condition_data, name in zip(subplot_indices, subject_data, condition_names):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_data.perceived_widths)
        random_values = [random()/4 for _ in range(length_data)]
        x_data = np.array((condition_data.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.ylim([1, 15])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.grid()
        plt.title(name, loc = 'right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig('{}/{}'.format(path_1, subject_ID))
    print(f'Saving id scatter plots for {subject_ID}')
    plt.close()

    plt.figure(figsize=(10, 10))
    plt.suptitle(str('{} Scatterplot'.format(plot)))

    for subplot_index, condition_data, name in zip(subplot_indices, subject_data, condition_names):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_data.perceived_widths)
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array((condition_data.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.ylim([1, 15])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.grid()
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig(('{}/{}.pdf'.format(path_2, plot)))
    print(f'Saving de_id scatter plots for {subject_ID}')
    plt.close


def plot_subject_reg_lines_by_category(subject_IDs, all_subject_data):
    if not os.path.exists('./plots/group_plots'):
        os.makedirs('./plots/group_plots')
    else:
        print('group plot folder already exists')

    path = Path('./plots/group_plots')
    minimiser = mpatches.Patch(color='firebrick', label='Minimiser')
    maximiser = mpatches.Patch(color='green', label='Maximiser')
    crosser = mpatches.Patch(color='royalblue', label='Crosser')

    plt.figure(figsize=(15, 20))
    plt.suptitle(str('Participant Regression Lines'))
    plt.plot([2, 10], [2, 10], 'k--', linewidth = 5)
    print('Line of reality plotted')

    for subject_ID, subject_data in zip(subject_IDs, all_subject_data):
        y_when_x_is_2, y_when_x_is_10, line_colour = regression_calcs.subject_reg_line(subject_data)
        print(y_when_x_is_2, y_when_x_is_10, line_colour)
        x2 = 2
        x10 = 10
        plt.plot([x2, x10], [y_when_x_is_2, y_when_x_is_10], color=line_colour)
        print('Reg line plotted {}'.format(subject_ID))

    plt.xticks(range(2, 11))
    plt.xlim([1, 11])
    plt.yticks(list(range(-3, 16)))
    plt.ylim([-1, 16])
    plt.grid()
    plt.ylabel('Perceived width (cm)')
    plt.xlabel('Actual width (cm)')
    plt.legend(handles=[minimiser, maximiser, crosser])

    plt.savefig('{}/{}'.format(path, 'reg_lines_by_group'))
    print(f'Saving whole group reg ')
    plt.close()
