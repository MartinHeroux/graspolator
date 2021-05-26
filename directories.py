import os
from pathlib import Path


def create_plot_subdirectories():
    plot_subdirectories = ['group_plots',
                           'indiviudal_plots,'
                           'individual_plots/subject_regression_plots',
                           'individual_plots/consistency_plots',
                           'individual_plots/area_plots',
                           'individual_plots/area_plots/regression_vs_reality',
                           'individual_plots/area_plots/between_condition_comparison']
    for subdirectory in plot_subdirectories:
        path = Path(f'./plots/{subdirectory}')
        if not os.path.exists(path):
            os.makedirs(path)


def get_filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames


def create_directory(directory):
    if not os.path.exists(f'./{directory}'):
        os.makedirs(f'./{directory}')
        print(f'created directory {directory}')


def create_sub_directory(directory, sub_diretory):
    if not os.path.exists(f'./{directory}/{sub_diretory}'):
        os.makedirs(f'./{directory}/{sub_diretory}')
        print(f'created directory {directory}/{sub_diretory}')

