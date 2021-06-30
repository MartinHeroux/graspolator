from pathlib import Path

import data
import figures

experiments = ['exp1', 'exp2']
data_folders = [Path('./data/exp1'), Path('./data/exp2')]

for experiment, data_folder in zip(experiments, data_folders):
    all_subject_data, subject_IDs = data.get_data_and_subjects(experiment, data_folder)
    # text files of numerical results generated simultaneous with figures
    figures.generate(all_subject_data, subject_IDs, experiment)








#def axis_fix(axes, x_ticks, y_ticks, x_labels, y_labels, etc):