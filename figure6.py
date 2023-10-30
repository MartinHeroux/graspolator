from pathlib import Path

import matplotlib.pyplot as plt

import constants
import figure_utils



def plot(study_data):
    # ------------------------------------------------------------------------------------------------------------------
    # Plot settings
    # ------------------------------------------------------------------------------------------------------------------
    rotation = 90
    y_label = "Perceived width (cm)"
    left_adjust = 0.125
    figure = "Figure_6"
    x_lims = [1, 11]
    x_data_lims = [2, 10]
    colors = ["darkgray", "darkgray", "darkgray", "darkgray"]
    x_ticks = list(range(0, 14, 2))
    label_list = ["A", "B", "C", "D"]
    y_lim = [0, 16]
    example_subject_labels = [
        "Participant 1",
        "Participant 2",
        "Participant 3",
        "All participants",
    ]
    text_coordinates = (-4, 17)
    subplot_rows = 4
    subplot_cols = 4
    y_ticks = list(range(0, 17, 2))

    # ------------------------------------------------------------------------------------------------------------------
    # Setting up plot
    # ------------------------------------------------------------------------------------------------------------------
    save_path = figure_utils.create_figure_save_path(figure)
    plt.figure(figsize=(7, 7))

    # ------------------------------------------------------------------------------------------------------------------
    # Get example subject data
    # ------------------------------------------------------------------------------------------------------------------
    example_subjects = [
        constants.ExampleParticipantIDs.kathy_participant_1,
        constants.ExampleParticipantIDs.kathy_participant_2,
        constants.ExampleParticipantIDs.kathy_participant_3,
    ]
    example_subject_data = list()
    for example_subject in example_subjects:
        for subject in study_data:
            if subject.subject == example_subject:
                example_subject_data.append(subject)

    # ------------------------------------------------------------------------------------------------------------------
    # plot example subjects in left and centre subplot cols
    # ------------------------------------------------------------------------------------------------------------------
    sub_num_subplots = [[1, 5, 9, 13], [2, 6, 10, 14], [3, 7, 11, 15]]
    x1 = x_data_lims[0]
    x2 = x_data_lims[1]
    for sub_num, subject_data in enumerate(example_subject_data):
        for block_num in range(4):
            plt.subplot(
                subplot_rows, subplot_cols, sub_num_subplots[sub_num][block_num]
            )
            ax = plt.gca()
            ax.plot(x_lims, x_lims, "k--", linewidth=1)  # plot line of 'reality'
            if block_num == 0:
                actual = subject_data.day1_dominant.actual
                perceived = subject_data.day1_dominant.perceived
                intercept = subject_data.day1_dominant.intercept
                slope = subject_data.day1_dominant.slope
                r_squared = subject_data.day1_dominant.r_squared
                mae = subject_data.day1_dominant.mean_abs_error
            if block_num == 1:
                actual = subject_data.day1_non_dominant.actual
                perceived = subject_data.day1_non_dominant.perceived
                intercept = subject_data.day1_non_dominant.intercept
                slope = subject_data.day1_non_dominant.slope
                r_squared = subject_data.day1_non_dominant.r_squared
                mae = subject_data.day1_non_dominant.mean_abs_error
            if block_num == 2:
                actual = subject_data.day2_dominant_1.actual
                perceived = subject_data.day2_dominant_1.perceived
                intercept = subject_data.day2_dominant_1.intercept
                slope = subject_data.day2_dominant_1.slope
                r_squared = subject_data.day2_dominant_1.r_squared
                mae = subject_data.day2_dominant_1.mean_abs_error
            if block_num == 3:
                actual = subject_data.day2_dominant_2.actual
                perceived = subject_data.day2_dominant_2.perceived
                intercept = subject_data.day2_dominant_2.intercept
                slope = subject_data.day2_dominant_2.slope
                r_squared = subject_data.day2_dominant_2.r_squared
                mae = subject_data.day2_dominant_2.mean_abs_error

            text = ["R$^2$", "Error"]
            label1 = f"{text[0]:8s} {r_squared:3.2f}\n{text[1]:6s}{mae:3.1f}"
            figure_utils.plot_data_scatter(ax, actual, perceived, colors[sub_num])
            figure_utils.plot_regression_line(
                ax, intercept, slope, colors[sub_num], x1, x2, label1=label1
            )

            #   figure_utils.plot_data_scatter(ax, actual, perceived, colors[sub_num])
            #   figure_utils.plot_regression_line(ax, intercept, slope, colors[sub_num], x1, x2)

            plt.legend(
                loc="upper left",
                bbox_to_anchor=(0.01, 0.95, 0.05, 0.05),
                facecolor="white",
                framealpha=1,
                fontsize=7,
                handlelength=0,
                handleheight=1,
                edgecolor="none",
            )

            figure_utils.set_ax_parameters(
                ax,
                x_ticks,
                y_ticks,
                x_ticks,
                y_ticks,
                x_lims,
                y_lim,
                None,
                None,
                8,
                True,
            )
            y_var = 0.86
            y_err = 0.75

            figure_utils.draw_ax_spines(ax, False, False, False, False)
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
            if sub_num == 0:
                ax.tick_params(axis="y", which="both", left=True, labelleft=True)
                ax.spines["left"].set_visible(True)

                # Set row letter ID
                plt.text(
                    text_coordinates[0],
                    text_coordinates[1],
                    label_list[block_num],
                    fontsize=12,
                )

                ax.set_ylabel(y_label, fontsize=8, rotation=rotation)

            if block_num == 3:
                ax.tick_params(axis="x", which="both", bottom=True, labelbottom=True)
                ax.spines["bottom"].set_visible(True)
                plt.xlabel("Actual width (cm)", fontsize=8)

    # ------------------------------------------------------------------------------------------------------------------
    # plot group regression lines in the right subplot column
    # ------------------------------------------------------------------------------------------------------------------
    subplots = [4, 8, 12, 16]
    for subplot in subplots:
        plt.subplot(subplot_rows, subplot_cols, subplot)
        plt.plot(x_lims, x_lims, "k--", linewidth=1)

    for subject in study_data:
        for row in range(4):
            plt.subplot(subplot_rows, subplot_cols, subplots[row])
            line_color = "darkgrey"
            line_width = 0.5
            order = 5
            alpha = 0.7
            ax = plt.gca()
            if row == 0:
                intercept = subject.day1_dominant.intercept
                slope = subject.day1_dominant.slope
            if row == 1:
                intercept = subject.day1_non_dominant.intercept
                slope = subject.day1_non_dominant.slope
            if row == 2:
                intercept = subject.day2_dominant_1.intercept
                slope = subject.day2_dominant_1.slope
            if row == 3:
                intercept = subject.day2_dominant_2.intercept
                slope = subject.day2_dominant_2.slope

            figure_utils.plot_regression_line(
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
            figure_utils.set_ax_parameters(
                ax,
                x_ticks,
                y_ticks,
                x_ticks,
                y_ticks,
                x_lims,
                y_lim,
                None,
                None,
                10,
                True,
            )
            figure_utils.draw_ax_spines(ax, False, False, False, False)
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

            plt.grid(True, axis="both", linewidth=0.5, color="lightgrey")

            if row == 3:
                plt.gca().spines["bottom"].set_visible(True)
                plt.gca().tick_params(
                    axis="x", which="both", bottom=True, labelbottom=True
                )
                plt.xlabel("Actual width (cm)", fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 1)
    plt.title(example_subject_labels[0], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 2)
    plt.title(example_subject_labels[1], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 3)
    plt.title(example_subject_labels[2], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 4)
    plt.title(example_subject_labels[3], loc="center", size=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 1)
    plt.text(-9, 7, "day 1 \ndominant", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 5)
    plt.text(-9, 7, "day 1\nnon-dominant", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 9)
    plt.text(-9, 7, "day 2\ndominant 1", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 13)
    plt.text(-9, 7, "day 2\ndominant 2", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 16)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    for i in range(16):
        plt.subplot(subplot_rows, subplot_cols, i + 1)
        plt.yticks([0, 4, 8, 12, 16])

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
