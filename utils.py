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

