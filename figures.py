import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from termcolor import colored

import utils
import calculate_area


def generate(all_subject_data, subjects, experiment):

    figure_1_and_5(all_subject_data, subjects, experiment)
    figure_2_and_6(all_subject_data, subjects, experiment)

    if experiment == 'exp2':
        figure_3(all_subject_data, experiment)
        figure_4(all_subject_data, experiment)

    if experiment == 'exp1':
        figure_7(all_subject_data, experiment)


def figure_1_and_5(all_subject_data, subjects, experiment):
    plot = 'Example participants and group regression summary'
    
    if experiment == 'exp1':
        figure = 'Figure 5'
        subject_1_ID = 'SUB03L'
        subject_2_ID = 'SUB11R'
        data_list = utils.store_example_subject_data_exp1(all_subject_data, subjects, subject_1_ID, subject_2_ID)

    else:
        figure = 'Figure 1'
        subject_1_ID = 'sub02'
        subject_2_ID = 'sub29'
        data_list = utils.store_example_subject_data_exp2(all_subject_data, subjects, subject_1_ID, subject_2_ID)

    utils.write_plot_header(experiment, figure, plot)
    path = utils.create_figure_save_path(figure)

    subplot_rows = 4
    subplot_cols = 3
    plot_indices_list = [[1, 4, 7, 10], [2, 5, 8, 11]]
    y_lim = [0, 16]
    y_ticks = list(range(0, 16, 2))

    # set up experiment specific parameters
    if experiment == 'exp1':
        condition_names = ['day 1 dominant', 'day 1 non-dominant', 'day 2 dominant 1', 'day 2 dominant 2']
        x_lims = [1, 11]
        x_data_lims = [2, 10]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9, 12]
        colors = ['royalblue', 'darkblue']
        example_subjects = [subject_1_ID, subject_2_ID]
        x_ticks = list(range(2, 11, 2))
        label_list = ['A', 'B', 'C', 'D']

    else:
        condition_names = ['line to width', 'width to line', 'width to width', 'dummy_data']
        x_lims = [1, 11]
        x_data_lims = [3, 9]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9]
        colors = ['darkred', 'red']
        example_subjects = [subject_1_ID, subject_2_ID]
        x_ticks = list(range(2, 11, 2))
        label_list = ['A', 'B', 'C']

    plt.figure(figsize=(17.5 / 2.4, 22 / 2.4))
    # plot example subjects in left and centre subplot cols
    for column, (example_subject_data, color, plot_indices, example_subject) in enumerate(zip(data_list, colors,
                                                                                              plot_indices_list,
                                                                                              example_subjects), start=1):
        utils.write_example_subject_name(experiment, example_subject)
        # plot each condition data
        for condition_data, condition_plot_index, condition_name in zip(example_subject_data, plot_indices, condition_names):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            if condition_plot_index == 1:
                plt.title(example_subjects[0], loc='center', size=8, fontfamily='arial')
            if condition_plot_index == 2:
                plt.title(example_subjects[1], loc='center', size=8, fontfamily='arial')

            intercept, slope = utils.calculate_regression_general(condition_data.ACTUAL, condition_data.PERCEIVED)
            area = calculate_area.actual_vs_perceived(condition_data.ACTUAL, condition_data.PERCEIVED, experiment)

            ax = plt.gca()

            plt.plot(x_lims, x_lims, 'k--', linewidth=1) # plot line of 'reality'
            utils.plot_data_scatter(ax, condition_data.ACTUAL, condition_data.PERCEIVED, color)
            utils.plot_regression_line(ax, intercept, slope, color, x_data_lims[0], x_data_lims[1])
            utils.shade_area(ax, intercept, slope, x_data_lims[0], x_data_lims[1])
            utils.write_example_subject_results(experiment, example_subject, condition_name, intercept, slope, area)

            legend_handles = [mpatches.Patch(color='lightgrey', alpha=0.5, label=f'{area:3.1f}cm$^2$')]
            plt.legend(handles=legend_handles, loc='upper left', facecolor='white', framealpha=1, fontsize=8,
                       handlelength=1, handleheight=1, edgecolor='none')


            utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lim, None, None)
            utils.draw_ax_spines(ax, False, False, False, False)
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                           labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            # draw axes, labels, and ticks for left column and bottom row subplots
            if condition_plot_index in subplot_left_col:
                ax.tick_params(axis='y', which='both', left=True, labelleft=True)
                ax.spines['left'].set_visible(True)
                if condition_plot_index == 4 and experiment == 'exp2':
                    ax.set_ylabel('Perceived width (cm)', fontfamily='arial', fontsize=8)
                elif condition_plot_index == 7 and experiment == 'exp1':
                    ax.set_ylabel('                                              Perceived width (cm)',
                                  fontfamily='arial', fontsize=8)

            if condition_plot_index in subplot_bottom_row:
                ax.tick_params(axis='x', which='both', bottom=True, labelbottom=True)
                ax.spines['bottom'].set_visible(True)
                if condition_plot_index == 11:
                    plt.xlabel('Stimulus width (cm)', fontsize=8, fontfamily='arial')


    # plot group regression lines in the right subplot column
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, condition_plot_index, label in zip(data_list, group_plot_indices, label_list):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)

            if condition_plot_index == 3:
                plt.title('Regression lines\nAll subjects', loc='center', size=8, fontfamily='arial')

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

            intercept, slope = utils.calculate_regression_general(condition_tuple.ACTUAL, condition_tuple.PERCEIVED)
            alpha = 0.7

            ax = plt.gca()

            plt.plot(x_lims, x_lims, 'k--', linewidth=1)
            utils.plot_regression_line(ax, intercept, slope, line_color, x_data_lims[0], x_data_lims[1], alpha, line_width, order)

            utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lim, None, None)
            utils.draw_ax_spines(ax, False, False, False, False)
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                           labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            # plot condition labels (A, B, C, +/- D) + turn grid back on
            plt.text(11.5, 14, label, fontsize=12, fontfamily='arial')
            plt.grid(True, axis='both', linewidth=0.5, color='lightgrey')

            # draw axes and ticks for bottom row
            if condition_plot_index in subplot_bottom_row:
                plt.gca().spines['bottom'].set_visible(True)
                plt.gca().tick_params(axis='x', which='both', bottom=True, labelbottom=True)

    # plot dummy data + axis labels for cropping
    # TODO remove for final version
    if experiment == 'exp2':
        plt.subplot(subplot_rows, subplot_cols, 12)
        plt.plot([4, 6], [6, 8])
        plt.xticks(x_ticks, fontfamily='arial', fontsize=8)
        plt.xlim([x_lims[0], x_lims[1]])
        plt.gca().tick_params(axis='both', which='both', bottom=True, top=False, left=False, right=False,
                              labelbottom=True,
                              labeltop=False, labelleft=False, labelright=False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)

    plt.tight_layout(h_pad=0.4, w_pad=0.9)
    plt.savefig(path, dpi=300)
    #path_svg = Path(path.parts[0], path.parts[1], path.stem + '.svg')
    #plt.savefig(path_svg)
    #print(f'{experiment} example subjects and group regressions saved in in {path_svg}\n')
    text = colored(path, 'blue')
    print(f'{experiment} example subjects and group regressions saved in in {text}\n')
    plt.close()


def figure_7(all_subject_data, experiment):
    plot = 'Area difference between conditions'
    figure = 'Figure_7'
    path = utils.create_figure_save_path(figure)

    utils.write_plot_header(experiment, figure, plot)

    x_ticks = [1.3, 1.6, 1.9]
    x_points_left = [1.27, 1.57, 1.87]
    x_points_right = [1.33, 1.63, 1.93]
    x_tick_labels = ['Across hands', 'Within hand', 'Within hand']
    x_descriptors = ['Same day', '1 week apart', 'Same day']
    x_lim = [1.19, 2.02]
    y_lim = [-13, 13]
    y_ticks = list(range(-12, 13, 3))
    y_label = 'Area difference (cm$^2$)'

    between_hands_areas, across_days_areas, within_day_areas = [], [], []

    plt.figure(figsize=(8 / 2.4, 8 / 2.4))
    ax = plt.gca()

    for line_number, subject_data in enumerate(all_subject_data, start=1):
        area_comparison_list = calculate_area.return_condition_comparison_areas(subject_data, experiment)
        utils.plot_comparison_areas(ax, line_number, x_ticks, x_points_right, area_comparison_list)

        between_hands_areas.append(area_comparison_list[0])
        across_days_areas.append(area_comparison_list[1])
        within_day_areas.append(area_comparison_list[2])

    area_diff_list = [between_hands_areas, across_days_areas, within_day_areas]

    for x_point, area_list, label, descriptor in zip(x_points_left, area_diff_list, x_tick_labels, x_descriptors):
        mean, ci = utils.calculate_mean_ci(area_list)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='black', mec='black',
                     markersize=3.5, elinewidth=1)
        utils.write_mean_ci_result(experiment, mean, ci, label, descriptor)

    utils.set_ax_parameters(ax, x_ticks, y_ticks, x_tick_labels, y_ticks, x_lim, y_lim, None, y_label)
    utils.draw_ax_spines(ax, left=True, right=False, top=False, bottom=True)
    plt.grid(which='both', axis='x', linewidth=0.5, color='lightgrey') # turn grid off for x axis

    plt.text(0.15, 0.01, 'Same day', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.41, 0.01, '1 week apart', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.71, 0.01, 'Same day', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)

    plt.plot([1, 3], [0, 0], color='black', linewidth=0.5)

    plt.savefig(path, dpi=300, bbox_inches='tight')
    text = colored(path, 'blue')
    print(f'Area_difference_between_conditions saved in {text}\n')
    plt.close()


def figure_2_and_6(all_subject_data, subjects, experiment):
    plot = 'Area and R^2 Group Summary'
    if experiment == 'exp1':
        figure = 'Figure_6'
    else:
        figure = 'Figure_2'
    path = utils.create_figure_save_path(figure)

    utils.write_plot_header(experiment, figure, plot)

    x_points, x_lims = utils.x_points_group_plot(experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)
    plot_text = ['B', 'A']
    results_headers = ['R^2', 'Area (cm2)']
    params = utils.r2_area_constants()

    if experiment == 'exp1':
        colors = params.exp_1_colors
        example_subjects = params.exp_1_subjects
        text_x = 4.3
        text_y_plot_1 = 25
        text_y_plot_2 = 1
        y_lims = [(0.7, 1), (0, 26)]
        condition_names = ['day 1 dominant', 'day 1 non-dominant', 'day 2 dominant 1', 'day 2 dominant 2']
    else:
        colors = params.exp_2_colors
        example_subjects = params.exp_2_subjects
        text_x = 3.3
        text_y_plot_1 = 20
        text_y_plot_2 = 1
        y_lims = [(0.6, 1), (0, 20)]
        condition_names = ['Line-to-width', 'Width-to-line', 'Width-to-width']

    r2_means, r2_cis = utils.store_condition_r2_means_and_cis(all_subject_data, experiment)
    area_means, area_cis = calculate_area.store_condition_area_means_and_cis(all_subject_data, experiment)
    means_lists, ci_lists = [r2_means, area_means], [r2_cis, area_cis]

    plt.figure(figsize=(3.3, 4.3))
    for subject, subject_data in zip(subjects, all_subject_data):
        data_pairs = utils.create_data_tuples(experiment, subject_data)
        y_points_r2 = []
        y_points_area = []

        if subject == example_subjects[0]:
            line_color, line_width, order, alpha = colors[0], 0.75, 10, 0.3
        elif subject == example_subjects[1]:
            line_color, line_width, order, alpha = colors[1], 0.75, 10, 0.3
        else:
            line_color, line_width, order, alpha = 'grey', 0.5, 5, 0.3

        for pair in data_pairs:
            y_points_r2.append(utils.calculate_r2(pair.ACTUAL, pair.PERCEIVED))
            y_points_area.append(calculate_area.actual_vs_perceived(pair.ACTUAL, pair.PERCEIVED, experiment))

        y_point_lists = [y_points_r2, y_points_area]

        for subplot, y_points, y_label, y_tick, y_lim, text in zip(params.subplot_indices, y_point_lists,
                                                                   params.y_labels,
                                                                   params.y_ticks, y_lims, plot_text):
            plt.subplot(2, 1, subplot)
            plt.plot(x_points, y_points, color=line_color, alpha=alpha, linewidth=line_width, zorder=order)

            ax = plt.gca()
            utils.set_ax_parameters(ax, x_points, y_tick, x_labels, y_tick, x_lims, y_lim, None, y_label)

            if experiment == 'exp1' and subplot == 2:
                plt.ylim(0.75, 1)

            if subplot == 1:
                plt.text(text_x, text_y_plot_1, text, fontsize=11, fontfamily='arial')
                ax.tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                               labelbottom=False, labeltop=False, labelleft=True, labelright=False)
                utils.draw_ax_spines(ax, True, False, False, False)
            else:
                plt.text(text_x, text_y_plot_2, text, fontsize=11, fontfamily='arial')
                ax.tick_params(axis='both', which='both', bottom=True, labelbottom=True)
                utils.draw_ax_spines(ax, True, False, False, True)


    for mean_list, ci_list, subplot, y_label in zip(means_lists, ci_lists, params.subplot_indices, results_headers):
        plt.subplot(2, 1, subplot)
        plt.grid(axis='y', linewidth=0.5, color='lightgrey')
        for mean, ci, x_point, x_label in zip(mean_list, ci_list, x_points, condition_names):
            plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="o", markerfacecolor='black', mec='black',
                         markersize=3, linewidth=1, zorder=11)
            utils.write_mean_ci_result(experiment, mean, ci, y_label, x_label)

        ax = plt.gca()
        utils.add_plot_text(ax, subplot, experiment)
        utils.add_plot_shading(ax, subplot, experiment, params.r2_ci_lower, params.r2_ci_upper, params.area_ci_lower, params.area_ci_upper)

    plt.tight_layout(h_pad=0.6, w_pad=0.9)
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'R2 and area per condition plots saved in {text}\n')
    plt.close()


def figure_3(all_subject_data, experiment):
    figure = 'Figure_3'
    plot = 'Area vs R^2 Regression'
    path = utils.create_figure_save_path(figure)

    utils.write_plot_header(experiment, figure, plot)

    area_lists = calculate_area.group_areas(all_subject_data, experiment)
    r2_lists = utils.store_r2_lists(all_subject_data, experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)

    if experiment == 'exp1':
        subplot_indices = [1, 2, 3, 4]
        text_labels = ['A', 'B', 'C', 'D']
    else:
        subplot_indices = [1, 2, 3]
        text_labels = ['A', 'B', 'C']

    x_lims, y_lims = (0, 20), (0.6, 1)
    x_ticks, y_ticks = [0, 5, 10, 15, 20], [0.6, 0.7, 0.8, 0.9, 1]
    x_label, y_label = None, 'R$^2$'

    plt.figure(figsize=(3.3, 7))
    for subplot_index, condition_r2_data, condition_area_data, condition_name, text in zip(subplot_indices, r2_lists,
                                                                                     area_lists, x_labels, text_labels):
        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)

        plt.subplot(subplot_indices[-1], subplot_indices[0], subplot_index)
        x_vals = np.array([0, max(condition_area_data)])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color='black', linewidth=1, zorder=11)
        plt.scatter(condition_area_data, condition_r2_data, c='gray', marker='o', alpha=0.6, s=5, linewidths=0,
                    zorder=10)

        ax = plt.gca()
        utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lims, x_label, y_label)
        utils.draw_ax_spines(ax, True, False, False, False)
        ax.tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                              labelbottom=False, labeltop=False, labelleft=True, labelright=False)

        # draw axes and ticks for bottom subplot
        if subplot_index == 4 and experiment == 'exp1' or subplot_index == 3 and experiment == 'exp2':
            plt.xlabel('Area (cm$^2$)', size=8, fontfamily='arial')
            ax.tick_params(axis='both', which='both', bottom=True, labelbottom=True)
            ax.spines['bottom'].set_visible(True)

        # label subplot letter (A, B, C, +/- D)
        plt.text(22, 1, text, fontsize = 12, fontfamily = 'arial')

        utils.write_regression_results(experiment, condition_area_data, condition_r2_data, intercept, slope, condition_name)

        #plt.tight_layout()

    plt.tight_layout(h_pad=0.9)
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'{experiment} area vs r2 plots saved in {text}\n')
    plt.close()


def figure_4(all_subject_data, experiment):
    figure = 'Figure_4'
    plot = 'Slope regression: Line-to-width vs. width-to-line'
    path = utils.create_figure_save_path(figure)
    condition_name = 'line-to-width vs width-to-line'

    utils.write_plot_header(experiment, figure, plot)

    slopes_line_width = []
    slopes_width_line = []

    x_lims, y_lims = (0.4, 1.6), (0.4, 2.0)
    x_ticks, y_ticks = [0.4, 0.8, 1.2, 1.6, 2], [0.4, 0.8, 1.2, 1.6, 2]
    x_label, y_label = 'Line-to-width slope', 'Width-to-line slope'

    for subject_data in all_subject_data:
        intercept_line_width, slope_line_width = utils.calculate_regression_general(subject_data.LINE_WIDTH.ACTUAL,
                                                                                    subject_data.LINE_WIDTH.PERCEIVED)
        intercept_width_line, slope_width_line = utils.calculate_regression_general(subject_data.WIDTH_LINE.ACTUAL,
                                                                                    subject_data.WIDTH_LINE.PERCEIVED)

        slopes_line_width.append(slope_line_width)
        slopes_width_line.append(slope_width_line)

    plt.figure(figsize=(3.3, (7 / 2.6)))

    intercept, slope = utils.calculate_regression_general(slopes_line_width, slopes_width_line)

    # print and plot results without outlier
    for slope_1, slope_2 in zip(slopes_line_width, slopes_width_line):
        if slope_2 > 1.7:
            plt.plot(slope_1, slope_2, marker='o', color='white', markeredgecolor='gray', markersize=2, markeredgewidth=0.5)
            index = slopes_width_line.index(slope_2)
            slope_line_width_2 = slopes_line_width
            slope_width_line_2 = slopes_width_line
            slope_line_width_2.pop(index)
            slope_width_line_2.pop(index)
            intercept_2, slope_2 = utils.calculate_regression_general(slope_line_width_2, slope_width_line_2)

    utils.write_regression_results(experiment, slopes_line_width, slopes_width_line, intercept, slope, condition_name)
    utils.write_regression_results(experiment, slope_line_width_2, slope_width_line_2, intercept_2, slope_2, 'Outlier removed')

    x_vals = np.array([min(slopes_line_width) - 0.25, max(slopes_line_width) + 0.25])
    y_vals = intercept + slope * x_vals

    # plot regression line
    plt.plot(x_vals, y_vals, color='black', linewidth=1, zorder=10)
    # plot individual slope values
    plt.scatter(slopes_line_width, slopes_width_line, c='gray', marker='o', alpha=0.6, s=5, zorder=5, linewidths=0)

    ax = plt.gca()
    utils.draw_ax_spines(ax, True, False, False, True)
    utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lims, x_label, y_label)

    plt.tight_layout()

    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'slope comparison saved in {text}\n')
    plt.close()
