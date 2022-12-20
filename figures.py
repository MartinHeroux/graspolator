import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import numpy as np
from termcolor import colored
from pathlib import Path
from matplotlib.ticker import MultipleLocator

import summarise
import utils
import calculate_area

LOVISA = 'exp2'

KATHY = "exp1"

font = "arial"


def generate_all(all_subject_data, subjects, experiment, vertical_y_label=True):

    figure_2_and_6(all_subject_data, subjects, experiment, vertical_y_label)
    figure_3_and_7(all_subject_data, subjects, experiment, vertical_y_label)

    if experiment == "exp2":
        figure_4(all_subject_data, experiment, vertical_y_label)
        figure_5(all_subject_data)

    if experiment == "exp1":
        figure_8(all_subject_data, experiment, vertical_y_label)


def figure_2_and_6(all_subject_data, subjects, experiment, vertical_y_label):
    plot = "Example participants and group regression summary"
    font = "arial"
    example = utils.ExampleParticipantIDs

    if vertical_y_label:
        rotation = 90
        y_label = 'Perceived width (cm)'
        left_adjust = 0.125
    else:
        rotation = 0
        y_label = 'Perceived\nwidth (cm)'
        left_adjust = 0.15

    if experiment == KATHY:
        figure = "Figure_6"
        subject_1_ID = example.exp1_participant_1
        subject_2_ID = example.exp1_participant_2
        data_list = utils.store_example_subject_data_kathy(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )

        condition_names = [
            "day 1 dominant",
            "day 1 non-dominant",
            "day 2 dominant 1",
            "day 2 dominant 2",
        ]
        x_lims = [0, 12]
        x_data_lims = [2, 10]
        subplot_left_col = [1, 4, 7, 10]
        subplot_bottom_row = [10, 11, 12]
        group_plot_indices = [3, 6, 9, 12]
        colors = ["darkgray", "dimgrey"]
        example_subjects = [subject_1_ID, subject_2_ID]
        x_ticks = list(range(0, 13, 2))
        label_list = ["A", "B", "C", "D"]
        y_lim = [0, 16]
        example_subject_labels = ["Participant 1", "Participant 2"]
        text_coordinates = (-4, 16)
        subplot_rows = 4
        subplot_cols = 3
        plot_indices_list = [[1, 4, 7, 10], [2, 5, 8, 11]]

    else:
        figure = "Figure_2"
        subject_1_ID = example.exp2_participant_1
        subject_2_ID = example.exp2_participant_2
        data_list = utils.store_example_subject_data_lovisa(
            all_subject_data, subjects, subject_1_ID, subject_2_ID
        )
        condition_names = ["line to width", "width to line", "width to width"]
        x_lims = [2, 10]
        x_data_lims = [3, 9]
        subplot_left_col = [1, 4, 7]
        subplot_bottom_row = [7, 8, 9]
        group_plot_indices = [3, 6, 9]
        colors = ["darkgray", "dimgrey"]
        example_subjects = [subject_1_ID, subject_2_ID]
        x_ticks = list(range(2, 12, 2))
        label_list = ["A", "B", "C"]
        y_lim = [0, 14]
        example_subject_labels = ["Participant 1", "Participant 2"]
        text_coordinates = (-1, 14)
        subplot_rows = 3
        subplot_cols = 3
        plot_indices_list = [[1, 4, 7], [2, 5, 8]]

    if not vertical_y_label:
        figure = figure + '_horizontal'

    save_path = utils.create_figure_save_path(figure)
    y_ticks = list(range(0, 17, 2))

    print(f'Starting {figure}.\n')

    plt.figure(figsize=(17.5 / 2.4, 22 / 2.4))
    plt.rcParams.update({"font.family": font})
    # plot example subjects in left and centre subplot cols
    print(f'{figure} - plotting example participants')
    for column, (
        example_subject_data,
        color,
        plot_indices,
        example_subject,
    ) in enumerate(
        zip(data_list, colors, plot_indices_list, example_subjects), start=1
    ):
        # plot each condition data
        for condition_data, condition_plot_index, condition_name, label in zip(
            example_subject_data, plot_indices, condition_names, label_list
        ):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)
            if condition_plot_index == 1:
                plt.title(
                    example_subject_labels[0], loc="center", size=10, fontfamily=font
                )
            if condition_plot_index == 2:
                plt.title(
                    example_subject_labels[1], loc="center", size=10, fontfamily=font
                )

            intercept, slope = utils.calculate_regression_general(
                condition_data.ACTUAL, condition_data.PERCEIVED
            )
            area = calculate_area.between_regression_and_reality_absolute(
                condition_data.ACTUAL, condition_data.PERCEIVED, experiment
            )
            r2 = utils.calculate_r2(condition_data.ACTUAL, condition_data.PERCEIVED)

            ax = plt.gca()

            plt.plot(x_lims, x_lims, "k--", linewidth=1)  # plot line of 'reality'
            utils.plot_data_scatter(
                ax, condition_data.ACTUAL, condition_data.PERCEIVED, color
            )
            print(f"{figure} {example_subject}: {condition_name} {len(condition_data.ACTUAL)} data points")
            utils.plot_regression_line(
                ax, intercept, slope, color, x_data_lims[0], x_data_lims[1]
            )
            utils.shade_area(ax, intercept, slope, x_data_lims[0], x_data_lims[1])

            legend_handles = [
                mpatches.Rectangle(
                    (15, 6.0),
                    width=30,
                    height=1,
                    color="white",
                    alpha=0.5,
                    label=f"{r2:3.2f}",
                ),
                mpatches.Rectangle(
                    (15, 6.0),
                    width=30,
                    height=1,
                    color="white",
                    alpha=0.5,
                    label=f"{area:3.1f}",
                ),
            ]
            plt.legend(
                handles=legend_handles,
                loc="upper left",
                facecolor="white",
                framealpha=1,
                fontsize=8,
                handlelength=3,
                handleheight=1,
                edgecolor="none",
            )

            # plt.text(0.05, 0.89, 'Variability', fontfamily=font, fontsize=8, transform=plt.gca().transAxes, zorder=20)
            utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lim, None, None, 10, True)

            if experiment == LOVISA:
                y_var = 0.8955
                y_err = 0.815
            else:
                y_var = 0.885
                y_err = 0.79
            ax.text(0.1, y_var, 'R$^2$', fontsize=8, transform=ax.transAxes, zorder=10)
            ax.text(0.1, y_err, 'Error', fontsize=8, transform=ax.transAxes, zorder=10)

            utils.draw_ax_spines(ax, False, False, False, False)
            ax.tick_params(
                axis="both",
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
                labeltop=False,
                labelleft=False,
                labelright=False,
            )

            # draw axes, labels, and ticks for left column and bottom row subplots
            if condition_plot_index in subplot_left_col:
                ax.tick_params(axis="y", which="both", left=True, labelleft=True)
                ax.spines["left"].set_visible(True)
                plt.text(
                    text_coordinates[0],
                    text_coordinates[1],
                    label,
                    fontsize=14,
                    fontfamily=font,
                )
            if condition_plot_index == 4 and experiment == "exp2":
                ax.set_ylabel(
                    y_label, fontfamily="arial", fontsize=10, rotation=rotation
                )
            elif condition_plot_index == 7 and experiment == KATHY:
                ax.set_ylabel(
                    y_label, fontfamily="arial", fontsize=10, rotation=rotation
                )

            if condition_plot_index in subplot_bottom_row:
                ax.tick_params(axis="x", which="both", bottom=True, labelbottom=True)
                ax.spines["bottom"].set_visible(True)
            if condition_plot_index == 11 and experiment == KATHY:
                plt.xlabel("Actual width (cm)", fontsize=10, fontfamily=font)
            if condition_plot_index == 8 and experiment == "exp2":
                plt.xlabel("Actual width (cm)", fontsize=10, fontfamily=font)

    # plot group regression lines in the right subplot column

    for subject_ID, subject_data in zip(subjects, all_subject_data):
        data_list = utils.create_data_tuples(experiment, subject_data)
        for condition_tuple, condition_plot_index, label, condition_name in zip(
            data_list, group_plot_indices, label_list, condition_names
        ):
            plt.subplot(subplot_rows, subplot_cols, condition_plot_index)

            if condition_plot_index == 3:
                plt.title("All participants", loc="center", size=10, fontfamily=font)

            if subject_ID == example_subjects[0]:
                line_color = "darkgrey"
                line_width = 0.5
                order = 10
            elif subject_ID == example_subjects[1]:
                line_color = "darkgrey"
                line_width = 0.5
                order = 10
            else:
                line_color = "darkgrey"
                line_width = 0.5
                order = 5

            intercept, slope = utils.calculate_regression_general(
                condition_tuple.ACTUAL, condition_tuple.PERCEIVED
            )
            alpha = 0.7

            ax = plt.gca()

            plt.plot(x_lims, x_lims, "k--", linewidth=1)
            utils.plot_regression_line(
                ax,
                intercept,
                slope,
                line_color,
                x_data_lims[0],
                x_data_lims[1],
                alpha,
                line_width,
                order,
            )

            utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lim, None, None, 10, True)
            utils.draw_ax_spines(ax, False, False, False, False)
            ax.tick_params(
                axis="both",
                which="both",
                bottom=False,
                top=False,
                left=False,
                right=False,
                labelbottom=False,
                labeltop=False,
                labelleft=False,
                labelright=False,
            )

            # turn grid back on
            plt.grid(True, axis="both", linewidth=0.5, color="lightgrey")

            # draw axes and ticks for bottom row
            if condition_plot_index in subplot_bottom_row:
                plt.gca().spines["bottom"].set_visible(True)
                plt.gca().tick_params(
                    axis="x", which="both", bottom=True, labelbottom=True
                )

    """
    if experiment == 'exp2':
        plt.subplot(subplot_rows, subplot_cols, 12)
        plt.plot([4, 6], [6, 8])
        plt.xticks(x_ticks, fontfamily=font, fontsize=8)
        plt.xlim([x_lims[0], x_lims[1]])
        plt.gca().tick_params(axis='both', which='both', bottom=True, top=False, left=False, right=False,
                              labelbottom=True,
                              labeltop=False, labelleft=False, labelright=False)
        plt.gca().spines['left'].set_visible(False)
        plt.gca().spines['right'].set_visible(False)
    """

    if experiment == "exp2":
        plt.subplots_adjust(left=left_adjust, bottom=0.25, right=0.95, top=0.95)
    else:
        plt.subplots_adjust(left=left_adjust, right=0.95, top=0.95)

    plt.savefig(save_path, dpi=300)
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)

    png_text = colored(save_path, "blue")
    print(f"{png_text} saved\n")
    svg_text = colored(path_svg, 'blue')
    print(f"{svg_text} saved\n")
    plt.close()


def figure_3_and_7(all_subject_data, subjects, experiment, vertical_y_label=True):
    font = "arial"
    if experiment == KATHY:
        figure = "Figure_7"
    else:
        figure = "Figure_3"

    print(f'Starting {figure}.\n')

    if not vertical_y_label:
        figure = figure + '_horizontal'
    save_path = utils.create_figure_save_path(figure)

    x_points, x_lims = utils.x_points_group_plot(experiment)
    x_labels = utils.x_tick_labels_group_plot(experiment)
    plot_text = ["B", "A"]
    results_headers = ["R^2", "Error (cm2 / cm)"]
    params = utils.r2_area_constants()

    if vertical_y_label:
        y_label_error = "Error (cm$^2$ / cm)"
        y_label_r2 = "Variability (R$^2$)"
        rotation = 90
    else:
        y_label_error = "Error\n(cm$^2$ / cm)"
        y_label_r2 = "Variability\n(R$^2$)"
        rotation = 0

    if experiment == KATHY:
        colors = params.exp_1_colors
        example_subjects = params.exp_1_subjects
        y_lims = [(0.7, 1), (0, 3)]
        condition_names = [
            "day 1 dominant",
            "day 1 non-dominant",
            "day 2 dominant 1",
            "day 2 dominant 2",
        ]
        x_ticks = [0.95, 2, 3, 4.05]
        text_y = 3.1
        x_label_size = 8
    else:
        colors = params.exp_2_colors
        example_subjects = params.exp_2_subjects
        y_lims = [(0.6, 1), (0, 4)]
        condition_names = ["Grasp-to-grasp", "Grasp-to-vision", "Vision-to-grasp"]
        x_ticks = [0.95, 2, 3.05]
        text_y = 4.1
        x_label_size = 10

    r2_means, r2_cis = summarise.r2_mean_and_ci_by_condition(
        all_subject_data, experiment
    )
    area_means, area_cis = summarise.area_mean_and_ci_by_condition(
        all_subject_data, experiment
    )

    vision_to_grasp = 0
    grasp_to_vision = 1
    grasp_to_grasp = -1

    if experiment == 'exp2':    # change order of x-axis so that grasp-to-grasp is first
        r2_means = [r2_means[grasp_to_grasp], r2_means[grasp_to_vision], r2_means[vision_to_grasp]]
        r2_cis = [r2_cis[grasp_to_grasp], r2_cis[grasp_to_vision], r2_cis[vision_to_grasp]]
        area_means = [area_means[grasp_to_grasp], area_means[grasp_to_vision], area_means[vision_to_grasp]]
        area_cis = [area_cis[grasp_to_grasp], area_cis[grasp_to_vision], area_cis[vision_to_grasp]]

    means_lists, ci_lists = [r2_means, area_means], [r2_cis, area_cis]

    plt.figure(figsize=(3.3, (2.7 * 2)))
    for subject, subject_data in zip(subjects, all_subject_data):
        data_pairs = utils.create_data_tuples(experiment, subject_data)
        if experiment == 'exp2':    # change order of x-axis so that grasp-to-grasp is first
            data_pairs = [data_pairs[grasp_to_grasp], data_pairs[grasp_to_vision], data_pairs[vision_to_grasp]]
        y_points_r2 = []
        y_points_area = []

        if subject == example_subjects[0]:
            line_color, line_width, order, alpha = "grey", 0.5, 5, 0.3
        elif subject == example_subjects[1]:
            line_color, line_width, order, alpha = "grey", 0.5, 5, 0.3
        else:
            line_color, line_width, order, alpha = "grey", 0.5, 5, 0.3

        for pair in data_pairs:
            y_points_r2.append(utils.calculate_r2(pair.ACTUAL, pair.PERCEIVED))
            y_points_area.append(
                calculate_area.between_regression_and_reality_absolute(pair.ACTUAL, pair.PERCEIVED, experiment)
            )

        y_point_lists = [y_points_r2, y_points_area]

        for subplot, y_points, y_label, y_tick, y_lim, text in zip(
            params.subplot_indices,
            y_point_lists,
            params.y_labels,
            params.y_ticks,
            y_lims,
            plot_text,
        ):
            plt.subplot(2, 1, subplot)
            plt.plot(
                x_points,
                y_points,
                color=line_color,
                alpha=alpha,
                linewidth=line_width,
                zorder=order,
            )
            ax = plt.gca()
            if subplot == 1:
                ax.tick_params(
                    axis="both",
                    which="both",
                    bottom=False,
                    top=False,
                    left=True,
                    right=False,
                    labelbottom=False,
                    labeltop=False,
                    labelleft=True,
                    labelright=False,
                )
                utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)
                plt.gca().text(0.5, text_y, text, fontsize=14, fontfamily=font)

            else:
                ax.tick_params(axis="both", which="both", bottom=True, labelbottom=True)
                utils.draw_ax_spines(
                    ax,
                    left=True,
                    right=False,
                    top=False,
                    bottom=True,
                    x_offset=True,
                    y_offset=True,
                )
                plt.gca().text(0.5, 1.01, text, fontsize=14, fontfamily=font)

            if experiment == 'exp1':
                x_ticks_fontsize = 8
            else:
                x_ticks_fontsize = 10
            utils.set_ax_parameters(ax, x_ticks, y_tick, x_labels, y_tick, x_lims, y_lim, None, None, x_ticks_fontsize,
                                    False, 'arial', y_fontsize=10)

            if experiment == KATHY and subplot == 2:
                plt.ylim(0.70, 1)

    for mean_list, ci_list, subplot, y_label in zip(
        means_lists, ci_lists, params.subplot_indices, results_headers
    ):
        plt.subplot(2, 1, subplot)
        for mean, ci, x_point, x_label in zip(
            mean_list, ci_list, x_points, condition_names
        ):
            plt.errorbar(
                x_point,
                mean,
                yerr=ci,
                ecolor="black",
                marker="o",
                markerfacecolor="black",
                mec="black",
                markersize=3,
                linewidth=1,
                zorder=11,
            )
        if subplot == 1:
            plt.ylabel(y_label_error, fontfamily=font, fontsize=10, rotation=rotation)
        else:
            plt.ylabel(y_label_r2, fontfamily=font, fontsize=10, rotation=rotation)

        ax = plt.gca()
        add_plot_text(ax, subplot, experiment, fontsize=10)
        utils.add_plot_shading(
            ax,
            subplot,
            experiment,
            params.r2_ci_lower,
            params.r2_ci_upper,
            params.area_ci_lower,
            params.area_ci_upper,
        )

    plt.grid(False)
    # plt.tight_layout(h_pad=0.6, w_pad=0.9)
    plt.subplots_adjust(left=0.25, right=0.9)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    text = colored(save_path, "blue")
    text_svg = colored(path_svg, "blue")
    print(f"{text} saved\n")
    print(f"{text_svg} saved\n")
    plt.close()


def figure_4(all_subject_data, experiment, vertical_y_label=True):
    font = "arial"
    figure_name = "Figure_4"
    print(f'Starting {figure_name}.\n')
    if not vertical_y_label:
        figure_name = figure_name + '_horizontal'
    save_path = utils.create_figure_save_path(figure_name)

    # store data for plot
    error_lists = summarise.errors_per_condition(all_subject_data, experiment)
    variability_lists = summarise.r2_data_by_condition(all_subject_data, experiment)

    x_labels = utils.x_tick_labels_group_plot(experiment)
    if experiment == KATHY:
        subplot_indices = [1, 2, 3, 4]
        subplot_labels = ["A", "B", "C", "D"]
    else:
        subplot_indices = [1, 2, 3]
        subplot_labels = ["A", "B", "C"]

    if vertical_y_label:
        y_label = "Variability (R$^2$)"
        rotation = 90
        left_adjust = 0.125
    else:
        y_label = "Variability\n(R$^2$)"
        rotation = 0
        left_adjust = 0.25

    x_lims, y_lims = (0, 3), (0.6, 1)
    x_ticks, y_ticks = [0, 1, 2, 3], [0.6, 0.7, 0.8, 0.9, 1]
    x_label = None

    plt.figure(figsize=(3.3, (2.7 * 3)))
    plt.rcParams.update({"font.family": font})
    for (
        subplot_index,
        condition_r2_data,
        condition_area_data,
        condition_name,
        text,
    ) in zip(subplot_indices, variability_lists, error_lists, x_labels, subplot_labels):
        # condition_area_data.pop(20)
        # condition_r2_data.pop(20)
        intercept, slope = utils.calculate_regression_general(
            condition_area_data, condition_r2_data
        )

        plt.subplot(subplot_indices[-1], subplot_indices[0], subplot_index)
        x_vals = np.array([0, max(condition_area_data)])
        y_vals = intercept + slope * x_vals
        plt.plot(x_vals, y_vals, color="black", linewidth=1, zorder=11)
        plt.scatter(
            condition_area_data,
            condition_r2_data,
            c="dimgray",
            marker="o",
            alpha=0.6,
            s=5,
            linewidths=0,
            zorder=10,
        )

        ax = plt.gca()

        if subplot_index in [2, 3]:
            y_ticks = [0.7, 0.8, 0.9, 1]
            y_lims = (0.7, 1)

        utils.draw_ax_spines(
            ax, True, False, False, False, x_offset=True, y_offset=True
        )
        ax.tick_params(
            axis="both",
            which="both",
            bottom=False,
            top=False,
            left=True,
            right=False,
            labelbottom=False,
            labeltop=False,
            labelleft=True,
            labelright=False,
        )

        utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lims, x_label, None, 10, False,
                                font=font)

        # draw axes and ticks for bottom subplot
        if subplot_index == 3 and experiment == "exp2":
            plt.xlabel("Error (cm$^2$ / cm)", size=10, fontfamily=font)
            ax.tick_params(
                axis="both",
                which="both",
                bottom=True,
                labelbottom=True,
                left=True,
                labelleft=True,
            )
            ax.spines["bottom"].set_visible(True)

        if subplot_index == 2:
            plt.ylabel(
                y_label, fontsize=10, fontfamily=font, rotation=rotation
            )

        # label subplot letter (A, B, C, +/- D)
        plt.gca().text(-0.5, 1.01, text, fontsize=14, fontfamily=font)

    plt.subplots_adjust(left=left_adjust, right=0.95, top=0.9, bottom=0.1)
    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    text = colored(save_path, "blue")
    text_svg = colored(path_svg, "blue")
    print(f"{text} saved\n")
    print(f"{text_svg} saved\n")
    plt.close()


def figure_5(all_subject_data):
    figure = "Figure_5"
    print(f'Starting {figure}.\n')
    save_path = utils.create_figure_save_path(figure)

    slopes_line_width = []
    slopes_width_line = []

    x_lims, y_lims = (0.4, 1.6), (0.4, 2.0)
    x_ticks, y_ticks = [0.4, 0.8, 1.2, 1.6, 2], [0.4, 0.8, 1.2, 1.6, 2]
    x_label, y_label = (
        "Vision-to-grasp regression slope",
        "Grasp-to-vision regression slope",
    )

    for subject_data in all_subject_data:
        intercept_line_width, slope_line_width = utils.calculate_regression_general(
            subject_data.LINE_WIDTH.ACTUAL, subject_data.LINE_WIDTH.PERCEIVED
        )
        intercept_width_line, slope_width_line = utils.calculate_regression_general(
            subject_data.WIDTH_LINE.ACTUAL, subject_data.WIDTH_LINE.PERCEIVED
        )
        slopes_line_width.append(slope_line_width)
        slopes_width_line.append(slope_width_line)

    plt.figure(figsize=(3.3, 2.7))
    intercept, slope = utils.calculate_regression_general(
        slopes_line_width, slopes_width_line
    )

    # print and plot results without outlier
    for count, (slope_1, slope_2) in enumerate(zip(slopes_line_width, slopes_width_line)):
        if slope_2 > 1.7:
            plt.plot(
                slope_1,
                slope_2,
                marker="x",
                color="gray",
                markeredgecolor="gray",
                markersize=3,
                markeredgewidth=0.5,
            )
            slopes_line_width.pop(count)
            slopes_width_line.pop(count)


    x_vals = np.array([min(slopes_line_width) - 0.25, max(slopes_line_width) + 0.25])
    y_vals = intercept + slope * x_vals

    # plot regression line
    plt.plot(x_vals, y_vals, color="black", linewidth=1, zorder=10)
    # plot individual slope values
    plt.scatter(
        slopes_line_width,
        slopes_width_line,
        c="gray",
        marker="o",
        alpha=0.6,
        s=5,
        zorder=5,
        linewidths=0,
    )

    ax = plt.gca()
    utils.draw_ax_spines(ax, True, False, False, True)
    ax.spines["bottom"].set(linewidth=0.75)
    ax.spines["left"].set(linewidth=0.75)
    utils.set_ax_parameters(ax, x_ticks, y_ticks, x_ticks, y_ticks, x_lims, y_lims, x_label, y_label, 10, False)
    plt.tight_layout()

    plt.savefig(save_path, dpi=300)
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    text = colored(save_path, "blue")
    text_svg = colored(path_svg, "blue")
    print(f"{text} saved\n")
    print(f"{text_svg} saved\n")
    plt.close()


def figure_8(all_subject_data, experiment, vertical_y_axis=True):
    font = "arial"
    figure = "Figure_8"
    print(f'Starting {figure}.\n')
    if not vertical_y_axis:
        figure = figure + '_horizontal'
    save_path = utils.create_figure_save_path(figure)

    subplots = [1, 2, 3, 4]
    measures = ["area", "R2", "intercept", "slope"]

    x_ticks = [1.3, 1.45, 1.6]
    x_points_left = [1.3, 1.45, 1.6]
    x_points_right = [1.315, 1.465, 1.615]
    x_tick_labels = ["Between hands", "Within hand", "Within hand"]
    x_descriptors = ["Same day", "1 week apart", "Same day"]
    x_lim = [1.295, 1.63]
    text_y_points = [1.5, 0.21, 2.1, 0.55]
    text_letters = ['A', 'B', 'C', 'D']

    if vertical_y_axis:
        measure_labels = [
            "error (cm$^2$) / cm",
            "variability (R$^2$)",
            "y-intercept",
            "slope",
        ]
        left_adjust = 0.125
    else:
        measure_labels = [
            "error\n(cm$^2$) / cm",
            "variability\n(R$^2$)",
            "y-intercept",
            "slope",
        ]
        left_adjust = 0.25

    plt.figure(figsize=(3.3, (2.7 * 4)))

    for subplot, measure, label, text_y_point, letter in zip(subplots, measures, measure_labels, text_y_points, text_letters):
        between_hands, across_days, within_day = [], [], []
        y_label = f"\u0394 {label}"

        plt.subplot(4, 1, subplot)
        ax = plt.gca()

        for line_number, subject_data in enumerate(all_subject_data, start=1):
            if measure == "area":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = summarise.absolute_condition_comparison_areas(
                    subject_data, experiment
                )
                y_ticks = [-1.4, -0.7, 0, 0.7, 1.4]
                y_lim = [-1.4, 1.4]
            elif measure == "intercept":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )
                y_ticks = list(range(-2, 3))
                y_lim = [-2, 2]
            elif measure == "slope":
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )
                y_lim = [-0.5, 0.5]
                y_ticks = [-0.5, -0.25, 0, 0.25, 0.5]
            else:
                (
                    dom_vs_non_dom,
                    dom_d1_vs_d2,
                    dom_d2_vs_d2,
                ) = utils.return_subject_between_condition_comparisons_kathy(
                    subject_data, measure
                )
                y_lim = [-0.2, 0.2]
                y_ticks = [-0.2, -0.1, 0, 0.1, 0.2]

            utils.plot_subject_condition_comparison(
                ax,
                line_number,
                x_ticks,
                x_points_right,
                [dom_vs_non_dom, dom_d1_vs_d2, dom_d2_vs_d2],
            )

            between_hands.append(dom_vs_non_dom)
            across_days.append(dom_d1_vs_d2)
            within_day.append(dom_d2_vs_d2)

        all_differences = [between_hands, across_days, within_day]

        for x_point, difference_list, label, descriptor in zip(
            x_points_left, all_differences, x_tick_labels, x_descriptors
        ):
            mean, ci = utils.calculate_mean_ci(difference_list)
            plt.errorbar(
                x_point,
                mean,
                yerr=ci,
                ecolor="black",
                marker="^",
                markerfacecolor="black",
                mec="black",
                markersize=3.5,
                elinewidth=1,
                zorder=10,
            )

        utils.draw_ax_spines(
            ax,
            left=True,
            right=False,
            top=False,
            bottom=False,
            x_offset=True,
            y_offset=True,
        )
        utils.set_ax_parameters(ax, [], y_ticks, [], y_ticks, x_lim, y_lim, None, y_label, 10, True)
        plt.grid(False)

        if subplot == 4:
            utils.draw_ax_spines(
                ax,
                left=True,
                right=False,
                top=False,
                bottom=True,
                x_offset=True,
                y_offset=True,
            )
            utils.set_ax_parameters(ax, x_ticks, y_ticks, x_tick_labels, y_ticks, x_lim, y_lim, None, y_label, 10, True)
            # plt.text(1.2, 0.01, 'A', fontsize=12, fontfamily='arial', color='white')
            plt.text(
                0.073,
                0.065,
                "Same day",
                fontsize=10,
                fontfamily=font,
                transform=plt.gcf().transFigure,
            )
            plt.text(
                0.383,
                0.065,
                "1 week apart",
                fontsize=10,
                fontfamily=font,
                transform=plt.gcf().transFigure,
            )
            plt.text(
                0.75,
                0.065,
                "Same day",
                fontsize=10,
                fontfamily=font,
                transform=plt.gcf().transFigure,
            )

        plt.grid(False)
        plt.plot([1, 3], [0, 0], color="dimgrey", linewidth=0.5, zorder=5)

        # turn grid off for x axis

        plt.gca().text(
            1.22,
            text_y_point,
            letter,
            fontfamily="arial",
            fontsize=14,
        )

    plt.subplots_adjust(left=left_adjust, right=0.95, top=0.9, bottom=0.1)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    text = colored(save_path, "blue")
    text_svg = colored(path_svg, "blue")
    print(f"{text} saved\n")
    print(f"{text_svg} saved\n")
    plt.close()


def add_plot_text(ax, subplot, experiment, font="arial", fontsize=10):
    if subplot == 2 and experiment == KATHY:
        ax.text(
            0.1, -0.25, "Day 1", fontsize=fontsize, fontfamily=font, transform=ax.transAxes
        )
        ax.text(
            0.75, -0.25, "Day 2", fontsize=fontsize, fontfamily=font, transform=ax.transAxes
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
