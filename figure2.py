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
    figure = "Figure_2"
    condition_names = ["line to width", "width to line", "width to width"]
    colors = ["darkgray", "darkgray", "darkgray"]
    label_list = ["A", "B", "C"]
    example_subject_labels = [
        "Participant 1",
        "Participant 2",
        "Participant 3",
        "All participants",
    ]
    x_lims = [2, 10]
    x_data_lims = [3, 9]
    y_lim = [0, 14]
    subplot_rows = 3
    subplot_cols = 4
    text_coordinates = (-2, 15)
    x_ticks = list(range(2, 12, 2))
    y_ticks = list(range(0, 17, 2))

    # ------------------------------------------------------------------------------------------------------------------
    # Setting up plot
    # ------------------------------------------------------------------------------------------------------------------
    save_path = figure_utils.create_figure_save_path(figure)
    plt.figure(figsize=(7, 5))

    # ------------------------------------------------------------------------------------------------------------------
    # Get example subject data
    # ------------------------------------------------------------------------------------------------------------------
    example_subjects = [
        constants.ExampleParticipantIDs.lovisa_participant_1,
        constants.ExampleParticipantIDs.lovisa_participant_2,
        constants.ExampleParticipantIDs.lovisa_participant_3,
    ]
    example_subject_data = list()
    for example_subject in example_subjects:
        for subject in study_data:
            if subject.subject_id == example_subject:
                example_subject_data.append(subject)

    # ------------------------------------------------------------------------------------------------------------------
    # plot example subjects in left and centre subplot cols
    # ------------------------------------------------------------------------------------------------------------------
    sub_num_subplots = [[1, 5, 9], [2, 6, 10], [3, 7, 11]]
    x1 = x_data_lims[0]
    x2 = x_data_lims[1]
    for sub_num, subject_data in enumerate(example_subject_data):
        for block_num in range(3):
            plt.subplot(
                subplot_rows, subplot_cols, sub_num_subplots[sub_num][block_num]
            )
            ax = plt.gca()
            ax.plot(x_lims, x_lims, "k--", linewidth=1)  # plot line of 'reality'
            if block_num == 0:
                actual = subject_data.line_width.actual
                perceived = subject_data.line_width.perceived
                intercept = subject_data.line_width.intercept
                slope = subject_data.line_width.slope
                r_squared = subject_data.line_width.r_squared
                mae = subject_data.line_width.mean_abs_error
            if block_num == 1:
                actual = subject_data.width_line.actual
                perceived = subject_data.width_line.perceived
                intercept = subject_data.width_line.intercept
                slope = subject_data.width_line.slope
                r_squared = subject_data.width_line.r_squared
                mae = subject_data.width_line.mean_abs_error
            if block_num == 2:
                actual = subject_data.width_width.actual
                perceived = subject_data.width_width.perceived
                intercept = subject_data.width_width.intercept
                slope = subject_data.width_width.slope
                r_squared = subject_data.width_width.r_squared
                mae = subject_data.width_width.mean_abs_error

            text = ["R$^2$", "Error"]
            label1 = f"{text[0]:8s} {r_squared:3.2f}\n{text[1]:6s}{mae:3.1f}"
            figure_utils.plot_data_scatter(ax, actual, perceived, colors[sub_num])
            figure_utils.plot_regression_line(
                ax, intercept, slope, colors[sub_num], x1, x2, label1=label1
            )

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
            y_var = 0.8955
            y_err = 0.815
            # ax.text(0.1, y_var, 'R$^2$', fontsize=8, transform=ax.transAxes, zorder=10)
            # ax.text(0.1, y_err, 'Error', fontsize=8, transform=ax.transAxes, zorder=10)

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

            if block_num == 2:
                ax.tick_params(axis="x", which="both", bottom=True, labelbottom=True)
                ax.spines["bottom"].set_visible(True)
                plt.xlabel("Actual width (cm)", fontsize=8)

    # ------------------------------------------------------------------------------------------------------------------
    # plot group regression lines in the right subplot column
    # ------------------------------------------------------------------------------------------------------------------
    subplots = [4, 8, 12]
    for subplot in subplots:
        plt.subplot(subplot_rows, subplot_cols, subplot)
        plt.plot(x_lims, x_lims, "k--", linewidth=1)

    for subject in study_data:
        for row in range(3):
            plt.subplot(subplot_rows, subplot_cols, subplots[row])
            line_color = "darkgrey"
            line_width = 0.5
            order = 5
            alpha = 0.7
            ax = plt.gca()
            if row == 0:
                intercept = subject.line_width.intercept
                slope = subject.line_width.slope
            if row == 1:
                intercept = subject.width_line.intercept
                slope = subject.width_line.slope
            if row == 2:
                intercept = subject.width_width.intercept
                slope = subject.width_width.slope

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
                8,
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

            if row == 2:
                plt.gca().spines["bottom"].set_visible(True)
                plt.gca().tick_params(
                    axis="x", which="both", bottom=True, labelbottom=True
                )
                plt.xlabel("Actual width (cm)", fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 1)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    plt.title(example_subject_labels[0], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 2)
    plt.title(example_subject_labels[1], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 3)
    plt.title(example_subject_labels[2], loc="center", size=8)
    plt.subplot(subplot_rows, subplot_cols, 4)
    plt.title(example_subject_labels[3], loc="center", size=8)

    plt.subplot(subplot_rows, subplot_cols, 1)
    plt.text(-5, 7, "vision-\nto-grasp", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 5)
    plt.text(-5, 7, "grasp-\nto-vision", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.subplot(subplot_rows, subplot_cols, 9)
    plt.text(-5, 7, "grasp-\nto-grasp", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.tight_layout()
    plt.savefig(save_path, dpi=300)
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
