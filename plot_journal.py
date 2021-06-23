import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from random import random
from pathlib import Path
from matplotlib.ticker import MultipleLocator
from termcolor import colored
from matplotlib.lines import Line2D

import utils
import plot_utils
import calculate_area

constants = utils.create_general_constants()
plot_constants = plot_utils.create_plot_constants()


## panel figure of individual subjects and group reg lines

def example_subjects_group_reg_summary(all_subject_data, subjects, experiment):
    plot = f'example_subjects_group_regression_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    tuple_list = plot_utils.store_example_subject_plot_info(all_subject_data, subjects, experiment)

    subplot_rows = 4
    subplot_cols = 3

    # set up experiment specific parameters
    if experiment == 'exp1':
        condition_names = ['dominant', 'non-dominant', 'dominant', 'dominant']
        x_lims = [2, 10]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9, 12]
        colors = ['royalblue', 'seagreen']
        example_subjects = ['SUB05R', 'SUB01L']
        text_x = -3.5
    else:
        condition_names = ['line to width', 'width to line', 'width to width', 'dummy_data']
        x_lims = [3, 9]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9]
        colors = ['darkblue', 'darkorange']
        example_subjects = ['SUB04', 'SUB23']
        text_x = -1.5

    plt.figure(figsize=(8.1 / 2.4, 12 / 2.4))
    # plot example subjects in left and centre subplot cols
    for column, (example_subject_tuple, color) in enumerate(zip(tuple_list, colors), start=1):
        for condition_data, condition_plot_index, condition_name in zip(example_subject_tuple.condition_data,
                                                                        example_subject_tuple.indices, condition_names):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            if condition_plot_index == 1:
                plt.title(example_subjects[0], loc='center', size=8, fontfamily='arial')
            if condition_plot_index == 2:
                plt.title(example_subjects[1], loc='center', size=8, fontfamily='arial')
            plt.plot(x_lims, x_lims, 'k--')

            length_data = len(condition_data.PERCEIVED)
            jitter_values = [random() / 4 for _ in range(length_data)]
            x_data = np.array(condition_data.ACTUAL) + np.array(jitter_values)
            plt.plot(x_data, condition_data.PERCEIVED, 'o', color=color,
                     alpha=0.3, markersize=1, mec=None)

            intercept, slope = utils.calculate_regression_general(condition_data.ACTUAL,
                                                                  condition_data.PERCEIVED)

            x1 = x_lims[0]
            x2 = x_lims[1]
            y1 = slope * x1 + intercept
            y2 = slope * x2 + intercept

            plt.plot([x1, x2], [y1, y2], color=color, linewidth=1)
            plt.grid(axis='both')
            area = calculate_area.actual_vs_perceived(condition_data.ACTUAL, condition_data.PERCEIVED, experiment)

            legend_handles = [mpatches.Patch(color='grey', alpha=0.3, label=f'{area:4.2f}cm$^2$')]
            # plt.legend(handles=legend_handles, loc='upper left')

            x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                             color='grey', alpha=0.3, interpolate=True)
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                             color='grey', alpha=0.3, interpolate=True)

            plt.ylim([0, 15])
            plt.xlim([x1 - 1, x2 + 1])
            plt.yticks(list(range(0, 16, 3)), fontfamily='arial', fontsize=8)
            plt.xticks(list(range(2, 11, 2)))

            ax = plt.gca()
            # ax.yaxis.set_major_locator(MultipleLocator(3))
            # ax.yaxis.set_major_formatter('{x:.0f}')
            # ax.yaxis.set_minor_locator(MultipleLocator(1))
            # ax.yaxis.grid(True, which='minor')
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                           labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            if condition_plot_index in subplot_left_col:
                ax.tick_params(axis='y', which='both', left=True, labelleft=True)
                ax.spines['left'].set_visible(True)
                ax.set_ylabel('width', fontsize=8)
                # ax.text(text_x, 4.5, condition_name, rotation=90, fontsize=8)

            if condition_plot_index in subplot_bottom_row:
                ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)
                ax.spines['bottom'].set_visible(True)
                plt.xticks((list(range(2, 11, 2))), fontfamily='arial', fontsize=8)
                plt.xlabel('reference width')

    # plot the group regression lines in the rightmost subplots
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, condition_plot_index in zip(data_list, group_plot_indices):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            plt.grid(True)
            plt.plot(x_lims, x_lims, 'k--')
            if condition_plot_index == 3:
                plt.title('Regression lines\nAll subjects', loc='center', size=8, fontfamily='arial')

            x1, x2, y1, y2 = calculate_area.reg_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                               experiment)

            if subject_ID == example_subjects[0]:
                line_color = colors[0]
                line_width = 1
                order = 10
            elif subject_ID == example_subjects[1]:
                line_color = colors[1]
                line_width = 1
                order = 10
            else:
                line_color = 'darkgrey'
                line_width = 0.5
                order = 5

            plt.plot([x1, x2], [y1, y2], color=line_color, linewidth=line_width, zorder=order)
            plt.yticks(list(range(0, 16, 3)), fontfamily='arial', fontsize=8)
            plt.ylim([0, 15])
            plt.xticks(list(range(2, 11, 2)), fontfamily='arial', fontsize=8)
            plt.xlim([x1 - 1, x2 + 1])

            ax = plt.gca()
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                           labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            if condition_plot_index in subplot_bottom_row:
                ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)
                ax.spines['bottom'].set_visible(True)
                plt.xticks(list(range(2, 11, 2)), fontfamily='arial')
                plt.xlabel('width', fontsize=8)

    # plot dummy data + axis labels for cropping
    if experiment == 'exp2':
        plt.subplot(subplot_rows, subplot_cols, 12)
        plt.plot([4, 6], [6, 8])
        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))), fontfamily='arial', fontsize=8)
        plt.xlim([2, 10])
        plt.xlabel('width', fontsize=8)
        plt.gca().tick_params(axis='both', which='both', bottom=True, top=False, left=False, right=False,
                              labelbottom=True,
                              labeltop=False, labelleft=False, labelright=False)

    plt.tight_layout(h_pad=0.4, w_pad=0.9)
    plt.savefig(path, dpi=300)
    path_svg = Path(path.parts[0], path.parts[1], path.stem + '.svg')
    plt.savefig(path_svg)
    print(f'Saving {plot}')
    plt.close()


def consistency_between_conditions(all_subject_data, experiment):
    plot = f'consistency_between_conditions_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    plt.figure(figsize=(8 / 2.4, 8 / 2.4))
    plt.ylabel('Area difference $(cm^2)$', fontfamily='arial', fontsize=10)
    plt.grid(axis='y')
    y_points_list = []
    between_hands_areas, across_days_areas, within_day_areas = [], [], []

    x_points_base = [1.3, 1.6, 1.9]
    x_points_left = [1.255, 1.555, 1.855]
    x_points_right = [1.355, 1.655, 1.955]

    plt.xticks(x_points_base, labels=['across hands', 'within hands', 'within hands'], fontfamily='arial')

    for line_number, subject_data in enumerate(all_subject_data, start=1):
        jitter_values = [random() / 40 for _ in range(len(x_points_base))]
        if line_number < 15:
            x_points_jitter = np.array(x_points_right) + np.array(jitter_values)
        else:
            x_points_jitter = np.array(x_points_right) - np.array(jitter_values)

        d1_dom_area = calculate_area.actual_vs_perceived(subject_data.day1_dominant.ACTUAL,
                                                         subject_data.day1_dominant.PERCEIVED,
                                                         experiment)
        d1_non_dom_area = calculate_area.actual_vs_perceived(subject_data.day1_non_dominant.ACTUAL,
                                                             subject_data.day1_non_dominant.PERCEIVED,
                                                             experiment)
        d2_dom_1_area = calculate_area.actual_vs_perceived(subject_data.day2_dominant_1.ACTUAL,
                                                           subject_data.day2_dominant_1.PERCEIVED,
                                                           experiment)
        d2_dom_2_area = calculate_area.actual_vs_perceived(subject_data.day2_dominant_2.ACTUAL,
                                                           subject_data.day2_dominant_2.PERCEIVED,
                                                           experiment)

        dom_vs_non_dom_area = d1_dom_area - d1_non_dom_area
        between_hands_areas.append(dom_vs_non_dom_area)

        dom_d1_vs_d2_area = d1_dom_area - d2_dom_1_area
        across_days_areas.append(dom_d1_vs_d2_area)

        dom_d2_vs_d2_area = d2_dom_1_area - d2_dom_2_area
        within_day_areas.append(dom_d2_vs_d2_area)

        y_points = [dom_vs_non_dom_area, dom_d1_vs_d2_area, dom_d2_vs_d2_area]
        y_points_list.append(y_points)
        plt.plot(x_points_jitter, y_points, mfc='black', marker='^', alpha=0.4, markersize=4, linestyle='', mec='none')

    area_diff_list = [between_hands_areas, across_days_areas, within_day_areas]

    for x_point, area_list in zip(x_points_left, area_diff_list):
        mean, ci = utils.calculate_mean_ci(area_list)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='black', mec='black',
                     markersize=7)

    y_max, y_min = utils.max_min(y_points_list)
    plt.ylim([y_min - 1, (abs(y_min) + 1)])
    plt.yticks(list(range(-12, 14, 2)), fontfamily='arial')

    plt.text(0.15, 0.01, 'same day', fontsize=10, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.4, 0.01, '1 week apart', fontsize=10, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.71, 0.01, 'same day', fontsize=10, fontfamily='arial', transform=plt.gcf().transFigure)

    plt.plot([1, 3], [0, 0], color='black', linewidth=1)
    plt.xlim([1.19, 2.02])

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().spines['bottom'].set_visible(False)
    plt.gca().tick_params(axis='x', which='both', bottom=False)

    plt.savefig(path, dpi=300, bbox_inches='tight')
    text = colored(path, 'blue')
    print(f'Group consistency plots saved in {text}\n')
    plt.close()


def r2_area_plots(all_subject_data, subjects, experiment):
    plot = f'area_r2_group_plot_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    x_points = utils.x_points_group_plot(experiment)
    x_labels = utils.x_ticks_group_plot(experiment)
    params = plot_utils.r2_area_constants()

    if experiment == 'exp1':
        colors = params.exp_1_colors
        example_subjects = params.exp_1_subjects
    else:
        colors = params.exp_2_colors
        example_subjects = params.exp_2_subjects

    r2_means, r2_cis = utils.store_r2_means_CIs_per_condition(all_subject_data, experiment)
    area_means, area_cis = calculate_area.store_area_means_CIs_per_condition(all_subject_data, experiment)

    means_lists, ci_lists = [r2_means, area_means], [r2_cis, area_cis]

    plt.figure(figsize=(3.3, 4.3))
    for subject, subject_data in zip(subjects, all_subject_data):
        data_pair_tuples = utils.create_data_tuples(experiment, subject_data)
        y_points_r2 = []
        y_points_area = []

        if subject == example_subjects[0]:
            line_color = colors[0]
            line_width = 1.5
            order = 10
        elif subject == example_subjects[1]:
            line_color = colors[1]
            line_width = 1.5
            order = 10
        else:
            line_color = 'darkgrey'
            line_width = 1
            order = 5

        for tuple in data_pair_tuples:
            y_points_r2.append(utils.calculate_r2(tuple.ACTUAL, tuple.PERCEIVED))
            y_points_area.append(calculate_area.actual_vs_perceived(tuple.ACTUAL, tuple.PERCEIVED, experiment))

        y_point_lists = [y_points_r2, y_points_area]

        for subplot, y_points, y_label, y_tick, y_lim in zip(params.subplot_indices, y_point_lists, params.y_labels,
                                                             params.y_ticks, params.y_lims):
            plt.subplot(2, 1, subplot)
            plt.plot(x_points, y_points, color=line_color, alpha=0.7, linewidth=line_width, zorder=order)
            plt.ylabel(y_label, fontfamily=params.font, fontsize=8)
            plt.yticks(y_tick, fontfamily=params.font, fontsize=8)
            plt.ylim(y_lim)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            if subplot == 2:
                plt.xticks(x_points, labels=x_labels, fontfamily=params.font, fontsize=8)
            if experiment == 'exp1' and subplot == 1:
                plt.plot([1, 4], [params.r2_mean, params.r2_mean], linewidth=0.5, color='black', linestyle='--',
                         alpha=0.3, zorder=10)
                plt.fill_between(np.array([1, 4]), np.array([params.r2_ci_lower, params.r2_ci_lower]),
                                 np.array([params.r2_ci_upper, params.r2_ci_upper]), alpha=0.4, facecolor='peachpuff')
            if experiment == 'exp1' and subplot == 2:
                plt.plot([1, 4], [params.area_mean, params.area_mean], linewidth=0.5, color='black', linestyle='--',
                         alpha=0.3, zorder=10)
                plt.fill_between(np.array([1, 4]), np.array([params.area_ci_lower, params.area_ci_lower]),
                                 np.array([params.area_ci_upper, params.area_ci_upper]), alpha=0.4,
                                 facecolor='peachpuff')

    for mean_list, ci_list, subplot in zip(means_lists, ci_lists, params.subplot_indices):
        plt.subplot(2, 1, subplot)
        plt.grid(axis='y')
        plt.gca().tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                              labelbottom=False, labeltop=False, labelleft=True, labelright=False)
        if subplot == 2:
            plt.gca().tick_params(axis='both', which='both', labelbottom=True)
        for mean, ci, x_point in zip(mean_list, ci_list, x_points):
            plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='black', mec='black',
                         markersize=4, zorder=10)
        if subplot == 2 and experiment == 'exp1':
            ax = plt.gca()
            plt.text(0.28, 0.035, 'Day 1', fontsize=8, fontfamily=params.font, transform=plt.gcf().transFigure)
            plt.text(0.73, 0.035, 'Day 2', fontsize=8, fontfamily=params.font, transform=plt.gcf().transFigure)
            ax.annotate('', xy=(0, -0.12), xycoords='axes fraction', xytext=(0.45, -0.12),
                        arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
            ax.annotate('', xy=(0.6, -0.12), xycoords='axes fraction', xytext=(0.99, -0.12),
                        arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
        elif subplot == 1:
            plt.gca().xaxis.set_major_locator(MultipleLocator(1))
            plt.gca().xaxis.set_major_formatter('{x:.0f}')
    plt.tight_layout(h_pad=0.6, w_pad=0.9)
    plt.savefig(path, dpi=300)
    print(f'R2 and area per condition plots saved')
    plt.close()


def area_vs_r2_plot(all_subject_data, experiment):
    plot = f'measure_correlation_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    area_lists = calculate_area.group_areas(all_subject_data, experiment)
    r2_lists = utils.store_r2_tuples(all_subject_data, experiment)
    x_labels = utils.x_ticks_group_plot(experiment)

    if experiment == 'exp1':
        subplot_indices = [1, 2, 3, 4]
    else:
        subplot_indices = [1, 2, 3]

    plt.figure(figsize=(3.3, 6.5))
    for subplot_index, condition_r2_data, condition_area_data, condition_name in zip(subplot_indices, r2_lists, area_lists, x_labels):
        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)
        plt.subplot(subplot_indices[-1], subplot_indices[0], subplot_index)
        x_vals = np.array([0, 25])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color = 'black')
        plt.scatter(condition_area_data, condition_r2_data, marker='o', s = 4, c='grey', linewidths=0)

        plt.xlim(0, 25)
        plt.yticks([0.6, 0.65, 0.7, 0.75, 0.8, 0.85, 0.9, 0.95, 1], fontsize=8, fontfamily='arial')
        plt.xticks(fontsize=8, fontfamily='arial')
        plt.ylim(0.60, 1)
        plt.ylabel(condition_name, fontsize=8, fontfamily='arial')
        plt.grid()
        plt.text(17, 0.65, f'{slope:6.4f}')
        plt.gca().tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                       labelbottom=False, labeltop=False, labelleft=True, labelright=False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        if subplot_index == 4 and experiment == 'exp1' or subplot_index == 3 and experiment == 'exp2':
            plt.xlabel('Area (cm^2)', size = 8, fontfamily='arial')
            plt.gca().tick_params(axis='both', which='both', bottom=True, labelbottom=True)
            plt.gca().spines['bottom'].set_visible(True)
        plt.tight_layout()

    plt.tight_layout(h_pad=0.6)
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'Area vs r2 plots saved in {text}\n')
    plt.close()

def slope_comparison(all_subject_data, experiment):
    plot = f'slope_correlation_{experiment}'
    path = utils.create_article_plot_save_path(plot)

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
    plt.grid()

    intercept, slope = utils.calculate_regression_general(slopes_line_width, slopes_width_line)
    utils.regression_summary(slopes_line_width, slopes_width_line)

    x_vals = np.array([min(slopes_line_width)-0.25, max(slopes_line_width)+0.25])
    y_vals = intercept + slope * x_vals

    plt.plot(x_vals, y_vals, color='black')
    plt.scatter(slopes_line_width, slopes_width_line, marker='o', color='black', alpha=0.5, zorder=10, linewidths=0)
    plt.text(1.2, 2.0, f'm: {slope:4.2f}')

    plt.xlabel(f'Slope\n Line to width regression')
    plt.ylabel(f'Slope\n Width to line regression')
    plt.xlim((min(slopes_line_width) - 0.25), (max(slopes_line_width) + 0.25))
    plt.ylim((min(slopes_width_line) - 0.25), (max(slopes_width_line) + 0.25))
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'slope comparison saved in {text}\n')
    plt.close()