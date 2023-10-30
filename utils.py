import yaml
import os
from pathlib import Path
from dataclasses import dataclass


def read_yaml_corrections_file(fix_yaml):
    if not fix_yaml.is_file():
        return
    with open(fix_yaml) as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def get_subject_ids(directory):
    directories = list()
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directories.append(directory)
    return directories


def create_results_save_path():
    results_path = Path(f"./results/")
    if not os.path.exists(results_path):
        os.makedirs(results_path)
    return results_path
