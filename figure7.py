from pathlib import Path

import matplotlib.pyplot as plt
from matplotlib.lines import Line2D

import figure_utils


def plot(study_data, plot_outcomes):
    save_path = figure_utils.create_figure_save_path("Figure_7")
    condition_names = ["dominant", "non-dominant", "  dominant 1", "dominant 2"]
    x_ticks = [0.95, 2, 3, 4.05]
    plt.figure(figsize=(3, 4.5))
    for subject_data in study_data:
        plt.subplot(2, 1, 1)
        y_vals = [
            subject_data.day1_dominant.r_squared,
            subject_data.day1_non_dominant.r_squared,
            subject_data.day2_dominant_1.r_squared,
            subject_data.day2_dominant_2.r_squared,
        ]
        plt.plot(x_ticks, y_vals, linewidth=0.5, color="lightgrey", alpha=0.4)

        plt.subplot(2, 1, 2)
        y_vals = [
            subject_data.day1_dominant.mean_abs_error,
            subject_data.day1_non_dominant.mean_abs_error,
            subject_data.day2_dominant_1.mean_abs_error,
            subject_data.day2_dominant_2.mean_abs_error,
        ]
        plt.plot(x_ticks, y_vals, linewidth=0.5, color="lightgrey", alpha=0.4)

    plt.subplot(2, 1, 1)
    plt.ylim(0.7, 1.0)
    plt.xlim([x_ticks[0], x_ticks[3]])
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
    plt.gca().text(0.1, 1, "A", fontsize=12)

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
    plt.gca().text(0.1, 3, "B", fontsize=12)
    figure_utils.set_ax_parameters(
        ax,
        x_ticks,
        [0, 1, 2, 3],
        condition_names,
        [0, 1, 2, 3],
        [x_ticks[0], x_ticks[3]],
        [0, 3],
        None,
        "Mean absolute error (cm)",
        8,
        False,
        y_fontsize=8,
    )
    for block in range(4):
        if block == 0:
            offset = 0.04
        if block == 2:
            offset = 0
        if block == 1:
            offset = 0
        if block == 3:
            offset = -0.04
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
            x_ticks[block] + offset, plot_outcomes[block + 4][0], "ko", markersize=3
        )
        plt.plot(
            [x_ticks[block] + offset, x_ticks[block] + offset],
            plot_outcomes[block + 4][1],
            "-k",
            linewidth=1,
        )
        plt.yticks(fontsize=8)
        plt.xticks(fontsize=8)
    # plt.subplots_adjust(left=0.25, right=0.9)
    plt.subplot(2, 1, 2)
    plt.text(1.2, -1, "day 1", fontsize=8)
    plt.text(3.3, -1, "day 2", fontsize=8)

    ax2 = plt.axes([0, 0, 1, 1], facecolor=(1, 1, 1, 0))

    line = Line2D([0.12, 0.39], [0.032, 0.032], lw=0.5, color="k")
    ax2.add_line(line)
    line = Line2D([0.65, 0.9], [0.032, 0.032], lw=0.5, color="k")
    ax2.add_line(line)
    figure_utils.draw_ax_spines(
        ax2,
        left=False,
        right=False,
        top=False,
        bottom=False,
        x_offset=True,
        y_offset=True,
    )
    ax2.tick_params(
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
    # plt.subplots_adjust(left=0.3, right=0.9)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
