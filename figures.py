import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from random import random
from pathlib import Path
from matplotlib.ticker import MultipleLocator
from termcolor import colored

import utils
import calculate_area

constants = utils.create_general_constants()
plot_constants = utils.create_plot_constants()


def generate(all_subject_data, subjects, experiment):
    # TODO rename to match figure numbers
    example_subjects_group_reg_summary(all_subject_data, subjects, experiment)
    r2_area_plots(all_subject_data, subjects, experiment)

    if experiment == 'exp1':
        consistency_between_conditions(all_subject_data, experiment)

    if experiment == 'exp2':
        slope_comparison(all_subject_data, experiment)
        area_vs_r2_plot(all_subject_data, experiment)


## panel figure of individual subjects and group reg lines

def example_subjects_group_reg_summary(all_subject_data, subjects, experiment):

    results = open(f'results_{experiment}.txt', 'a')

    if experiment == 'exp1':
        plot = f'figure_5_{experiment}'
        subject_1_ID = 'SUB03L'
        subject_2_ID = 'SUB11R'
        data_list = utils.store_example_subject_data_exp1(all_subject_data, subjects, subject_1_ID, subject_2_ID)
        results.write('\nFigure 5: Example subjects and group regression summary\n')

    else:
        plot = f'figure_1_{experiment}'
        subject_1_ID = 'sub02'
        subject_2_ID = 'sub29'
        data_list = utils.store_example_subject_data_exp2(all_subject_data, subjects, subject_1_ID, subject_2_ID)
        results.write('\nFigure 1: Example subjects and group regression summary\n')


    path = utils.create_article_plot_save_path(plot)

    subplot_rows = 4
    subplot_cols = 3
    plot_indices_list = [[1, 4, 7, 10], [2, 5, 8, 11]]

    # set up experiment specific parameters
    if experiment == 'exp1':
        condition_names = ['dominant', 'non-dominant', 'dominant', 'dominant']
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

        results.write(f'{example_subject}\n')

        for condition_data, condition_plot_index, condition_name in zip(example_subject_data,
                                                                        plot_indices,
                                                                        condition_names):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            if condition_plot_index == 1:
                plt.title(example_subjects[0], loc='center', size=8, fontfamily='arial')
            if condition_plot_index == 2:
                plt.title(example_subjects[1], loc='center', size=8, fontfamily='arial')
            plt.plot(x_lims, x_lims, 'k--', linewidth=1)

            length_data = len(condition_data.PERCEIVED)
            jitter_values = [random() / 4 for _ in range(length_data)]
            x_data = (np.array(condition_data.ACTUAL) - 0.1) + np.array(jitter_values)
            plt.plot(x_data, condition_data.PERCEIVED, 'o', color=color,
                     alpha=0.5, markersize=3, markeredgecolor=None, markeredgewidth=0)

            intercept, slope = utils.calculate_regression_general(condition_data.ACTUAL,
                                                                  condition_data.PERCEIVED)

            x1 = x_data_lims[0]
            x2 = x_data_lims[1]
            y1 = slope * x1 + intercept
            y2 = slope * x2 + intercept

            plt.plot([x1, x2], [y1, y2], color=color, linewidth=1)
            plt.grid(axis='both', linewidth=0.5, color='lightgrey')
            area = calculate_area.actual_vs_perceived(condition_data.ACTUAL, condition_data.PERCEIVED, experiment)

            results.write(f'{condition_name}:   intercept = {intercept:4.2f}   slope = {slope:4.2f}     area = {area:4.2f}cm^2\n')

            legend_handles = [mpatches.Patch(color='lightgrey', alpha=0.5, label=f'{area:3.1f}cm$^2$')]
            plt.legend(handles=legend_handles, loc='upper left', facecolor='white', framealpha=1, fontsize=8,
                       handlelength=1, handleheight=1, edgecolor='none')

            x_colour_points, y_points_reality, y_points_reg = np.array([x1, x2]), np.array([x1, x2]), np.array([y1, y2])

            plt.ylim([0, 16])
            plt.xlim([x_lims[0], x_lims[1]])
            plt.yticks(list(range(0, 16, 2)), fontfamily='arial', fontsize=8)
            plt.xticks(x_ticks)

            ax = plt.gca()
            ax.tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                           labelbottom=False, labeltop=False, labelleft=False, labelright=False)
            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)

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
                plt.xticks(x_ticks, fontfamily='arial', fontsize=8)
                if condition_plot_index == 11:
                    plt.xlabel('Stimulus width (cm)', fontsize=8, fontfamily='arial')

            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality > y_points_reg),
                             color='lightgrey', alpha=0.5, interpolate=True)
            plt.fill_between(x_colour_points, y_points_reality, y_points_reg, where=(y_points_reality < y_points_reg),
                             color='lightgrey', alpha=0.5, interpolate=True)

    # plot the group regression lines in the rightmost subplots
    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, condition_plot_index, label in zip(data_list, group_plot_indices, label_list):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            plt.plot(x_lims, x_lims, 'k--', linewidth=1)
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

            plt.plot([x1, x2], [y1, y2], color=line_color, linewidth=line_width, zorder=order, alpha=0.7)
            plt.yticks(list(range(0, 16, 2)), fontfamily='arial', fontsize=8)
            plt.ylim([0, 16])
            plt.xticks(x_ticks, fontfamily='arial', fontsize=8)
            plt.xlim([x_lims[0], x_lims[1]])

            # plot condition labels
            plt.text(11.5, 14, label, fontsize=12, fontfamily='arial')

            plt.gca().grid(True, linewidth=0.5, color='lightgrey')

            plt.gca().spines['bottom'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['left'].set_visible(False)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().tick_params(axis='both', which='both', bottom=False, top=False, left=False, right=False,
                                  labelbottom=False, labeltop=False, labelleft=False, labelright=False)

            if condition_plot_index in subplot_bottom_row:
                plt.gca().spines['bottom'].set_visible(True)
                plt.gca().tick_params(axis='x', which='both', bottom=True, labelbottom=True)
                plt.xticks(x_ticks, fontfamily='arial')

    # plot dummy data + axis labels for cropping
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
    path_svg = Path(path.parts[0], path.parts[1], path.stem + '.svg')
    plt.savefig(path_svg)
    print(f'{experiment} example subjects and group regressions saved in in {path_svg}\n')
    text = colored(path, 'blue')
    print(f'{experiment} example subjects and group regressions saved in in {text}\n')
    results.close()
    plt.close()


def consistency_between_conditions(all_subject_data, experiment):
    plot = f'figure_7_{experiment}'
    path = utils.create_article_plot_save_path(plot)
    results = open(f'results_{experiment}.txt', 'a')

    results.write('\nFigure 7: Consistency between conditions\n')

    plt.figure(figsize=(8 / 2.4, 8 / 2.4))
    plt.ylabel('Area difference (cm$^2$)', fontfamily='arial', fontsize=8)
    plt.grid(axis='y', linewidth=0.5, color='lightgrey')
    y_points_list = []
    between_hands_areas, across_days_areas, within_day_areas = [], [], []

    x_points_base = [1.3, 1.6, 1.9]
    x_points_left = [1.27, 1.57, 1.87]
    x_points_right = [1.33, 1.63, 1.93]
    x_labels = ['Across hands', 'Within hands', 'Within hands']

    plt.xticks(x_points_base, labels=x_labels, fontfamily='arial', fontsize=8)

    for line_number, subject_data in enumerate(all_subject_data, start=1):
        jitter_values = [random() / 60 for _ in range(len(x_points_base))]
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
        plt.plot(x_points_jitter, y_points, mfc='gray', marker='^', alpha=0.6, markersize=3, linestyle='', mec='none')

    area_diff_list = [between_hands_areas, across_days_areas, within_day_areas]

    for x_point, area_list, label in zip(x_points_left, area_diff_list, x_labels):
        mean, ci = utils.calculate_mean_ci(area_list)
        plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="^", markerfacecolor='black', mec='black',
                     markersize=3.5, elinewidth=1)
        ci_lower = mean - ci
        ci_upper = mean + ci
        results.write(f'{label}:    mean: {mean:4.2f}    ci: [{ci_lower:4.2f} - {ci_upper:4.2f}]\n')

    plt.ylim([-13, 13])
    plt.yticks(list(range(-12, 13, 3)), fontfamily='arial', fontsize=8)

    plt.text(0.15, 0.01, 'Same day', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.41, 0.01, '1 week apart', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)
    plt.text(0.71, 0.01, 'Same day', fontsize=8, fontfamily='arial', transform=plt.gcf().transFigure)

    plt.plot([1, 3], [0, 0], color='black', linewidth=0.5)
    plt.xlim([1.19, 2.02])

    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.gca().tick_params(axis='x', which='both', bottom=True)

    plt.savefig(path, dpi=300, bbox_inches='tight')
    text = colored(path, 'blue')
    print(f'Group consistency plots saved in {text}\n')
    results.close()
    plt.close()


def r2_area_plots(all_subject_data, subjects, experiment):
    if experiment == 'exp1':
        plot = f'figure_6_{experiment}'
        y_lims = [(0.7, 1), (0, 26)]
    else:
        plot = f'figure_2_{experiment}'
        y_lims = [(0.6, 1), (0, 20)]
    path = utils.create_article_plot_save_path(plot)

    x_points = utils.x_points_group_plot(experiment)
    x_labels = utils.x_ticks_group_plot(experiment)
    plot_text = ['B', 'A']
    params = utils.r2_area_constants()

    if experiment == 'exp1':
        colors = params.exp_1_colors
        example_subjects = params.exp_1_subjects
        text_x = 4.3
        text_y_plot_1 = 25
        text_y_plot_2 = 1
    else:
        colors = params.exp_2_colors
        example_subjects = params.exp_2_subjects
        text_x = 3.3
        text_y_plot_1 = 20
        text_y_plot_2 = 1

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
            line_width = 0.75
            order = 10
            alpha = 0.3
        elif subject == example_subjects[1]:
            line_color = colors[1]
            line_width = 0.75
            order = 10
            alpha = 0.3
        else:
            line_color = 'grey'
            line_width = 0.5
            order = 5
            alpha = 0.3

        for tuple in data_pair_tuples:
            y_points_r2.append(utils.calculate_r2(tuple.ACTUAL, tuple.PERCEIVED))
            y_points_area.append(calculate_area.actual_vs_perceived(tuple.ACTUAL, tuple.PERCEIVED, experiment))

        y_point_lists = [y_points_r2, y_points_area]

        for subplot, y_points, y_label, y_tick, y_lim, text in zip(params.subplot_indices, y_point_lists,
                                                                   params.y_labels,
                                                                   params.y_ticks, y_lims, plot_text):
            plt.subplot(2, 1, subplot)
            plt.plot(x_points, y_points, color=line_color, alpha=alpha, linewidth=line_width, zorder=order)
            plt.ylabel(y_label, fontfamily=params.font, fontsize=8)
            plt.yticks(y_tick, fontfamily=params.font, fontsize=8)
            if experiment == 'exp1' and subplot == 2:
                plt.ylim(0.75, 1)
            else:
                plt.ylim(y_lim)
            plt.gca().spines['right'].set_visible(False)
            plt.gca().spines['top'].set_visible(False)
            plt.gca().spines['bottom'].set_visible(False)
            if subplot == 2:
                plt.xticks(x_points, labels=x_labels, fontfamily=params.font, fontsize=8)
                plt.text(text_x, text_y_plot_2, text, fontsize=11, fontfamily='arial')
            else:
                plt.text(text_x, text_y_plot_1, text, fontsize=11, fontfamily='arial')

    for mean_list, ci_list, subplot in zip(means_lists, ci_lists, params.subplot_indices):
        plt.subplot(2, 1, subplot)
        plt.grid(axis='y', linewidth=0.5, color='lightgrey')
        plt.gca().tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                              labelbottom=False, labeltop=False, labelleft=True, labelright=False)
        if subplot == 2:
            plt.gca().tick_params(axis='both', which='both', bottom=True, labelbottom=True)
            plt.gca().spines['bottom'].set_visible(True)
        for mean, ci, x_point in zip(mean_list, ci_list, x_points):
            plt.errorbar(x_point, mean, yerr=ci, ecolor='black', marker="o", markerfacecolor='black', mec='black',
                         markersize=3, linewidth=1, zorder=11)
        if subplot == 2 and experiment == 'exp1':
            ax = plt.gca()
            plt.text(0.28, 0.035, 'Day 1', fontsize=8, fontfamily=params.font, transform=plt.gcf().transFigure)
            plt.text(0.73, 0.035, 'Day 2', fontsize=8, fontfamily=params.font, transform=plt.gcf().transFigure)
            ax.annotate('', xy=(0, -0.12), xycoords='axes fraction', xytext=(0.45, -0.12),
                        arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
            ax.annotate('', xy=(0.6, -0.12), xycoords='axes fraction', xytext=(0.99, -0.12),
                        arrowprops=dict(arrowstyle='-', color='black', linewidth=0.5))
            ax.add_patch(mpatches.Rectangle(xy=(1, params.r2_ci_lower),  # point of origin.
                                            width=3,
                                            height=(params.r2_ci_upper - params.r2_ci_lower),
                                            linewidth=0,
                                            color='lightgray',
                                            fill=True,
                                            alpha=0.7))
        elif subplot == 1:
            plt.gca().xaxis.set_major_locator(MultipleLocator(1))
            plt.gca().xaxis.set_major_formatter('{x:.0f}')

        if experiment == 'exp1' and subplot == 1:
            plt.gca().add_patch(mpatches.Rectangle(xy=(1, params.area_ci_lower),  # point of origin.
                                                   width=3,
                                                   height=(params.area_ci_upper - params.area_ci_lower),
                                                   linewidth=0,
                                                   color='lightgray',
                                                   fill=True,
                                                   alpha=0.7))

    plt.tight_layout(h_pad=0.6, w_pad=0.9)
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'R2 and area per condition plots saved in {text}\n')
    plt.close()


def area_vs_r2_plot(all_subject_data, experiment):
    plot = f'figure_3_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    area_lists = calculate_area.group_areas(all_subject_data, experiment)
    r2_lists = utils.store_r2_tuples(all_subject_data, experiment)
    x_labels = utils.x_ticks_group_plot(experiment)

    if experiment == 'exp1':
        subplot_indices = [1, 2, 3, 4]
        text_labels = ['A', 'B', 'C', 'D']
    else:
        subplot_indices = [1, 2, 3]
        text_labels = ['A', 'B', 'C']

    plt.figure(figsize=(3.3, 7))
    for subplot_index, condition_r2_data, condition_area_data, condition_name, text in zip(subplot_indices, r2_lists,
                                                                                     area_lists, x_labels, text_labels):
        intercept, slope = utils.calculate_regression_general(condition_area_data, condition_r2_data)
        r, ci = utils.pearson_r_ci(condition_area_data, condition_r2_data)
        r_ci_text = str(f'{condition_name}: r = {r} {ci}    intercept = {intercept}     slope = {slope}')
        plt.subplot(subplot_indices[-1], subplot_indices[0], subplot_index)
        x_vals = np.array([0, max(condition_area_data)])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color='black', linewidth=1, zorder=11)
        plt.scatter(condition_area_data, condition_r2_data, c='gray', marker='o', alpha=0.6, s=5, linewidths=0,
                    zorder=10)

        plt.xlim(0, 20)
        plt.yticks([0.6, 0.7, 0.8, 0.9, 1], fontsize=8, fontfamily='arial')
        plt.xticks(fontsize=8, fontfamily='arial')
        plt.ylim(0.60, 1)
        plt.ylabel('R$^2$', fontsize=8, fontfamily='arial')
        plt.grid(linewidth=0.5, color='lightgrey')
        plt.gca().tick_params(axis='both', which='both', bottom=False, top=False, left=True, right=False,
                              labelbottom=False, labeltop=False, labelleft=True, labelright=False)
        plt.gca().spines['right'].set_visible(False)
        plt.gca().spines['top'].set_visible(False)
        plt.gca().spines['bottom'].set_visible(False)
        if subplot_index == 4 and experiment == 'exp1' or subplot_index == 3 and experiment == 'exp2':
            plt.xlabel('Area (cm$^2$)', size=8, fontfamily='arial')
            plt.gca().tick_params(axis='both', which='both', bottom=True, labelbottom=True)
            plt.gca().spines['bottom'].set_visible(True)
        plt.text(22, 1, text, fontsize = 12, fontfamily = 'arial')
        print(f'{condition_name}, {experiment} regression model:\n')
        utils.regression_summary(condition_area_data, condition_r2_data)
        with open('results.txt', 'w') as writer:
            writer.write(r_ci_text)
        plt.tight_layout()

    plt.tight_layout(h_pad=0.9)
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'{experiment} area vs r2 plots saved in {text}\n')
    plt.close()


def slope_comparison(all_subject_data, experiment):
    plot = f'figure_4_{experiment}'
    path = utils.create_article_plot_save_path(plot)

    slopes_line_width = []
    slopes_width_line = []

    for subject_data in all_subject_data:
        intercept_line_width, slope_line_width = utils.calculate_regression_general(subject_data.LINE_WIDTH.ACTUAL,
                                                                                    subject_data.LINE_WIDTH.PERCEIVED)
        intercept_width_line, slope_width_line = utils.calculate_regression_general(subject_data.WIDTH_LINE.ACTUAL,
                                                                                    subject_data.WIDTH_LINE.PERCEIVED)

        slopes_line_width.append(slope_line_width)
        slopes_width_line.append(slope_width_line)

    plt.figure(figsize=(3.3, (7 / 2.6)))
    plt.grid(linewidth=0.5, color='lightgrey')

    intercept, slope = utils.calculate_regression_general(slopes_line_width, slopes_width_line)

    print(f'Regression model summary {experiment}, {plot} \n')
    utils.regression_summary(slopes_line_width, slopes_width_line)

    x_vals = np.array([min(slopes_line_width) - 0.25, max(slopes_line_width) + 0.25])
    y_vals = intercept + slope * x_vals

    plt.plot(x_vals, y_vals, color='black', linewidth=1, zorder=10)
    plt.scatter(slopes_line_width, slopes_width_line, c='gray', marker='o', alpha=0.6, s=5, zorder=5, linewidths=0)

    plt.xlabel(f'Line-to-width slope', fontsize=8, fontfamily='arial')
    plt.ylabel(f'Width-to-line slope', fontsize=8, fontfamily='arial')
    plt.xticks([0.4, 0.8, 1.2, 1.6, 2], fontsize=8, fontfamily='arial')
    plt.yticks([0.4, 0.8, 1.2, 1.6, 2], fontsize=8, fontfamily='arial')
    plt.gca().spines['top'].set_visible(False)
    plt.gca().spines['right'].set_visible(False)
    plt.xlim(0.4, 1.6)
    plt.ylim(0.4, 2.0)
    plt.tight_layout()
    plt.savefig(path, dpi=300)
    text = colored(f'{path}', 'blue')
    print(f'slope comparison saved in {text}\n')
    plt.close()
