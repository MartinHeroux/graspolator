from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import figure_utils
import outcomes


def plot(plot_outcomes):
    save_path = figure_utils.create_figure_save_path("Figure_4")
    condition_names = ["Vision-\nto-grasp", "Grasp-\nto-vision", "Grasp-\nto-grasp"]

    plt.figure(figsize=(3, 4.5))
    plt.subplot(3, 1, 1)
    plt.scatter(plot_outcomes[3], plot_outcomes[0], color="lightgrey", s=3, alpha=1)
    plt.xlim([0, 3.5])
    plt.ylim([0.5, 1])

    plt.subplot(3, 1, 2)
    plt.scatter(plot_outcomes[4], plot_outcomes[1], color="lightgrey", s=3, alpha=1)
    plt.xlim([0, 3.5])
    plt.ylim([0.5, 1])

    plt.subplot(3, 1, 3)
    plt.scatter(plot_outcomes[5], plot_outcomes[2], color="lightgrey", s=3, alpha=1)
    plt.xlim([0, 3.5])
    plt.ylim([0.5, 1])

    plt.subplot(3, 1, 1)
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
    plt.gca().text(-1.4, 1, "A", fontsize=12)

    plt.subplot(3, 1, 2)
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
    plt.gca().text(-1.4, 1, "B", fontsize=12)

    plt.subplot(3, 1, 3)
    ax = plt.gca()
    plt.ylabel("Variability ($R^2$)", fontsize=8)
    plt.xlabel("Mean absolute error (cm)", fontsize=8)
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
    plt.gca().text(-1.4, 1, "C", fontsize=12)
    plt.subplot(3, 1, 1)
    _, intercept, slope = outcomes.regression(plot_outcomes[3], plot_outcomes[0])
    x1 = np.min(plot_outcomes[3])
    x2 = np.max(plot_outcomes[3])
    y1 = (slope * x1) + intercept
    y2 = (slope * x2) + intercept
    plt.plot([x1, x2], [y1, y2], "-k", linewidth=1)
    # plt.text(3, 0.975, 'r=0.22', fontsize=10)

    plt.subplot(3, 1, 2)
    _, intercept, slope = outcomes.regression(plot_outcomes[4], plot_outcomes[1])
    x1 = np.min(plot_outcomes[4])
    x2 = np.max(plot_outcomes[4])
    y1 = (slope * x1) + intercept
    y2 = (slope * x2) + intercept
    plt.plot([x1, x2], [y1, y2], "-k", linewidth=1)
    # plt.text(3, 0.975, 'r=0.09', fontsize=10)

    plt.subplot(3, 1, 3)
    _, intercept, slope = outcomes.regression(plot_outcomes[5], plot_outcomes[2])
    x1 = np.min(plot_outcomes[5])
    x2 = np.max(plot_outcomes[5])
    y1 = (slope * x1) + intercept
    y2 = (slope * x2) + intercept
    plt.plot([x1, x2], [y1, y2], "-k", linewidth=1)
    # plt.text(3, 0.975, 'r=-0.85', fontsize=10)

    plt.subplot(3, 1, 1)
    plt.title("vision-to-grasp", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    plt.subplot(3, 1, 2)
    plt.title("grasp-to-vision", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    plt.subplot(3, 1, 3)
    plt.title("grasp-to-grasp", fontsize=8)
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)
    plt.subplots_adjust(left=0.3, right=0.9)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
