import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import numpy as np
import random as rd


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
        plt.ylim([1, 14])
        plt.yticks([0.5] + list(range(1, 14)))
        plt.grid()
        plt.title(name, loc = 'right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig('{}/{}'.format(path_1, subject_ID))
    print(f'Saving id scatter plots for {subject_ID}')
    plt.close()

    plt.figure(figsize=(10, 10))
    plt.suptitle(str('Scatterplot'))

    for subplot_index, condition_data, name in zip(subplot_indices, subject_data, condition_names):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_data.perceived_widths)
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array((condition_data.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.ylim([1, 14])
        plt.yticks([0.5] + list(range(1, 14)))
        plt.grid()
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig(('{}/{}'.format(path_2, plot)))
    print(f'Saving de_id scatter plots for {subject_ID}')
    plt.close