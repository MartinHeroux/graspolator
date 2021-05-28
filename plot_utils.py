from collections import namedtuple
import matplotlib.patches as mpatches


def create_plot_constants():
    plot_constants = namedtuple('plot_constants', 'PLOT_SUBDIRECTORIES ACTUAL_WIDTH_RANGE PERCEIVED_WIDTH_RANGE ALPHA '
                                                  'SMALLEST_WIDTH LARGEST_WIDTH Y_MIN Y_MAX REALITY_LINE_MIN '
                                                  'REALITY_LINE_MAX '
                                                  'MINIMISER_PATCH MAXIMISER_PATCH CROSSER_PATCH')
    return plot_constants(PLOT_SUBDIRECTORIES=['group_plots',
                                               'regression_plots',
                                               'consistency_plots',
                                               'area_plots'],
                          ACTUAL_WIDTH_RANGE=[1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11],
                          PERCEIVED_WIDTH_RANGE=[0.5] + list(range(1, 15)),
                          ALPHA=0.5,
                          SMALLEST_WIDTH=2, LARGEST_WIDTH=10, Y_MIN=0, Y_MAX=14, REALITY_LINE_MIN=0,
                          REALITY_LINE_MAX=14,
                          MINIMISER_PATCH=mpatches.Patch(color='firebrick', label='Minimiser'),
                          MAXIMISER_PATCH=mpatches.Patch(color='green', label='Maximiser'),
                          CROSSER_PATCH=mpatches.Patch(color='royalblue', label='Crosser'))


def store_index_condition_data_tuple(subject_data):
    index_name_data = namedtuple('index_name_data', 'PLOT_INDEX DATA_INDEX NAME ACTUAL PERCEIVED')
    d1_dom_tuple = index_name_data(PLOT_INDEX=1, DATA_INDEX=0, NAME='d1_dominant',
                                   ACTUAL=subject_data.day1_dominant.actual_widths,
                                   PERCEIVED=subject_data.day1_dominant.perceived_widths)
    d1_non_dom_tuple = index_name_data(PLOT_INDEX=2, DATA_INDEX=1, NAME='d2_non_dominant',
                                       ACTUAL=subject_data.day1_non_dominant.actual_widths,
                                       PERCEIVED=subject_data.day1_non_dominant.perceived_widths)
    d2_dom_1_tuple = index_name_data(PLOT_INDEX=3, DATA_INDEX=2, NAME='d2_dominant_1',
                                     ACTUAL=subject_data.day2_dominant_1.actual_widths,
                                     PERCEIVED=subject_data.day2_dominant_1.perceived_widths)
    d2_dom_2_tuple = index_name_data(PLOT_INDEX=4, DATA_INDEX=3, NAME='d2_dominant_2',
                                     ACTUAL=subject_data.day2_dominant_2.actual_widths,
                                     PERCEIVED=subject_data.day2_dominant_2.perceived_widths)
    return d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple


def condition_pair_tuple(subject_data):
    d1_dom = mpatches.Patch(color='blue', label='Day 1 Dominant')
    d1_non_dom = mpatches.Patch(color='orange', label='Day 1 Non Dominant')
    d2_dom_a = mpatches.Patch(color='red', label='Day 2 Dominant A')
    d2_dom_b = mpatches.Patch(color='green', label='Day 2 Dominant B')

    Pair = namedtuple('Pair', 'data_1 data_2 label_1 label_2 title colour_1 colour_2 patch_1 patch_2 subplot_index')
    dom_vs_non_dom = Pair(data_1=subject_data.day1_dominant, data_2=subject_data.day1_non_dominant, label_1='d1_dom',
                          label_2='d1_non_dom',
                          title='Between Hands', colour_1='blue', colour_2='orange', patch_1=d1_dom,
                          patch_2=d1_non_dom, subplot_index=1)
    dom_d1_vs_d2 = Pair(data_1=subject_data.day1_dominant, data_2=subject_data.day2_dominant_1, label_1='d1_dom',
                        label_2='d2_dom_a',
                        title='Between Days', colour_1='blue', colour_2='red',
                        patch_1=d1_dom, patch_2=d2_dom_a, subplot_index=2)
    dom_d2_vs_d2 = Pair(data_1=subject_data.day2_dominant_1, data_2=subject_data.day2_dominant_2, label_1='d2_dom_a',
                        label_2='d2_dom_b',
                        title='Within Day', colour_1='red', colour_2='green', patch_1=d2_dom_a, patch_2=d2_dom_b,
                        subplot_index=3)
    return dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2


def subject_line_colour(intersection_x_value, y_when_x_equals_2):
    if 2 <= intersection_x_value <= 10:
        line_colour = 'royalblue'
    elif y_when_x_equals_2 < 2:
        line_colour = 'firebrick'
    else:
        line_colour = 'green'
    return line_colour
