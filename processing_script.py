from collections import namedtuple

import process
import plot


plot_dispatch = namedtuple('plot_dispatch', 'PLOT COMMAND')


# TODO change string below to match experiment
#  either 'exp1' or 'exp2' (Kathy and Lovisa respectively)
experiment = 'exp1'


# import data and subject list for experiment
all_subject_data, subjects = process.return_data_and_subjects(experiment)


# make plot dispatcher keys
# TODO change 'run' to 'skip' to alter which plots are made
A = plot_dispatch._make([plot.individual_regressions, 'skip'])
B = plot_dispatch._make([plot.individual_areas_to_reality, 'skip'])
C = plot_dispatch._make([plot.individual_areas_between_conditions, 'skip'])
D = plot_dispatch._make([plot.group_regression_lines_per_condition, 'run'])
E = plot_dispatch._make([plot.group_areas_per_conditions, 'run'])
F = plot_dispatch._make([plot.group_areas_vs_r2_per_condition, 'run'])
G = plot_dispatch._make([plot.group_r2_per_condition, 'run'])
# Exp1 specific plots
H = plot_dispatch._make([plot.group_areas_between_conditions, 'run'])
I = plot_dispatch._make([plot.group_areas_difference_of_differences, 'run'])
# Exp2 specific plots
J = plot_dispatch._make([plot.lovia_reciprocal_condition_regression, 'run'])


# plot according to dispatch keys and experiment
plot_summary = process.create_plot_dispatcher(experiment, A, B, C, D, E, F, G, H, I, J)
process.plot_by_dispatcher_key(plot_summary, all_subject_data, experiment, subjects)
