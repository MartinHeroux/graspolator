from pathlib import Path

import matplotlib.pyplot as plt

import figure_utils


def plot(study_data, plot_outcomes):
    save_path = figure_utils.create_figure_save_path("Figure_3")
    condition_names = ["vision-\nto-grasp", "grasp-\nto-vision", "grasp-\nto-grasp"]
    x_ticks = [0.95, 2, 3.05]
    plt.figure(figsize=(3, 3.5))
    for subject_data in study_data:
        plt.subplot(2, 1, 1)
        y_vals = [
            subject_data.line_width.r_squared,
            subject_data.width_line.r_squared,
            subject_data.width_width.r_squared,
        ]
        plt.plot(x_ticks, y_vals, linewidth=0.5, color="lightgrey", alpha=0.4)

        plt.subplot(2, 1, 2)
        y_vals = [
            subject_data.line_width.mean_abs_error,
            subject_data.width_line.mean_abs_error,
            subject_data.width_width.mean_abs_error,
        ]
        plt.plot(x_ticks, y_vals, linewidth=0.5, color="lightgrey", alpha=0.4)

    plt.subplot(2, 1, 1)
    plt.ylim(0.6, 1.0)
    plt.xlim([x_ticks[0], x_ticks[2]])
    ax = plt.gca()
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

    plt.ylabel("Variability ($R^2$)", fontsize=8)
    figure_utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)
    plt.gca().text(0.2, 1, "A", fontsize=12)

    plt.subplot(2, 1, 2)
    ax = plt.gca()
    ax.tick_params(axis="both", which="both", bottom=True, labelbottom=True)
    figure_utils.draw_ax_spines(
        ax,
        left=True,
        right=False,
        top=False,
        bottom=True,
        x_offset=True,
        y_offset=True,
    )

    plt.gca().text(0.2, 4, "B", fontsize=12)
    figure_utils.set_ax_parameters(
        ax,
        x_ticks,
        [0, 1, 2, 3, 4],
        condition_names,
        [0, 1, 2, 3, 4],
        [x_ticks[0], x_ticks[2]],
        [0, 4],
        None,
        "Mean absolute error (cm)",
        8,
        False,
        y_fontsize=8,
    )
    for block in range(3):
        if block == 0:
            offset = 0.04
        if block == 2:
            offset = -0.04
        if block == 1:
            offset = 0
        plt.subplot(2, 1, 1)
        plt.plot(x_ticks[block] + offset, plot_outcomes[block][0], "ko", markersize=3)
        plt.plot(
            [x_ticks[block] + offset, x_ticks[block] + offset],
            plot_outcomes[block][1],
            "-k",
            linewidth=1,
        )
        plt.yticks(fontsize=8)
        plt.xticks(fontsize=8)

        plt.subplot(2, 1, 2)
        plt.plot(
            x_ticks[block] + offset, plot_outcomes[block + 3][0], "ko", markersize=3
        )
        plt.plot(
            [x_ticks[block] + offset, x_ticks[block] + offset],
            plot_outcomes[block + 3][1],
            "-k",
            linewidth=1,
        )
        plt.yticks(fontsize=8)
        plt.xticks(fontsize=8)

    plt.subplots_adjust(left=0.25, right=0.9)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
