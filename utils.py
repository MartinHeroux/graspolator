import os
from pathlib import Path
import statsmodels.api as sm
import yaml
from PyPDF2 import PdfFileMerger


def exp1_subject_folders() -> object:
    return (
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
    )


def calculate_regression(block):
    x = block.actual_widths
    y = block.perceived_widths
    x = sm.add_constant(x)
    model = sm.OLS(y, x).fit()
    intercept, slope = model.params
    return intercept, slope

def calculate_regression_all_data(actual, perceived):
    actual = sm.add_constant(actual)
    model = sm.OLS(perceived, actual).fit()
    intercept, slope = model.params
    return intercept, slope

def read_yaml_corrections_file(fix_yaml):
    if not fix_yaml.is_file():
        return
    with open(fix_yaml) as config_file:
        return yaml.load(config_file, Loader=yaml.FullLoader)


def create_exp_folder(experiment):
    if not os.path.exists('./subject_folders_' + experiment):
        os.makedirs('./subject_folders_' + experiment)
        print("All-subject folder created " + experiment)
    else:
        print("All-subject folder already exists")


def create_subject_folder(subject_ID):
    if not os.path.exists('./subject_folders_exp1/' + subject_ID):
        os.makedirs('./subject_folders_exp1/' + subject_ID)
        print(str(subject_ID + ' folder created'))
    else:
        print(str(subject_ID + " folder already exists, proceeding"))

def filename_list(directory):
    filenames = []
    for root, dirs, files in os.walk(directory):
        for filename in files:
            filenames.append(filename)
    return filenames

def merge_pdfs(source_directory):
    filenames = filename_list(source_directory)
    merger = PdfFileMerger()
    for filename in filenames:
        pdf_path = str(Path('./randomised_plots_no_ID/', filename))
        merger.append(pdf_path)
    merger.write("concatenated.pdf")
    merger.close()

def point_of_intersection(intercept, slope):
    m1, b1 = 1, 0
    m2, b2 = slope, intercept
    x_intersect = (b2 - b1) / (m1 - m2)
    y_intersect = (x_intersect * slope) + intercept
    return x_intersect, y_intersect


def reg_line_endpoints(intercept, slope):
    x2 = 2
    x10 = 10
    y_at_x2 = slope * x2 + intercept
    y_at_x10 = slope * x10 + intercept
    return x2, x10, y_at_x2, y_at_x10

def subject_group(x_intersect, y_at_x2):
    if 2 <= x_intersect <= 10 and y_at_x2 >= 0:
        group = 'crosser'
    elif 2 <= x_intersect <= 10:
        group = 'crosser_triangle'
    elif y_at_x2 >= 2:
        group = 'maximiser'
    else:
        group = 'minimiser'
    return group

def subject_line_colour(intersection_x_value, y_when_x_equals_2):
    if intersection_x_value >= 2 and intersection_x_value <= 10:
        line_colour = 'royalblue'
    elif y_when_x_equals_2 > 2:
        line_colour = 'green'
    else:
        line_colour = 'firebrick'
    return line_colour