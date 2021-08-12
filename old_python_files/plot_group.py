import matplotlib.pyplot as plt
from pathlib import Path
from random import random
import random as rd
import numpy as np
from matplotlib.lines import Line2D
from matplotlib import cm
from termcolor import colored

import old_python_files.old_functions
import utils
import calculate_area

constants = utils.create_general_constants()
plot_constants = old_python_files.old_functions.create_plot_constants()


def subject_reg_lines_by_category(experiment, subjects, all_subject_data):
    plot = 'reg_lines_by_group'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)
    legend_handles = [plot_constants.MINIMISER_PATCH,
                      plot_constants.MAXIMISER_PATCH,
                      plot_constants.CROSSER_PATCH]
    y_points = []
    x_points = []

    if experiment == 'exp1':
        subplot_indices = [1, 2, 3, 4]
        subplot_width = 2
        subplot_length = 2
        figsize = (10, 10)
        condition_names = ['Day 1 dominant', 'Day 1 non-dominant', 'Day 2 dominant A', 'Day 2 dominant B']
    else:
        subplot_indices = [1, 2, 3]
        subplot_width = 1
        subplot_length = 3
        figsize = (15, 5)
        condition_names = ['Visual -> Proprioceptive', 'Proprioceptive -> Visual', 'Proprioceptive -> Proprioceptive']

    plt.figure(figsize= figsize)
    plt.suptitle(str('Participant Regression Lines'), fontfamily = 'arial', fontsize = 10)

    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple in data_list:
            plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
            plt.grid(True)
            intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
            intersect_x, intersect_y = calculate_area.point_of_intersection_with_reality(intercept, slope)
            x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                               experiment)
            y_points.append(y1)
            y_points.append(y2)
            x_points.append(x1)
            x_points.append(x2)
            line_colour = old_python_files.old_functions.subject_line_colour(intersect_x, y1, experiment)
            plt.plot([x1, x2], [y1, y2], color='grey', linewidth=0.5)


        y_min, y_max = min(y_points) - 1, max(y_points) + 1
        x_min, x_max = min(x_points) - 1, max(x_points) + 1

        for subplot, condition_name in zip(subplot_indices, condition_names):
            plt.subplot(subplot_width, subplot_length, subplot)
            plt.title(condition_name, loc='right', fontfamily='arial', fontsize=10)
            plt.xticks([2, 4, 6, 8, 10], fontfamily = 'arial', fontsize = 10)
            plt.xlim([2, 10])
            plt.yticks([0, 2, 4, 6, 8, 10, 12, 14], fontfamily = 'arial', fontsize = 10)
            plt.ylim([0, 14])
            plt.ylabel('Response width (cm)', fontfamily = 'arial', fontsize = 10)
            plt.xlabel('Actual width (cm)', fontfamily = 'arial', fontsize = 10)
            #plt.legend(handles=legend_handles, loc='upper left')
            plt.plot([2, 10], [2, 10], 'k--', linewidth=1.5)


    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'Group regression plots saved in {text}')
    plt.close()


def kathy_difference_of_differences(all_subject_data, experiment):
    plot = 'difference_of_differences'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    plt.figure(figsize=(7, 10))
    plt.suptitle(str('Difference of Differences'))
    plt.ylabel('Area Difference (cm^2)')
    plt.xlabel('Condition Pair')
    plt.grid()
    x_points_base = [1, 2, 3]
    plt.xticks(x_points_base,
               labels=['d1d - d1nd', 'd1d - d2d_a', 'd2d_a - d2d_b'])
    plt.yticks(range(-10, 10))
    key_text = str('d1d - d1nd = difference between dominant and non dominant hand on the same day \n '
                   'd1d - d2d_a = difference between two dominant hand test sessions on different days \n'
                   'd2d_a - d2d_b = difference between two dominant hand test sessions the same day ')
    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    hands_vs_day_list, hands_vs_days_list, day_vs_days_list = [], [], []

    for subject_data in all_subject_data:
        hands_vs_day, hands_vs_days, day_vs_days = old_python_files.old_functions.difference_of_difference_areas(experiment, subject_data)

        hands_vs_day_list.append(hands_vs_day)
        hands_vs_days_list.append(hands_vs_days)
        day_vs_days_list.append(day_vs_days)

        y_points = [hands_vs_day, hands_vs_days, day_vs_days]

        plt.plot(x_points_base, y_points, color='silver', alpha=0.5)

    area_diff_list = [hands_vs_day_list, hands_vs_days_list, day_vs_days_list]
    area_max, area_min = old_python_files.old_functions.max_min(area_diff_list)
    y_range = range(int(-area_max), int(area_max + 2))

    for x_point, area_list in zip(x_points_base, area_diff_list):
        mean, ci = utils.calculate_mean_ci(area_list)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec='r', markersize=8)

    plt.hlines(y=0, xmin=1, xmax=3, color='dimgrey', linestyle='--', lw=2)
    plt.ylim(-area_max, (area_max + 1))
    plt.yticks(y_range)
    plt.legend(handles=legend_elements, loc='upper right')
    plt.text(0.08, 0.01, key_text, fontsize=10, bbox=dict(facecolor='none', edgecolor='red'),
             transform=plt.gcf().transFigure)
    plt.savefig(path, bbox_inches='tight')
    text = colored(path, 'blue')
    print(f'Difference of difference plot saved in {text}\n')
    plt.close()


def area_per_condition_plot(all_subject_data, experiment):
    plot = 'areas_by_condition'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    plt.figure(figsize=(10, 10))
    plt.suptitle(str('Area Between Regression and Reality Lines'))
    plt.ylabel('Area Between Lines (cm^2)')
    plt.xlabel('Condition')

    x_points = utils.x_points_group_plot(experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)

    plt.xticks(x_points, labels=x_labels)

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='^', label='Mean Area Difference', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    all_area_lists = []

    for subject_data in all_subject_data:
        data_pair_tuples = utils.create_data_tuples(experiment, subject_data)
        y_points = []

        for tuple in data_pair_tuples:
            y_points.append(calculate_area.normalised(tuple.ACTUAL, tuple.PERCEIVED, experiment))

        all_area_lists.append(y_points)

        plt.plot(x_points, y_points, color='darkgrey', alpha=0.5)

    area_means, area_CIs = calculate_area.store_condition_area_means_and_cis(all_subject_data, experiment)

    for mean, ci, x_point in zip(area_means, area_CIs, x_points):
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='r', mec='r', markersize=8)

    area_max, area_min = old_python_files.old_functions.max_min(all_area_lists)
    plt.ylim(area_min - 1, area_max + 2)
    plt.legend(handles=legend_elements, loc='best')
    plt.grid()
    plt.savefig(path)
    text = colored(f'{path}', 'blue')
    print(f'Area per condition plots saved in {text}\n')
    plt.close()


def area_vs_r2_plot(all_subject_data, experiment):
    plot = 'area_r2_regression'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    area_lists = calculate_area.group_areas(all_subject_data, experiment)
    r2_lists = utils.store_r2_lists(all_subject_data, experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)
    subplot_indices = utils.x_points_group_plot(experiment)


    plt.figure(figsize=(20, 10))
    plt.suptitle('Area Between Reg Line + Reality Line vs. R^2 Value')
    for subplot_index, condition_r2_data, condition_area_data, condition_name in zip(subplot_indices, r2_lists, area_lists, x_labels):

        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)
        plt.subplot(subplot_indices[0], subplot_indices[-1], subplot_index)
        x_vals = np.array([min(condition_area_data), max(condition_area_data)])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color = 'b')
        plt.scatter(condition_area_data, condition_r2_data, marker='o', color='royalblue', alpha=0.5)

        legend_handles = [Line2D([0], [0], color='b', lw=2,
                                 label=f'Regression Line\n(y = {slope:6.4f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], marker='o', label='Individual subject (n = 30)', mec='royalblue',
                                 markerfacecolor='royalblue', markersize=8, linestyle='None')]

        plt.xlim(min(condition_area_data)-1, max(condition_area_data)+1)
        plt.ylim(min(condition_r2_data)-0.01, max(condition_r2_data)+0.01)
        plt.grid()
        plt.legend(handles = legend_handles, loc = 'upper left')
        plt.title(condition_name, loc='right')
        plt.xlabel('Area (cm^2)')
        plt.ylabel('R^2 Value')
        plt.tight_layout()
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'Area vs r2 plots saved in {text}\n')
    plt.close()


def r2_per_condition_plot(all_subject_data, experiment):
    plot = 'r2_per_condition'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    legend_elements = [Line2D([0], [0], color='silver', lw=2, label='Individual Subjects'),
                       Line2D([0], [0], marker='o', label='Mean R^2', mec='r',
                              markerfacecolor='r', markersize=8, linestyle='None'),
                       Line2D([0], [0], color='black', label='95% Confidence Interval', lw=2)]

    plt.figure(figsize=(10, 10))
    plt.suptitle('R^2 (actual vs perceived widths) Values Per Condition')
    plt.ylabel('R^2')
    plt.xlabel('Condition')
    x_points = utils.x_points_group_plot(experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)

    plt.xticks(x_points, labels=x_labels)
    all_r2_lists = []

    for subject_data in all_subject_data:
        data_pair_tuples = utils.create_data_tuples(experiment, subject_data)
        y_points = []

        for tuple in data_pair_tuples:
            y_points.append(utils.calculate_r2(tuple.ACTUAL, tuple.PERCEIVED))

        all_r2_lists.append(y_points)

        plt.plot(x_points, y_points, color='darkgrey', alpha=0.5)

    mean_list, ci_list = utils.store_condition_r2_means_and_cis(all_subject_data, experiment)

    for mean, ci, x_point in zip(mean_list, ci_list, x_points):
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="o", markerfacecolor='r', mec='r', markersize=8)

    r2_max, r2_min = old_python_files.old_functions.max_min(all_r2_lists)
    plt.ylim(r2_min - 0.01, 1.01)

    plt.legend(handles=legend_elements, loc='lower right')
    plt.grid()
    plt.savefig(path)
    text = colored(f'{path}', 'blue')
    print(f'R^2 per condition plot saved in {text}\n')
    plt.close()

def lovisa_between_condition_regression(all_subject_data, experiment):
    plot = 'between_condition_regression'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    r2_tuple = utils.store_r2_lists(all_subject_data, experiment)
    area_tuple = calculate_area.group_areas(all_subject_data, experiment)

    subplot_indices = [1, 2]
    line_width_data = [r2_tuple.line_width_r2_list, area_tuple.line_width_area_list]
    width_line_data = [r2_tuple.width_line_r2_list, area_tuple.width_line_area_list]
    plot_names = ['placeholder', 'R^2', 'Area between regression line and reality']

    plt.figure(figsize=(12, 7))
    plt.suptitle('Reciprocal Condition Regressions')

    for subplot_index, line_width, width_line in zip(subplot_indices, line_width_data, width_line_data):
        intercept, slope = utils.calculate_regression_general(line_width, width_line)
        plt.subplot(subplot_indices[0], subplot_indices[-1], subplot_index)
        x_vals = np.array([min(line_width), max(line_width)])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color='b')
        plt.scatter(line_width, width_line, marker='o', color='royalblue', alpha=0.5)
        legend_handles = [Line2D([0], [0], color='b', lw=2,
                                 label=f'Regression\n(y = {slope:6.4f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], marker='o', label='Individual subject (n = 30)', mec='royalblue',
                                 markerfacecolor='royalblue', markersize=8, linestyle='None')]

        #plt.xlim((min(line_width) - (min(line_width)/10)), (max(line_width) + (max(line_width)/10)))
        #plt.ylim((min(width_line) - (min(width_line)/10)), (min(width_line) + (min(width_line)/10)))
        plt.grid()
        plt.legend(handles=legend_handles, loc='best')
        plt.title(f'{plot_names[subplot_index]} Regression', loc='right')
        plt.xlabel(f'Show line pick width {plot_names[subplot_index]}')
        plt.ylabel(f'Present width pick line {plot_names[subplot_index]}')
        plt.tight_layout()
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'reciprocal condition regression saved in {text}\n')
    plt.close()

def slope_comparison(all_subject_data, experiment):
    plot = 'slope_comparison'
    path = old_python_files.old_functions.create_group_plot_save_path(experiment, plot)

    slopes_line_width = []
    slopes_width_line = []

    for subject_data in all_subject_data:
        intercept_line_width, slope_line_width = utils.calculate_regression_general(subject_data.LINE_WIDTH.ACTUAL, subject_data.LINE_WIDTH.PERCEIVED)
        intercept_width_line, slope_width_line = utils.calculate_regression_general(subject_data.WIDTH_LINE.ACTUAL, subject_data.WIDTH_LINE.PERCEIVED)

        slopes_line_width.append(slope_line_width)
        slopes_width_line.append(slope_width_line)

    print(f'Line width list: {slopes_line_width}')
    print(f'Width line list: {slopes_width_line}')
    plt.figure(figsize=(5,5))
    plt.suptitle('Slope Comparison')

    intercept, slope = utils.calculate_regression_general(slopes_line_width, slopes_width_line)
    utils.regression_summary(slopes_line_width, slopes_width_line)

    x_vals = np.array([min(slopes_line_width)-0.25, max(slopes_line_width)+0.25])
    y_vals = intercept + slope * x_vals

    plt.plot(x_vals, y_vals, color='b')
    plt.scatter(slopes_line_width, slopes_width_line, marker='o', color='royalblue', alpha=0.5)
    legend_handles = [Line2D([0], [0], color='b', lw=2,
                             label=f'Regression Line\n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                      Line2D([0], [0], marker='o', label='Subject (n = 30)', mec='royalblue',
                             markerfacecolor='royalblue', markersize=8, linestyle='None')]

    plt.grid()
    plt.legend(handles=legend_handles, loc='best')
    plt.xlabel(f'Slope: show line pick width')
    plt.ylabel(f'Slope: present width pick line')
    plt.xlim((min(slopes_line_width) - 0.25), (max(slopes_line_width) + 0.25))
    plt.ylim((min(slopes_width_line) - 0.25), (max(slopes_width_line) + 0.25))
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'slope comparison saved in {text}\n')
    plt.close()