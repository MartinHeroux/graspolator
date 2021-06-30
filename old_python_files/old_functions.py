from collections import namedtuple
from pathlib import Path

import matplotlib as mpl

import utils
from calculate_area import actual_vs_perceived

from utils import get_filename_list

mpl.get_configdir()
import matplotlib.pyplot as plt

plt.style.use('graspolator_style')

# Create figure
fig = plt.figure()
# Add subplot to figure
ax = fig.add_subplot(111)
plt.plot([2,4], [2,4])
# Show empty plot
plt.show()

def between_condition_pair(data_pair):
    x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b = utils.compute_area_calc_inputs(
        data_pair)
    group = utils.subject_group_reg_lines(x_intersect)

    if group == 'cross':
        total_area = reg_line_crosser_area(x_intersect, y_intersect, y_at_x2_a, y_at_x10_a,
                                           y_at_x2_b,
                                           y_at_x10_b)
    else:
        total_area = reg_line_no_cross_area(y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b)
    return total_area

def compute_area_calc_inputs(data_pair):
    intercept_a, slope_a = utils.calculate_regression(data_pair.data_1)
    intercept_b, slope_b = utils.calculate_regression(data_pair.data_2)

    x2_a, x10_a, y_at_x2_a, y_at_x10_a = reg_line_endpoints(intercept_a, slope_a)
    x2_b, x10_b, y_at_x2_b, y_at_x10_b = reg_line_endpoints(intercept_b, slope_b)
    x_intersect, y_intersect = point_of_intersection_reg_lines(intercept_a, slope_a, intercept_b, slope_b)

    return x_intersect, y_intersect, y_at_x2_a, y_at_x10_a, y_at_x2_b, y_at_x10_b


def create_directory(directory):
    if not os.path.exists(f'./{directory}'):
        os.makedirs(f'./{directory}')
        print(f'created directory {directory}')


def create_sub_directory(directory, sub_diretory):
    if not os.path.exists(f'./{directory}/{sub_diretory}'):
        os.makedirs(f'./{directory}/{sub_diretory}')
        print(f'created directory {directory}/{sub_diretory}')



def create_plot_subdirectories():
    plot_subdirectories = ['group_plots',
                           'individual_plots',
                           'individual_plots/subject_regression_plots',
                           'individual_plots/area_plots',
                           'individual_plots/area_plots/regression_vs_reality',
                           'individual_plots/area_plots/between_condition_comparison']
    plot_path = Path('./plots')
    for subdirectory in plot_subdirectories:
        path = plot_path / subdirectory
        if not os.path.exists(path):
            os.makedirs(path)


def merge_pdfs(source_directory):
    filenames = get_filename_list(source_directory)
    merger = PdfFileMerger()
    for filename in filenames:
        pdf_path = str(Path('./randomised_plots_no_ID/', filename))
        merger.append(pdf_path)
    merger.write("concatenated.pdf")
    merger.close()


def store_r2_and_area_tuples_exp1(all_subject_data, subject_IDs):
    experiment = 'exp1'
    r2s_areas = namedtuple('r2s_area',
                           'subject_ID d1_dom_r2 d1_non_dom_r2 d2_dom_1_r2 d2_dom_2_r2 d1_dom_area d1_non_dom_area '
                           'd2_dom_1_area d2_dom_2_area')
    r2_area_tuples = []

    for subject_data, subject_ID in zip(all_subject_data, subject_IDs):
        d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple = utils.store_index_condition_data_tuple(
            subject_data)

        r2s_areas_tuple = r2s_areas(subject_ID=subject_ID,
                                    d1_dom_r2=utils.calculate_r2(d1_dom_tuple.ACTUAL, d1_dom_tuple.PERCEIVED),
                                    d1_non_dom_r2=utils.calculate_r2(d1_non_dom_tuple.ACTUAL,
                                                                     d1_non_dom_tuple.PERCEIVED),
                                    d2_dom_1_r2=utils.calculate_r2(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED),
                                    d2_dom_2_r2=utils.calculate_r2(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED),
                                    d1_dom_area=actual_vs_perceived(d1_non_dom_tuple.ACTUAL, d1_non_dom_tuple.PERCEIVED,
                                                                    experiment),
                                    d1_non_dom_area=actual_vs_perceived(d1_non_dom_tuple.ACTUAL,
                                                                        d1_non_dom_tuple.PERCEIVED, experiment),
                                    d2_dom_1_area=actual_vs_perceived(d2_dom_1_tuple.ACTUAL, d2_dom_1_tuple.PERCEIVED,
                                                                      experiment),
                                    d2_dom_2_area=actual_vs_perceived(d2_dom_2_tuple.ACTUAL, d2_dom_2_tuple.PERCEIVED,
                                                                      experiment))

        r2_area_tuples.append(r2s_areas_tuple)

    return r2_area_tuples


def store_r2_and_area_tuples_exp2(all_subject_data, subject_IDs):
    experiment = 'exp2'
    r2s_areas = namedtuple('r2s_area',
                           'subject_ID line_width_r2 width_line_r2 width_width_r2 line_width_area width_line_area '
                           'width_width_area')
    r2_area_tuples = []

    for subject_data, subject_ID in zip(all_subject_data, subject_IDs):
        data_tuples = utils.condition_plot_inputs(subject_data)

        line_width, width_line, width_width = data_tuples[0], data_tuples[1], data_tuples[2]

        r2s_areas_tuple = r2s_areas(subject_ID=subject_ID,
                                    line_width_r2=utils.calculate_r2(line_width.ACTUAL, line_width.PERCEIVED),
                                    width_line_r2=utils.calculate_r2(width_line.ACTUAL, width_line.PERCEIVED),
                                    width_width_r2=utils.calculate_r2(width_width.ACTUAL, width_width.PERCEIVED),
                                    line_width_area=actual_vs_perceived(line_width.ACTUAL, line_width.PERCEIVED,
                                                                        experiment),
                                    width_line_area=actual_vs_perceived(width_line.ACTUAL, width_line.PERCEIVED,
                                                                        experiment),
                                    width_width_area=actual_vs_perceived(width_width.ACTUAL, width_width.PERCEIVED,
                                                                         experiment))

        r2_area_tuples.append(r2s_areas_tuple)

    return r2_area_tuples