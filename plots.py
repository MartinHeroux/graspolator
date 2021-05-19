import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
from random import random
import random as rd
import os
from collections import namedtuple
import numpy as np
from matplotlib.lines import Line2D
import scipy.stats as scp


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
    plt.close()


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
            x_intersect, y_intersect = utils.point_of_intersection_with_reality(intercept, slope)
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
        x_intersect, y_intersect = utils.point_of_intersection_with_reality(intercept, slope)
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

def group_consistency_plot(subject_IDs, all_subject_data):
    if not os.path.exists('./plots/group_plots'):
        os.makedirs('./plots/group_plots')

    path = Path('./plots/group_plots/')

    plt.figure(figsize=(7, 10))
    plt.suptitle(str('All Subject Consistency Plot'))
    plt.ylabel('Area Difference Between Regression Lines (cm^2)')
    plt.xlabel('Condition Pair')
    plt.grid()
    x_points_base = [1, 2, 3]
    plt.xticks(x_points_base, labels = ['Between Hands', 'Between Days', 'Within Day'])

    for line_number, (subject_ID, current_subject_data) in enumerate(zip(subject_IDs, all_subject_data), start=1):
        y_points = []
        jitter_values = [random() / 40 for _ in range(len(x_points_base))]
        if line_number < 15:
            x_points_jitter = np.array(x_points_base) + np.array(jitter_values)
        else:
            x_points_jitter = np.array(x_points_base) - np.array(jitter_values)

        between_hands, between_days, within_days = area_calcs.bh_bd_wd_areas(current_subject_data)
        y_points = [between_hands, between_days, within_days]
        rgb = np.random.rand(3, )
        plt.plot(x_points_jitter, y_points, color=rgb, marker = 'o', alpha = 0.5)

    plt.savefig('{}/group_consistency_plot.png'.format(path))
    print(f'Saving group consistency plots')
    plt.close()


def plot_difference_of_differences(all_subject_data):
    path = Path('./plots/group_plots/difference_of_differences_plot')

    plt.figure(figsize=(7, 10))
    plt.suptitle(str('Difference of Differences'))
    plt.ylabel('Difference Between Areas (cm^2)')
    plt.xlabel('Difference Pair')
    plt.grid()
    x_points_base = [1, 2, 3]
    plt.xticks(x_points_base,
               labels=['Between Hands - Within Day', 'Between Hands - Between Days', 'Within Day - Between Days'])
    plt.yticks(range(-10, 10))

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    all_bh_wd = []
    all_bh_bd = []
    all_wd_bd = []

    for current_subject_data in all_subject_data:
        between_hands_area, between_day_area, within_day_area = area_calcs.bh_bd_wd_areas(
            current_subject_data)
        bh_wd = between_hands_area - within_day_area
        bh_bd = between_hands_area - between_day_area
        wd_bd = within_day_area - between_day_area

        all_bh_wd.append(bh_wd)
        all_bh_bd.append(bh_bd)
        all_wd_bd.append(wd_bd)

        y_points = [bh_wd, bh_bd, wd_bd]

        plt.plot(x_points_base, y_points, color='silver', alpha=0.5)

    area_diff_list = [all_bh_wd, all_bh_bd, all_wd_bd]
    maximum_area_differences = [max(all_bh_wd), max(all_bh_bd), max(all_wd_bd)]
    maximum_area_difference = max(maximum_area_differences)

    for x_point, data in zip(x_points_base, area_diff_list):
        mean = np.mean(data)
        ci = utils.confidence_interval(data)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec = 'r', markersize=8)

    plt.hlines(y=0, xmin=1, xmax=3, color='dimgrey', linestyle='--', lw=2)
    plt.ylim(-(maximum_area_difference+1), (maximum_area_difference+1))
    plt.legend(handles=legend_elements, loc='upper right')
    plt.savefig(path)
    print(f'Saving difference of area differences plots')
    plt.close()

def plot_area_across_conditions(all_subject_data):
    if not os.path.exists('./plots/group_plots'):
        os.makedirs('./plots/group_plots')

    path = Path('./plots/group_plots/all_subject_areas_across_conditions')

    plt.figure(figsize=(10, 10))
    plt.suptitle(str('Area Between Regression and Reality Per Condition'))
    plt.ylabel('Area Between Lines (cm^2)')
    plt.xlabel('Condition')
    plt.grid()
    x_points_base = [1, 2, 3, 4]
    plt.xticks(x_points_base,
               labels=['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"])
    plt.ylim(0, 24)

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    d1_dom_areas, d1_non_dom_areas, d2_dom_1_areas, d2_dom_2_areas = [], [], [], []
    all_areas = d1_dom_areas, d1_non_dom_areas, d2_dom_1_areas, d2_dom_2_areas

    for subject_data in all_subject_data:
        d1_dom_area = utils.area_difference(subject_data[0])
        d1_non_dom_area = utils.area_difference(subject_data[1])
        d2_dom_1_area = utils.area_difference(subject_data[2])
        d2_dom_2_area = utils.area_difference(subject_data[3])

        y_points = [d1_dom_area, d1_non_dom_area, d2_dom_1_area, d2_dom_2_area]

        d1_dom_areas.append(d1_dom_area)
        d1_non_dom_areas.append(d1_non_dom_area)
        d2_dom_1_areas.append(d2_dom_1_area)
        d2_dom_2_areas.append(d2_dom_2_area)

        plt.plot(x_points_base, y_points, color='darkgrey', alpha=0.5)

    for x_point, data in zip(x_points_base, all_areas):
        mean = np.mean(data)
        ci = utils.confidence_interval(data)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec = 'r', markersize=8)

    plt.legend(handles=legend_elements, loc='upper left')
    plt.savefig(path)
    print(f'Saving difference of area difference by condition plots')
    plt.close()

def area_vs_r2_plot(all_subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    r2_lists = [[], [], [], []]
    area_lists = [[], [], [], []]
    path = Path('./plots/group_plots')

    for condition_number, condition_name in enumerate(condition_names, start=0):
        for current_subject_data in all_subject_data:
            data_for_calcs = current_subject_data[condition_number]
            actual_widths = data_for_calcs.actual_widths
            perceived_widths = data_for_calcs.perceived_widths
            r_score, p_value = scp.pearsonr(actual_widths, perceived_widths)
            r_squared = r_score ** 2
            r2_lists[condition_number].append(r_squared)

            area_total = area_calcs.extract_area_number(data_for_calcs)
            area_lists[condition_number].append(area_total)

    print(f'R2 List lengths: D1_dom: {len(r2_lists[0])}, D1_non_dom: {len(r2_lists[1])}, D2_dom_1: {len(r2_lists[2])}, D2_dom_2: {len(r2_lists[3])}')
    print(f'Area List lengths: D1_dom: {len(area_lists[0])}, D1_non_dom: {len(area_lists[1])}, D2_dom_1: {len(area_lists[2])}, D2_dom_2: {len(area_lists[3])}')
    print(r2_lists)
    print(area_lists)

    plt.figure(figsize=(10, 10))
    plt.suptitle('Area Between Reg Line + Reality Line vs. R^2 Value')
    for subplot_index, (condition_r2_data, condition_area_data, condition_name) in enumerate(zip(r2_lists, area_lists, condition_names), start = 1):
        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)
        #utils.abline(slope, intercept)
        plt.subplot(2, 2, subplot_index)
        x_vals = np.array([1, 26])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, 'k--')
        plt.scatter(condition_area_data, condition_r2_data, marker = 'o', color = 'royalblue', alpha = 0.5)
        plt.text(15, 0.75, f'{slope:6.5f}*x + {intercept:4.2f}', fontsize=12)
        plt.xlim([1, 26])
        plt.ylim([0.7, 1])
        plt.grid()
        plt.title(condition_name, loc='right')
        plt.xlabel('Area (cm^2)')
        plt.ylabel('R^2 Value')
        plt.tight_layout()
    plt.savefig('{}/{}'.format(path, 'area_vs_r2_plot_by_condition'), dpi=300)
    print(f'Saving area vs r2 plots')
    plt.close()

def r2_group_plot(all_subject_data):
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"]
    r2_lists = [[], [], [], []]
    path = Path('./plots/group_plots')

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='_', label='Mean R^2', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    for condition_number, condition_name in enumerate(condition_names, start = 0):
        for current_subject_data in all_subject_data:
            data_for_calcs = current_subject_data[condition_number]
            actual_widths = data_for_calcs.actual_widths
            perceived_widths = data_for_calcs.perceived_widths
            r_score, p_value = scp.pearsonr(actual_widths, perceived_widths)
            r_squared = r_score ** 2
            r2_lists[condition_number].append(r_squared)
        print(len(r2_lists[condition_number]))

    plt.figure(figsize=(10, 10))
    plt.suptitle('R^2 (actual vs perceived widths) Values Per Condition')
    plt.ylabel('R^2')
    plt.xlabel('Condition')

    d1_dom = r2_lists[0]
    d1_non_dom = r2_lists[1]
    d2_dom_1 = r2_lists[2]
    d2_dom_2 = r2_lists[3]

    for y1, y2, y3, y4 in zip(d1_dom, d1_non_dom, d2_dom_1, d2_dom_2):
        x_points = [1, 2, 3, 4]
        y_points = [y1, y2, y3, y4]
        plt.plot(x_points, y_points, color='darkgrey', alpha=0.5)

    for x_point, data in zip(x_points, r2_lists):
        mean = np.mean(data)
        ci = utils.confidence_interval(data)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="_", markerfacecolor='r', mec = 'r', markersize=8)

    plt.legend(handles=legend_elements, loc='lower right')
    plt.xticks(x_points,
               labels=['day1_dominant', "day1_non_dominant", "day2_dominant_1", "day2_dominant_2"])
    plt.savefig(f'{path}/r2_summary.png')
    print(f'Saving difference of area difference by condition plots')
    plt.close()