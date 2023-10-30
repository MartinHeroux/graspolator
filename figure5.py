from pathlib import Path

import matplotlib.pyplot as plt
import numpy as np

import figure_utils
import outcomes


def plot(plot_outcomes):
    save_path = figure_utils.create_figure_save_path("Figure_5")

    plt.figure(figsize=(3, 3))
    plt.subplot(1, 1, 1)
    plt.scatter(plot_outcomes[0], plot_outcomes[1], color="lightgrey", s=3, alpha=1)
    # plt.xlim([0, 4])
    # plt.ylim([0.6, 1])
    ax = plt.gca()
    plt.ylabel("Grasp-to-vision regression slope", fontsize=8)
    plt.xlabel("Vision-to-grasp regression slope", fontsize=8)
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
    _, intercept, slope = outcomes.regression(plot_outcomes[0], plot_outcomes[1])
    x1 = np.min(plot_outcomes[0])
    x2 = np.max(plot_outcomes[0])
    y1 = (slope * x1) + intercept
    y2 = (slope * x2) + intercept
    plt.plot([x1, x2], [y1, y2], "-k", linewidth=1)
    plt.yticks(
        [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
        [0.4, 0.6, 0.8, 1.0, 1.2, 1.4, 1.6, 1.8, 2.0],
    )
    plt.xlim([0.4, 1.4])
    plt.ylim([0.4, 2.0])

    # Plot outlier
    for i, value in enumerate(plot_outcomes[1]):
        if value > 1.89:
            index = i
            break

    plt.plot(
        plot_outcomes[0][index],
        plot_outcomes[1][index],
        "o",
        markersize=4,
        color="white",
    )

    plt.plot(
        plot_outcomes[0][index],
        plot_outcomes[1][index],
        "x",
        markersize=3,
        color="darkgrey",
    )
    plt.yticks(fontsize=8)
    plt.xticks(fontsize=8)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
