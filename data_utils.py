from dataclasses import dataclass
import outcomes


def remove_missing_data(actual_list, perceived_list, subject_ID):
    indices_to_remove = list()
    for trial in perceived_list:
        if trial == "":
            indices_to_remove.append(perceived_list.index(trial))
    indices_to_remove.reverse()
    if len(indices_to_remove) > 0:
        print(
            f"{str(len(indices_to_remove)):5s} saturated data point(s) removed for {subject_ID}\n"
        )
    for index in indices_to_remove:
        actual_list.pop(index)
        perceived_list.pop(index)
    return actual_list, perceived_list


def read_subject_data(subject_folder):
    path_to_data_file = subject_folder / (subject_folder.name + "_data.txt")
    with open(path_to_data_file) as file:
        current_subject_data = file.readlines()
    return current_subject_data


@dataclass
class GraspolatorBlock:
    actual: list
    perceived: list
    plot_index: int = 999
    r_squared: float = 999
    mean_abs_error: float = 999
    slope: float = 999
    intercept: float = 999

    def compute_outcomes(self):
        r_squared, intercept, slope = outcomes.regression(self.actual, self.perceived)
        self.r_squared = r_squared
        self.intercept = intercept
        self.slope = slope
        self.mean_abs_error = outcomes.mean_abs_error(self.actual, self.perceived)
