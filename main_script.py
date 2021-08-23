from pathlib import Path
import os

import data
import figures

experiments = ['exp1']
data_folders = [Path('./data/exp1')]
results_files = [Path('./results_exp1.txt')]

for experiment, data_folder, results_file in zip(experiments, data_folders, results_files):
    if results_file.exists():
        os.remove(results_file)
        print(f'Previous results_{experiment}.txt removed\n')

    data.write_participant_demographics(experiment, data_folder)

    all_subject_data, subject_IDs = data.get_data_and_subjects(experiment, data_folder)

    # text files of numerical results generated simultaneous with figures
    figures.generate(all_subject_data, subject_IDs, experiment)


