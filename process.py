from pathlib import Path
import os

import data
import figures

experiments = ['exp1', 'exp2']
data_folders = [Path('./data/exp1'), Path('./data/exp2')]
results_files = [Path('./results_exp1.txt'), Path('./results_exp2.txt')]

for experiment, data_folder, results_file in zip(experiments, data_folders, results_files):
    all_subject_data, subject_IDs = data.get_data_and_subjects(experiment, data_folder)

    if results_file.exists():
        os.remove(results_file)
        print('Previous results.txt removed')

    # text files of numerical results generated simultaneous with figures
    figures.generate(all_subject_data, subject_IDs, experiment)








#def axis_fix(axes, x_ticks, y_ticks, x_labels, y_labels, etc):