import matplotlib.pyplot as plt
from pathlib import Path
import seaborn as sns
import pandas as pd
from random import random
import numpy as np
import yaml
import utils



def visual_check_and_store(subject_ID, subject_data):
    condition_results = [subject_data[0], subject_data[1], subject_data[2], subject_data[3]]
    condition_names = ['day1_dominant', "day1_non_dominant", "day2_domimant_1", "day2_dominant_2"]
    plt.figure(figsize=(10, 10))
    plt.suptitle(str(subject_ID + ' Scatterplot'))
    for subplot_index, (condition, name) in enumerate(zip(condition_results, condition_names), start=1):
        plt.subplot(2, 2, subplot_index)
        plt.plot([0, 14], [0, 14], 'k--')
        length_data = len(condition.perceived_widths)
        random_values = [random()/4 for _ in range(length_data)]
        x_data = np.array((condition.actual_widths)) + np.array(random_values)
        plt.plot(x_data, condition.perceived_widths, 'o', alpha=0.5, color='royalblue')

        intercept, slope = utils.calculate_regression(condition)
        x2 = 2
        x10 = 10
        y2 = slope*x2 + intercept
        y10 = slope*x10 + intercept
        plt.plot([x2, x10], [y2, y10], color='royalblue')
        plt.text(2, 12, f'{slope:4.2f}*x + {intercept:4.2f}', fontsize=12)

        plt.xticks(range(2, 11))
        plt.xlim([1, 11])
        plt.yticks([0.5] + list(range(1, 14)))
        # TODO: Once id and fixed all bad trials, set y_lim to 14
        plt.ylim([0, None])
        plt.grid()
        plt.title(name, loc = 'right')
        plt.ylabel('Perceived width (cm)')
        plt.xlabel('Actual width (cm)')

    path = Path('./plots/scatter_checks/', subject_ID)
    plt.savefig(path)
    print(f'Saving the scatter_checks for {subject_ID}')
    plt.close()


def regplots(subject_ID, subject):
    condition_results = [subject[0], subject[1], subject[2], subject[3]]
    condition_names = ['d1_dom', "d1_non_dom", "d2_dom1", "day2_dom2"]
    locations = range(1, 5)
    fig = plt.figure(figsize=(10, 10))
    fig.suptitle(str(subject_ID + ' Reg. Plot'))
    path = Path('./plots/reg_plots/', subject_ID)
    for condition, name, loc in zip(condition_results, condition_names, locations):
        d = {'actual': condition[0], 'perceived': condition[1]}
        df = pd.DataFrame(d)
        ax = fig.add_subplot(2, 2, loc)
        sns.regplot(x='actual', y='perceived', data=df)
        ax.title.set_text(name)
    plt.savefig(path)
    print(f'Saving the reg_plots for {subject_ID}')
    plt.close()
