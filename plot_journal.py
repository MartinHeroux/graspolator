from collections import namedtuple
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from random import random
from pathlib import Path
from matplotlib.ticker import (MultipleLocator, AutoMinorLocator)

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

    plt.figure(figsize=(8.1/2.4, 12/2.4))
    # plot example subjects in left and centre subplot cols
    for column, (example_subject_tuple, color) in enumerate(zip(tuple_list, colors), start = 1):
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
            #plt.legend(handles=legend_handles, loc='upper left')

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
            #ax.yaxis.set_major_locator(MultipleLocator(3))
            #ax.yaxis.set_major_formatter('{x:.0f}')
            #ax.yaxis.set_minor_locator(MultipleLocator(1))
            #ax.yaxis.grid(True, which='minor')
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False, labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            if condition_plot_index in subplot_left_col:
                ax.tick_params(axis='y', which='both', left=True, labelleft=True)
                ax.spines['left'].set_visible(True)
                ax.set_ylabel('width', fontsize=8)
                #ax.text(text_x, 4.5, condition_name, rotation=90, fontsize=8)

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

            plt.plot([x1, x2], [y1, y2], color=line_color, linewidth=line_width, zorder = order)
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
        plt.plot([4,6], [6,8])
        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))), fontfamily='arial', fontsize=8)
        plt.xlim([2, 10])
        plt.xlabel('width', fontsize=8)
        plt.gca().tick_params(axis='both', which='both', bottom=True, top=False, left=False, right=False, labelbottom=True,
                       labeltop=False, labelleft=False, labelright=False)

    plt.tight_layout(h_pad=0.4, w_pad=0.9)
    plt.savefig(path, dpi=300)
    path_svg = Path(path.parts[0], path.parts[1], path.stem + '.svg')
    plt.savefig(path_svg)
    print(f'Saving {plot}')
    plt.close()

#def r2_area_plots(all_subject_data, subjects, experiment):
