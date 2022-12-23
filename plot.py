from random import random
import numpy as np
from matplotlib import pyplot as plt, patches as mpatches
from matplotlib.lines import Line2D


import area
import utils
from utils import create_individual_plot_save_path

KATHY = 'exp1'


def individual_scatterplots(all_subject_data, subjects, experiment):
    print('\n\nCreating individual scatter and regression plots. Note - this takes a while.\n')
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        scatterplots_and_reg_lines(subject_ID, subject_data, experiment)

    print(f'All individual scatter and regression plots saved in ./plots/individual_plots\n')
    dashes = '-' * 60
    print(f'\n{dashes}\n')


def individual_error_plots(all_subject_data, subjects, experiment):
    print('Creating individual error plots. Note - this takes a while.\n')
    for subject_ID, current_subject_data in zip(subjects, all_subject_data):
        areas_between_regression_and_reality(subject_ID, current_subject_data, experiment)

    print(f'All individual areas between regression line and reality saved in ./plots/individual_plots\n')
    dashes = '-' * 60
    print(f'\n{dashes}\n')


def scatterplots_and_reg_lines(subject_ID, subject_data, experiment):
    if experiment == 'exp1':
        manuscript_experiment = 'exp2'
    else:
        manuscript_experiment = 'exp1'

    plot = f'scatterplots_{manuscript_experiment}'
    path = create_individual_plot_save_path(plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)

    if experiment == KATHY:
        subplot_width = 4
        subplot_length = 1
        x_lims = [2, 10]
        fig_size = [7, 20]
    else:
        subplot_width = 1
        subplot_length = 3
        x_lims = [3, 9]
        fig_size = [15, 5]

    plt.figure(figsize=fig_size)
    plt.suptitle(str(subject_ID + ' Scatterplot + Regression Line'))
    for condition_tuple in data_list:
        plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
        plt.plot([2, 10],
                 [2, 10],
                 'k--')
        length_data = len(condition_tuple.PERCEIVED)
        jitter_values = [random() / 4 for _ in range(length_data)]
        x_data = np.array(condition_tuple.ACTUAL) + np.array(jitter_values)
        color = 'firebrick'
        plt.plot(x_data, condition_tuple.PERCEIVED, 'o', color = color, alpha=0.5)

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL,
                                                              condition_tuple.PERCEIVED)

        legend_handles = [Line2D([0], [0], color=color, lw=2,
                                 label=f'Regression \n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], color='black', linestyle='--', label='Reality (y = x)', lw=2),
                          Line2D([0], [0], color=color, marker = 'o', linestyle = 'none', alpha=0.3, label=f'Trial (n = {length_data})')]

        # Creating points to plot regression line [x1, y1][x2, y2]
        x1 = x_lims[0]
        x2 = x_lims[1]
        y1 = slope * x1 + intercept
        y2 = slope * x2 + intercept
        if y2 < 15:
            y_max = 15
        else:
            y_max = y2
        plt.plot([x1, x2], [y1, y2], color=color)
        plt.legend(handles = legend_handles, loc = 'upper left')
        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.ylim([0, y_max])
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.grid()

    plt.savefig(path, dpi=300, bbox_inches='tight')
    #text = colored(f'{path}', 'blue')
    #print(f'scatterplot and regression line saved for {subject_ID} in {text}')
    plt.close()


def areas_between_regression_and_reality(subject_ID, subject_data, experiment):
    if experiment == 'exp2':
        manuscript_experiment = 'exp1'
    else:
        manuscript_experiment = 'exp2'

    plot = f'error_plots_{manuscript_experiment}'
    path = create_individual_plot_save_path(plot, subject_ID)
    data_list = utils.create_data_tuples(experiment, subject_data)

    if experiment == KATHY:
        subplot_width = 4
        subplot_length = 1
        x_lims = [2, 10]
        fig_size = [7, 20]
    else:
        subplot_width = 1
        subplot_length = 3
        x_lims = [3, 9]
        fig_size = [15, 5]

    plt.figure(figsize=fig_size)
    plt.suptitle(subject_ID + ' Area Plots (reality vs. regression lines)')
    for condition_tuple in data_list:
        plt.subplot(subplot_width, subplot_length, condition_tuple.PLOT_INDEX)
        plt.plot([2, 10],
                 [2, 10],
                 'k--')

        intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
        x1, x2, y1, y2 = utils.return_regression_line_endpoints(condition_tuple.ACTUAL, condition_tuple.PERCEIVED,
                                                           experiment)
        if y2 < 15:
            y_max = 14
        else:
            y_max = y2

        area_result = area.between_regression_and_reality_absolute(condition_tuple.ACTUAL, condition_tuple.PERCEIVED, experiment)
        #area = calculate_area.normalised(condition_tuple.ACTUAL, condition_tuple.PERCEIVED, 'comparison')
        color = 'firebrick'

        x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])
        plt.plot([x1, x2], [y1, y2], color=color)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                         color=color, alpha=0.3, interpolate=True)
        plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                         color=color, alpha=0.3, interpolate=True)

        legend_handles = [Line2D([0], [0], color='royalblue', lw=2,
                                 label=f'Regression Line\n(y = {slope:4.2f}*x + {intercept:4.2f})'),
                          Line2D([0], [0], color='black', linestyle='--', label='Reality Line (y = x)', lw=2),
                          mpatches.Patch(color=color, alpha=0.3, label=f'Area = {area_result:4.2f}')]

        plt.xticks(list(range(x_lims[0], (x_lims[1] + 1))))
        plt.xlim([x1 - 1, x2 + 1])
        plt.yticks(list(range(0, int(y_max + 1))))
        plt.ylim(0, 15)
        plt.grid()
        plt.title(condition_tuple.NAME, loc='right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')
        plt.legend(handles=legend_handles, loc='upper left')

    plt.savefig(path)
    #text = colored(f'{path}', 'blue')
    #print(f'area between regression and reality saved for {subject_ID} in {text}')
    plt.close()





