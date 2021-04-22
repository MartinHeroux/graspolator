import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
from pathlib import Path
import numpy as np
import os
from collections import namedtuple

import utils
import area_calcs


def consistency_plot(subject_ID, subject_data):
    if not os.path.exists('./plots/consistency_plots'):
        os.makedirs('./plots/consistency_plots')
        print('consistency plot directory created')
    else:
        print('consistency plot directory already exists, continuing')

    path = Path('./plots/consistency_plots/')

    Pair = namedtuple('Pair', 'data_1 data_2 label_1 label_2 title colour_1 colour_2 patch_1 patch_2')
    Pairs = namedtuple('Pairs', 'between_hands, between_days, within_day')

    d1_dom = mpatches.Patch(color='blue', label='Day 1 Dominant')
    d1_non_dom = mpatches.Patch(color='orange', label='Day 1 Non Dominant')
    d2_dom_a = mpatches.Patch(color='red', label='Day 2 Dominant A')
    d2_dom_b = mpatches.Patch(color='green', label='Day 2 Dominant B')

    between_hands = Pair(data_1=subject_data[0], data_2=subject_data[1], label_1='d1_dom', label_2='d1_non_dom',
                         title='Between Hands', colour_1='blue', colour_2='orange', patch_1=d1_dom,
                         patch_2=d1_non_dom)
    between_days = Pair(data_1=subject_data[0], data_2=subject_data[2], label_1='d1_dom', label_2='d2_dom_a',
                        title='Between Days', colour_1='blue', colour_2='red',
                        patch_1=d1_dom, patch_2=d2_dom_a)
    within_day = Pair(data_1=subject_data[2], data_2=subject_data[3], label_1='d2_dom_a', label_2='d2_dom_b',
                      title='Within Day', colour_1='red', colour_2='green', patch_1=d2_dom_a, patch_2=d2_dom_b)

    subplot_indices = [1, 2, 3]
    data_pairs = Pairs(between_hands=between_hands, between_days=between_days, within_day=within_day)

    plt.figure(figsize=(15, 7))
    plt.suptitle(str(subject_ID + ' Consistency Plots'))

    for subplot_index, pair in zip(subplot_indices, data_pairs):
        print(pair.title)
        plt.subplot(1, 3, subplot_index)

        intercept_a, slope_a = utils.calculate_regression(pair.data_1)
        intercept_b, slope_b = utils.calculate_regression(pair.data_2)

        x2_a, x10_a, y_at_x2_a, y_at_x10_a = utils.reg_line_endpoints(intercept_a, slope_a)
        x2_b, x10_b, y_at_x2_b, y_at_x10_b = utils.reg_line_endpoints(intercept_b, slope_b)
        x_intersect, y_intersect = utils.point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)

        group = utils.subject_group_reg_lines(x_intersect)
        if group == 'cross':
            total_area = area_calcs.reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b,
                                                          y_at_x10_b)
        else:
            total_area = area_calcs.reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b)

        plt.plot([x2_a, x10_a], [y_at_x2_a, y_at_x10_a], color=pair.colour_1, label=pair.label_1)
        plt.plot([x2_b, x10_b], [y_at_x2_b, y_at_x10_b], color=pair.colour_2, label=pair.label_2)

        x_colour_points = np.array([2, 10])
        y_points_a = np.array([y_at_x2_a, y_at_x10_a])
        y_points_b = np.array([y_at_x2_b, y_at_x10_b])

        plt.fill_between(x_colour_points, y_points_a, y_points_b,
                         color='gray', alpha=0.3, interpolate=True)

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks([0.5] + list(range(1, 15)))
        plt.ylim([0, 15])
        plt.grid()
        plt.text(2, 12, f'Area Difference = {total_area:4.2f}', fontsize=12)
        plt.title(pair.title, loc='right')
        plt.legend(handles=[pair.patch_1, pair.patch_2], loc='upper left')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    plt.savefig('{}/{}'.format(path, subject_ID))
    print(f'Saving consistency plots for {subject_ID}')
    plt.close()
