import os
from pathlib import Path
import statsmodels.api as sm
import yaml
import scipy.stats as scp
import numpy as np
from matplotlib import patches as mpatches
from scipy.stats import sem, t
from collections import namedtuple
import math
from matplotlib.ticker import MultipleLocator
from random import random
from dataclasses import dataclass


#######################################
# PARSING DATA
#######################################


def read_yaml_corrections_file(fix_yaml):
    if not fix_yaml.is_file():
        return
    with open(fix_yaml) as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def remove_missing_data(actual_list, perceived_list, subject_ID, name):
    indices_to_remove = []
    for trial in perceived_list:
        if trial == "":
            indices_to_remove.append(perceived_list.index(trial))
    indices_to_remove.reverse()
    if len(indices_to_remove) > 0:
        #results = open("results_exp2.txt", "a")
        print(
            f"{str(len(indices_to_remove)):5s} saturated data point(s) removed for {subject_ID}\n"
        )
        #results.close()
    for index in indices_to_remove:
        actual_list.pop(index)
        perceived_list.pop(index)
    return actual_list, perceived_list


#########################################
# EQUATIONS
#########################################


def calculate_regression_general(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope


def calculate_reg_intercept(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept


def calculate_reg_slope(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return slope


def regression_summary(x, y):
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()

    t_vals = model.tvalues
    t_test = model.t_test([1, 0])
    f_test = model.f_test(np.identity(2))

    return t_vals, t_test, f_test


# def calculate_r2(actual, perceived):
# r_score, p_value = scp.pearsonr(actual, perceived)
# r_squared = r_score ** 2
# return r_squared


def calculate_r2(actual, perceived):
    actual = sm.add_constant(actual)
    model = sm.OLS(perceived, actual).fit()

    r_squared = model.rsquared
    return r_squared


def pearson_r_ci(x, y):
    if len(x) != len(y):
        print("Lists of uneven length in pearson calc")

    r_value, p_value = scp.pearsonr(x, y)

    alpha = 0.05 / 2  # Two-tail test

    z_critical = scp.norm.ppf(1 - alpha)  # z score for 95% CI
    z_sample = 0.5 * np.log((1 + r_value) / (1 - r_value))  # z score of r value

    n = len(x)
    std_err = 1 / np.sqrt(n - 3)

    z_ci_lower = z_sample - z_critical * std_err
    z_ci_upper = z_sample + z_critical * std_err

    r_ci_lower = (math.exp(2 * z_ci_lower) - 1) / (
        math.exp(2 * z_ci_lower) + 1
    )  # convert back to r
    r_ci_upper = (math.exp(2 * z_ci_upper) - 1) / (
        math.exp(2 * z_ci_upper) + 1
    )  # convert back to r

    r = f"{r_value:4.2f}"
    ci = str(f"[{r_ci_lower:4.2f} - {r_ci_upper:4.2f}]")

    return r, ci


def calculate_mean_ci(data_list):
    mean = np.mean(data_list)
    confidence = 0.95
    n = len(data_list)
    std_err = sem(data_list)
    ci = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return mean, ci


def calculate_ci(data_list):
    confidence = 0.95
    n = len(data_list)
    std_err = sem(data_list)
    ci = std_err * t.ppf((1 + confidence) / 2, n - 1)
    return ci


##########################################################
# OBJECT STORAGE
##########################################################


def create_data_tuples(experiment, subject_data):
    if experiment == "exp1":
        plot_inputs = store_condition_data_tuples_kathy(subject_data)
    else:
        plot_inputs = store_condition_data_tuples_lovisa(subject_data)
    return plot_inputs


def store_condition_data_tuples_lovisa(subject_data):
    plot_inputs = namedtuple("INPUTS", "NAME ACTUAL PERCEIVED PLOT_INDEX")
    line_width_inputs = plot_inputs(
        NAME="Show Line Pick Width",
        ACTUAL=subject_data.LINE_WIDTH.ACTUAL,
        PERCEIVED=subject_data.LINE_WIDTH.PERCEIVED,
        PLOT_INDEX=1,
    )
    width_line_inputs = plot_inputs(
        NAME="Present Width Pick Line",
        ACTUAL=subject_data.WIDTH_LINE.ACTUAL,
        PERCEIVED=subject_data.WIDTH_LINE.PERCEIVED,
        PLOT_INDEX=2,
    )
    width_width_inputs = plot_inputs(
        NAME="Present Width Pick Width",
        ACTUAL=subject_data.WIDTH_WIDTH.ACTUAL,
        PERCEIVED=subject_data.WIDTH_WIDTH.PERCEIVED,
        PLOT_INDEX=3,
    )
    tuples = line_width_inputs, width_line_inputs, width_width_inputs
    return tuples


def store_example_subject_data_kathy(
    all_subject_data, subjects, subject_1_ID, subject_2_ID
):
    experiment = "exp1"
    for subject_data, subject_name in zip(all_subject_data, subjects):
        if subject_name == subject_1_ID:
            condition_data_list_1 = extract_condition_data_with_dummy_data_kathy(subject_data, experiment)
        if subject_name == subject_2_ID:
            condition_data_list_2 = extract_condition_data_with_dummy_data_kathy(subject_data, experiment)

    return [condition_data_list_1, condition_data_list_2]


def store_example_subject_data_lovisa(
    all_subject_data, subjects, subject_1_ID, subject_2_ID
):
    experiment = "exp2"
    for subject_data, subject_name in zip(all_subject_data, subjects):
        if subject_name == subject_1_ID:
            condition_data_list_1 = extract_condition_data_with_dummy_data_kathy(subject_data, experiment)
        if subject_name == subject_2_ID:
            condition_data_list_2 = extract_condition_data_with_dummy_data_kathy(subject_data, experiment)

    return [condition_data_list_1, condition_data_list_2]


def extract_condition_data_with_dummy_data_kathy(subject_data, experiment):
    dummy_data = namedtuple("condition", "ACTUAL PERCEIVED")
    if experiment == "exp1":
        D1_DOM = subject_data.day1_dominant
        D1_NON_DOM = subject_data.day1_non_dominant
        D2_DOM_1 = subject_data.day2_dominant_1
        D2_DOM_2 = subject_data.day2_dominant_2

        condition_data_list = [D1_DOM, D1_NON_DOM, D2_DOM_1, D2_DOM_2]

    else:
        LINE_WIDTH = subject_data.LINE_WIDTH
        WIDTH_LINE = subject_data.WIDTH_LINE
        WIDTH_WIDTH = subject_data.WIDTH_WIDTH
        DUMMY_DATA = dummy_data(ACTUAL=[3, 6, 9], PERCEIVED=[3, 6, 9])

        condition_data_list = [LINE_WIDTH, WIDTH_LINE, WIDTH_WIDTH, DUMMY_DATA]

    return condition_data_list


def store_condition_data_tuples_kathy(subject_data):
    index_name_data = namedtuple(
        "index_name_data", "PLOT_INDEX DATA_INDEX NAME ACTUAL PERCEIVED"
    )
    d1_dom_tuple = index_name_data(
        PLOT_INDEX=1,
        DATA_INDEX=0,
        NAME="d1_dominant",
        ACTUAL=subject_data.day1_dominant.ACTUAL,
        PERCEIVED=subject_data.day1_dominant.PERCEIVED,
    )
    d1_non_dom_tuple = index_name_data(
        PLOT_INDEX=2,
        DATA_INDEX=1,
        NAME="d2_non_dominant",
        ACTUAL=subject_data.day1_non_dominant.ACTUAL,
        PERCEIVED=subject_data.day1_non_dominant.PERCEIVED,
    )
    d2_dom_1_tuple = index_name_data(
        PLOT_INDEX=3,
        DATA_INDEX=2,
        NAME="d2_dominant_1",
        ACTUAL=subject_data.day2_dominant_1.ACTUAL,
        PERCEIVED=subject_data.day2_dominant_1.PERCEIVED,
    )
    d2_dom_2_tuple = index_name_data(
        PLOT_INDEX=4,
        DATA_INDEX=3,
        NAME="d2_dominant_2",
        ACTUAL=subject_data.day2_dominant_2.ACTUAL,
        PERCEIVED=subject_data.day2_dominant_2.PERCEIVED,
    )
    tuples = d1_dom_tuple, d1_non_dom_tuple, d2_dom_1_tuple, d2_dom_2_tuple
    return tuples


#########################################################
# CONSTANTS
#########################################################

@dataclass
class ExpCodes:
    EXP_1 = 'exp2'
    EXP_2 = 'exp1'


def create_general_constants():
    general_constants = namedtuple(
        "constants",
        "CONDITION_NAMES_EXP1 CONDITION_NAMES_EXP2 CONDITION_PAIRS SUBJECT_IDS",
    )
    return general_constants(
        CONDITION_NAMES_EXP1=[
            "D1 dominant",
            "D1 non-dominant",
            "D2 dominant 1",
            "D2 dominant 2",
        ],
        CONDITION_NAMES_EXP2=["Line to width", "Width to line", "Width to width"],
        CONDITION_PAIRS=["between_hands", "between_days", "within_day"],
        SUBJECT_IDS=[
            "SUB01L",
            "SUB01R",
            "SUB02L",
            "SUB02R",
            "SUB03L",
            "SUB03R",
            "SUB04R",
            "SUB05R",
            "SUB06R",
            "SUB07R",
            "SUB08R",
            "SUB09R",
            "SUB10R",
            "SUB11R",
            "SUB12R",
            "SUB13R",
            "SUB14R",
            "SUB16R",
            "SUB17R",
            "SUB18R",
            "SUB19R",
            "SUB20R",
            "SUB21R",
            "SUB22R",
            "SUB23R",
            "SUB24R",
            "SUB25R",
            "SUB26R",
            "SUB27R",
            "SUB28R",
        ],
    )


def x_points_group_plot(experiment):
    if experiment == "exp1":
        x_points = [1, 2, 3, 4]
        x_lims = (0.95, 4.05)
    else:
        x_points = [1, 2, 3]
        x_lims = (0.95, 3.05)
    return x_points, x_lims


def x_tick_labels_group_plot(experiment):
    if experiment == "exp1":
        x_ticks = ["Dominant", "Non-dominant", "Dominant", "Dominant"]
    else:
        x_ticks = ["Grasp-to-grasp", "Grasp-to-vision", "Vision-to-grasp"]
    return x_ticks


def r2_area_constants():
    constants = namedtuple(
        "constants",
        "y_labels y_ticks y_lims subplot_indices r2_mean r2_ci_lower r2_ci_upper "
        "area_mean area_ci_lower area_ci_upper exp_1_colors exp_2_colors "
        "exp_1_subjects exp_2_subjects font",
    )

    r2_area_constants = constants(
        y_labels=["R$^2$", "Normalised error (cm$^2$ / cm)"],
        y_ticks=[[0.6, 0.7, 0.8, 0.9, 1], [0, 1, 2, 3, 4]],
        y_lims=[[0.6, 1.01], [0, 4]],
        subplot_indices=[2, 1],
        r2_mean=0.946,
        r2_ci_lower=0.9306,
        r2_ci_upper=0.9613,
        area_mean=0.22,
        area_ci_lower=0.16,
        area_ci_upper=0.28,
        exp_1_colors=["darkorchid", "fuchsia"],
        exp_2_colors=["green", "lime"],
        exp_1_subjects=["SUB18R", "SUB02R"],
        exp_2_subjects=["sub02", "sub29"],
        font="FreeSans",
    )

    return r2_area_constants


@dataclass
class ExampleParticipantIDs:
    exp1_participant_1: str = "SUB18R"
    exp1_participant_2: str = "SUB02R"
    exp2_participant_1: str = "sub17"
    exp2_participant_2: str = "sub29"


@dataclass
class ExpNameStrings:
    exp1 = 'exp1'
    exp2 = 'exp2'


####################################################################
# PATHS AND DIRECTORIES
####################################################################


def create_figure_save_path(plot):
    path = Path(f"./plots/figures/")
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f"./plots/figures/{plot}.png")
    return savepath


def create_results_save_path():
    results_path = Path(f"./results/")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    return results_path


def create_data_save_path():
    results_path = Path(f"./data/")
    if not os.path.exists(results_path):
        os.makedirs(results_path)

    return results_path


def create_individual_plot_save_path(plot, subject_id):
    path = Path(f'./plots/individual_plots/{plot}')
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f'./plots/individual_plots/{plot}/{plot}_{subject_id}.png')
    return savepath


def get_directory_list(directory):
    directories = []
    for root, dirs, files in os.walk(directory):
        for directory in dirs:
            directories.append(directory)
    return directories


##################################################################
# PLOT APPEARANCE
##################################################################


def set_ax_parameters(ax, x_ticks, y_ticks, x_tick_labels, y_tick_labels, x_lims, y_lims, x_label, y_label,
                      x_fontsize=10, gridlines=None, font="arial", y_fontsize=10):
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels, fontsize=x_fontsize, fontfamily=font)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels, fontsize=y_fontsize, fontfamily=font)
    ax.set_xlim(x_lims)
    ax.set_ylim(y_lims)
    ax.set_xlabel(x_label, fontsize=10, fontfamily=font)
    ax.set_ylabel(y_label, fontsize=10, fontfamily=font)
    if gridlines:
        ax.grid(axis="both", linewidth=0.5, color="lightgray")


def draw_ax_spines(ax, left, right, top, bottom, x_offset=False, y_offset=False):
    commands = [left, right, top, bottom]
    spines = ["left", "right", "top", "bottom"]

    for spine, command in zip(spines, commands):
        if command == True:
            ax.spines[spine].set_visible(True)
        else:
            ax.spines[spine].set_visible(False)

    if y_offset == True:
        ax.spines["left"].set_position(("outward", 3))
    if x_offset == True:
        ax.spines["bottom"].set_position(("outward", 5))


def add_plot_text(ax, subplot, experiment, font="arial"):
    if subplot == 2 and experiment == "exp1":
        ax.text(
            0.1, -0.25, "Day 1", fontsize=8, fontfamily=font, transform=ax.transAxes
        )
        ax.text(
            0.75, -0.25, "Day 2", fontsize=8, fontfamily=font, transform=ax.transAxes
        )
        ax.annotate(
            "",
            xy=(0, -0.17),
            xycoords="axes fraction",
            xytext=(0.45, -0.17),
            arrowprops=dict(arrowstyle="-", color="black", linewidth=0.5),
        )
        ax.annotate(
            "",
            xy=(0.6, -0.17),
            xycoords="axes fraction",
            xytext=(0.99, -0.17),
            arrowprops=dict(arrowstyle="-", color="black", linewidth=0.5),
        )

    elif subplot == 1:
        ax.xaxis.set_major_locator(MultipleLocator(1))
        ax.xaxis.set_major_formatter("{x:.0f}")


def add_plot_shading(
    ax, subplot, experiment, r2_ci_lower, r2_ci_upper, area_ci_lower, area_ci_upper
):
    if subplot == 2 and experiment == "exp1":
        ax.add_patch(
            mpatches.Rectangle(
                xy=(1, r2_ci_lower),  # point of origin.
                width=3,
                height=(r2_ci_upper - r2_ci_lower),
                linewidth=0,
                color="gray",
                fill=True,
                alpha=0.5,
            )
        )

    if experiment == "exp1" and subplot == 1:
        ax.add_patch(
            mpatches.Rectangle(
                xy=(1, area_ci_lower),  # point of origin.
                width=3,
                height=(area_ci_upper - area_ci_lower),
                linewidth=0,
                color="gray",
                fill=True,
                alpha=0.5,
            )
        )


def plot_data_scatter(ax, actual, perceived, color):
    length_data = len(perceived)
    jitter_values = [random() / 4 for _ in range(length_data)]
    x_data = (np.array(actual) - 0.1) + np.array(jitter_values)

    # plot scatter plot of stimulus vs perceived widths
    ax.plot(
        x_data,
        perceived,
        "o",
        color=color,
        alpha=0.5,
        markersize=3,
        markeredgecolor=None,
        markeredgewidth=0,
    )


def plot_regression_line(
    ax, intercept, slope, color, x_1, x_2, alpha=1, width=1, order=10
):
    x1 = x_1
    x2 = x_2
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept

    ax.plot([x1, x2], [y1, y2], color=color, linewidth=width, alpha=alpha, zorder=order)


def shade_area(ax, intercept, slope, x_1, x_2):
    x1 = x_1
    x2 = x_2
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    x_colour_points, y_points_reality, y_points_reg = (
        np.array([x1, x2]),
        np.array([x1, x2]),
        np.array([y1, y2]),
    )

    ax.fill_between(
        x_colour_points,
        y_points_reality,
        y_points_reg,
        where=(y_points_reality > y_points_reg),
        color="lightgrey",
        alpha=0.5,
        interpolate=True,
    )
    ax.fill_between(
        x_colour_points,
        y_points_reality,
        y_points_reg,
        where=(y_points_reality < y_points_reg),
        color="lightgrey",
        alpha=0.5,
        interpolate=True,
    )


def plot_subject_condition_comparison(
    ax, line_number, x_points_base, x_points_right, y_points
):
    jitter_values = [random() / 200 for _ in range(len(x_points_base))]
    if line_number < 15:
        x_points_jitter = np.array(x_points_right) + np.array(jitter_values)
    else:
        x_points_jitter = np.array(x_points_right) - np.array(jitter_values)

    ax.plot(
        x_points_jitter,
        y_points,
        mfc="gray",
        marker="^",
        alpha=0.6,
        markersize=3,
        linestyle="",
        mec="none",
    )

#############################
# DATA SUMMARIES
#############################

def return_subject_between_condition_comparisons_kathy(subject_data, measure):
    if measure == "R2":
        func = calculate_r2
    elif measure == "intercept":
        func = calculate_reg_intercept
    else:
        func = calculate_reg_slope

    d1_dom = func(
        subject_data.day1_dominant.ACTUAL, subject_data.day1_dominant.PERCEIVED
    )
    d1_non_dom = func(
        subject_data.day1_non_dominant.ACTUAL, subject_data.day1_non_dominant.PERCEIVED
    )
    d2_dom_1 = func(
        subject_data.day2_dominant_1.ACTUAL, subject_data.day2_dominant_1.PERCEIVED
    )
    d2_dom_2 = func(
        subject_data.day2_dominant_2.ACTUAL, subject_data.day2_dominant_2.PERCEIVED
    )

    dom_vs_non_dom = d1_dom - d1_non_dom

    dom_d1_vs_d2 = d1_dom - d2_dom_1

    dom_d2_vs_d2 = d2_dom_1 - d2_dom_2

    return dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2


#########################################################################
# RESULT WRITING
##########################################################################


def write_result_header(experiment, result_name):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write("\n")
    results.write("#####" * 20)
    results.write(f"\n\n{result_name}\n\n")
    results.close()


def write_regression_results(experiment, x, y, intercept, slope, condition_name):
    results = open(f"./results/results_{experiment}.txt", "a")
    t_vals, t_test, f_test = regression_summary(x, y)
    r, ci = pearson_r_ci(x, y)
    pearson, ols = "Pearson's", "OLS"
    intercept_text, slope_text = f"{intercept:4.2f}", f"{slope:4.2f}"
    condition_name = condition_name.upper()
    results.write(
        f"\n##### {condition_name:20s}\n{pearson:20s}r         = {r:10s}     ci    = {ci:10s}\n{ols:20s}intercept = {intercept_text:10s}     slope = {slope_text:10s}"
    )
    results.write(
        f"\n\nOLS Model Summary:\nt VALUES: {t_vals}\n\nt TEST:\n {t_test}\n\nf TEST:\n {f_test} \n"
    )
    results.close()


def write_correlation(experiment, x, y, condition_name):
    results = open(f"./results/results_{experiment}.txt", "a")
    r, ci = pearson_r_ci(x, y)
    pearson = "Pearson's r [95%CI]:"
    condition_name = condition_name
    results.write(f"\n{condition_name:^20s}\n{pearson:25s}{r:5s} {ci}\n")
    results.close()


def write_example_subject_name(experiment, example_subject):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write(f"{example_subject}\n")
    results.close()


def write_example_subject_header(experiment):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write(
        f'{"CONDITION":20s}{"INTERCEPT":20s}{"SLOPE":20s}{"ERROR (cm^2 / cm)":20s}{"VARIABILITY (R^2)":20s}\n'
    )
    results.close()


def write_example_subject_results(
    experiment, condition_name, intercept, slope, area, R2
):
    results = open(f"./results/results_{experiment}.txt", "a")
    intercept_text = f"{intercept:4.2f}"
    slope_text = f"{slope:4.2f}"
    area_text = f"{area:4.2f}"
    R2_text = f"{R2:4.2f}"

    results.write(
        f"{condition_name:20s}{intercept_text:20s}{slope_text:20s}{area_text:20s}{R2_text:20s}\n"
    )
    results.close()


def write_mean_ci_header(experiment):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write(f'{"CONDITION":20s}{"MEASURE":27s}{"MEAN":10s}95%CI\n')
    results.close()


def write_difference_mean_ci_header(experiment):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write(f'{"DIFFERENCE":47s}{"MEAN":10s}95%CI\n')
    results.close()


def write_mean_ci_result(experiment, mean, ci, y_label, x_label):
    results = open(f"./results/results_{experiment}.txt", "a")
    mean_text = f"{mean:4.2f}"
    ci_lower = f"{mean - ci:4.2f}"
    ci_upper = f"{mean + ci:4.2f}"
    results.write(
        f"{x_label:20s}{y_label:27s}{mean_text:10s}[{ci_lower} - {ci_upper}]\n"
    )
    results.close()


def write_measure_header(experiment, measure):
    results = open(f"./results/results_{experiment}.txt", "a")
    results.write(f"\n{measure.upper()}\n")
    results.close()


#################################
# REGRESSION LINE CHARACTERISTICS
#################################

def return_subject_regression_line_type(x_intersect, y_at_x2, experiment):
    if experiment == "exp1":
        x1 = 2
        x2 = 10
    elif experiment == "exp2":
        x1 = 3
        x2 = 9
    else:
        print("experiment not defined - subject group function")

    if x1 <= x_intersect <= x2 and y_at_x2 >= 0:
        group = "crosser"
    elif x1 <= x_intersect <= x2:
        group = "crosser_triangle"
    elif y_at_x2 >= 2:
        group = "maximiser"
    else:
        group = "minimiser"
    return group


def return_point_of_intersection_regression_line_and_reality_line(intercept, slope):
    m1, b1 = 1, 0
    m2, b2 = slope, intercept

    if m1 - m2 == 0:
        print("zero gradient difference")
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope) + intercept
    return x_intersect, y_intersect


def return_regression_line_endpoints(actual, perceived, experiment):
    intercept, slope = calculate_regression_general(actual, perceived)
    if experiment == "exp1":
        x1 = 2
        x2 = 10
    elif experiment == "exp2":
        x1 = 3
        x2 = 9
    else:
        print("experiment not defined reg line endpoints")
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    return x1, x2, y1, y2

