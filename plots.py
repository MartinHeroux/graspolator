import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import pandas as pd


def visual_check_and_store(file_name, subject):
    condition_results = [subject[0], subject[1], subject[2], subject[3]]
    condition_names = ['d1_dom', "d1_non_dom", "d2_dom1", "day2_dom2"]
    locations = range(1, 5)
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle(str(file_name + ' Scatterplot'))
    path = Path('./plots/scatter_checks/', file_name)
    for condition, name, loc in zip(condition_results, condition_names, locations):
        d = {'actual': condition[0], 'perceived': condition[1]}
        df = pd.DataFrame(d)
        ax = fig.add_subplot(2, 2, loc)
        ax.scatter(df.actual, df.perceived, marker='o', s=2)
        ax.title.set_text(name)
    plt.savefig(path)


def regplots(file_name, subject):
    condition_results = [subject[0], subject[1], subject[2], subject[3]]
    condition_names = ['d1_dom', "d1_non_dom", "d2_dom1", "day2_dom2"]
    locations = range(1, 5)
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle(str(file_name + ' Reg. Plot'))
    path = Path('./plots/reg_plots/', file_name)
    for condition, name, loc in zip(condition_results, condition_names, locations):
        d = {'actual': condition[0], 'perceived': condition[1]}
        df = pd.DataFrame(d)
        ax = fig.add_subplot(2, 2, loc)
        sns.regplot(x='actual', y='perceived', data=df)
        ax.title.set_text(name)
    plt.savefig(path)
