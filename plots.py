import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from random import random
import random as rd
import numpy as np
import os

import utils
import area_calcs


def plot_and_store(subject_ID, subject_data):
    if not os.path.exists('./plots/reg_plots'):
        os.makedirs('./plots/reg_plots')
    else:
        print('reg plot folder already exists')

    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]

    path = Path('./plots/reg_plots/')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot + Reg Line'))
    for subplot_index, (condition_data, name) in enumerate(zip(subject_data, condition_names), start=1):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition_data.perceived_widths)
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_data.actual_widths) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        intercept, slope = utils.calculate_regression(condition_data)

        x2 = 2
        x10 = 10
        y2 = slope * x2 + intercept
        y10 = slope * x10 + intercept
        plt.plot([x2, x10], [y2, y10], color='royalblue')
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks([0.5] + list(range(1, 14)))
        plt.ylim([0, 14])
        plt.grid()
        plt.title(name, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig(str('{}/{}'.format(path, subject_ID)))
    print(f'Saving scatter plots and regressions for {subject_ID}')
    plt.close()


def random_plot(plot, subject_ID, subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]

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
        random_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array((condition_data.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition_data.perceived_widths, 'o', alpha=0.5, color='royalblue')

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.ylim([1, 15])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.grid()
        plt.title(name, loc='right')
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
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]

    plt.figure(figsize=(15, 5))
    plt.suptitle(str('Participant Regression Lines'))
    subplot_indices = [1, 2, 3, 4]

    for condition_name, subplot_index in zip(condition_names, subplot_indices):
        plt.subplot(1, 4, subplot_index)
        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks(list(range(-1, 16)))
        plt.ylim([-1, 16])
        plt.grid()
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.legend(handles=[minimiser, maximiser, crosser], loc='upper left')
        plt.plot([2, 10], [2, 10], 'k--', linewidth=1.5)
        plt.title(condition_name, loc='right')

    for subject_ID, subject_data in zip(subject_IDs, all_subject_data):
        for subplot_index, condition_data in zip(subplot_indices, subject_data):
            plt.subplot(1, 4, subplot_index)

            intercept, slope = utils.calculate_regression(condition_data)
            x_intersect, y_intersect = utils.point_of_intersection(intercept, slope)
            x2, x10, y_at_x2, y_at_x10 = utils.reg_line_endpoints(intercept, slope)
            line_colour = utils.subject_line_colour(x_intersect, y_at_x2)
            plt.plot([x2, x10], [y_at_x2, y_at_x10], color=line_colour, linewidth=0.5)
            print('Reg line plotted subplot {}, subject {}'.format(subplot_index, subject_ID))

    plt.savefig('{}/{}'.format(path, 'reg_lines_by_group_by_condition'), dpi=300)
    print(f'Saving whole group reg plots')
    plt.close()


def plot_areas(subject_ID, subject_data):
    if not os.path.exists('./plots/area_plots'):
        os.makedirs('./plots/area_plots')
    else:
        print('area plot folder already exists')

    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]

    path = Path('./plots/area_plots/')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Difference Plots (area between lines of reality and regression)'))
    for subplot_index, (condition_data, name) in enumerate(zip(subject_data, condition_names), start=1):
        print(f'Starting subplot {subplot_index} for {subject_ID}')
        plt.subplot(2, 2, subplot_index)
        plt.plot([2, 10], [2, 10], 'k--')

        intercept, slope = utils.calculate_regression(condition_data)
        x_intersect, y_intersect = utils.point_of_intersection(intercept, slope)
        x2, x10, y_at_x2, y_at_x10 = utils.reg_line_endpoints(intercept, slope)
        group = utils.subject_group(x_intersect, y_at_x2)

        if group == 'crosser':
            area_left, area_right, area_difference = area_calcs.crosser_area_calc(x_intersect,
                                                                                  y_intersect,
                                                                                  y_at_x2,
                                                                                  y_at_x10)
            text = str(
                f'area_left = {area_left:4.2f} \narea_right = {area_right:4.2f} \narea_difference = {area_difference:4.2f}')
        elif group == 'crosser_triangle':
            area_left, area_right, area_difference = area_calcs.crosser_triangle_area_calc(x_intersect,
                                                                                           y_intersect,
                                                                                           y_at_x2,
                                                                                           y_at_x10)
            text = str(
                f'area_left = {area_left:4.2f} \narea_right = {area_right:4.2f} \narea_difference = {area_difference:4.2f}')
        elif group == 'minimiser':
            area_difference = area_calcs.minimiser_area_calc(y_at_x2, y_at_x10)
            text = str(f'area_difference = {area_difference:4.2f}')
        else:
            area_difference = area_calcs.maximiser_area_calc(y_at_x2, y_at_x10)
            text = str(f'area_difference = {area_difference:4.2f}')

        x_colour_points = np.array([2, 10])
        y_points_reality = np.array([2, 10])
        y_points_reg = np.array([y_at_x2, y_at_x10])

        plt.plot([x2, x10], [y_at_x2, y_at_x10], color='royalblue')
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                         color='C0', alpha=0.3, interpolate=True)

        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)
        plt.text(2, 9, text, fontsize=10)

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.ylim([0, 15])
        plt.grid()
        plt.title(name, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig('{}/{}'.format(path, subject_ID))
    print(f'Saving area plots for {subject_ID}')
    plt.close()


def plot_area_between_reg_lines(subject_ID, subject_data):
    if not os.path.exists('./plots/area_between_reg_lines'):
        os.makedirs('./plots/area_between_reg_lines')
    else:
        print('folder already exists, continuing')

    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    colours = ['r', 'g', 'b', 'orange']

    path = Path('./plots/area_between_reg_lines/')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Difference between Reg. Lines'))

    for condition_data, name, colour in zip(subject_data, condition_names, colours):
        intercept, slope = utils.calculate_regression(condition_data)
        x2, x10, y_at_x2, y_at_x10 = utils.reg_line_endpoints(intercept, slope)
        plt.plot([x2, x10], [y_at_x2, y_at_x10], color=colour)

    plt.xticks(range(2, 11))
    plt.xlim([1, 11])
    plt.yticks([0.5] + list(range(1, 14)))
    plt.ylim([0, 14])
    plt.grid()
    plt.ylabel('Perceived width (cm)')
    plt.xlabel('Actual width (cm)')

    plt.savefig(str('{}/{}_all_reg_lines'.format(path, subject_ID)))
    print(f'Saving all reg lines for {subject_ID}')
    plt.close()
