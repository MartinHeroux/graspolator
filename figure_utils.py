from pathlib import Path
import os
from random import random

import numpy as np


def create_figure_save_path(plot):
    path = Path(f"./plots/figures/")
    if not os.path.exists(path):
        os.makedirs(path)
    savepath = Path(f"./plots/figures/{plot}.png")
    return savepath


def plot_data_scatter(ax, actual, perceived, color):
    length_data = len(perceived)
    jitter_values = [random() / 4 for _ in range(length_data)]
    x_data = (np.array(actual) - 0.1) + np.array(jitter_values)

    # plot scatter plot of stimulus vs perceived widths
    ax.plot(
        x_data,
        perceived,
        "o",
        color=color,
        alpha=0.5,
        markersize=3,
        markeredgecolor=None,
        markeredgewidth=0,
    )


def plot_regression_line(
    ax, intercept, slope, color, x1, x2, alpha=1, width=1, order=10, label1=None
):
    y1 = slope * x1 + intercept
    y2 = slope * x2 + intercept
    if label1:
        ax.plot(
            [x1, x2],
            [y1, y2],
            color=color,
            linewidth=width,
            alpha=alpha,
            zorder=order,
            label=label1,
        )
    else:
        ax.plot(
            [x1, x2], [y1, y2], color=color, linewidth=width, alpha=alpha, zorder=order
        )


def set_ax_parameters(
    ax,
    x_ticks,
    y_ticks,
    x_tick_labels,
    y_tick_labels,
    x_lims,
    y_lims,
    x_label,
    y_label,
    x_fontsize=10,
    gridlines=None,
    y_fontsize=8,
):
    ax.set_xticks(x_ticks)
    ax.set_xticklabels(x_tick_labels, fontsize=x_fontsize)
    ax.set_yticks(y_ticks)
    ax.set_yticklabels(y_tick_labels, fontsize=y_fontsize)
    ax.set_xlim(x_lims)
    ax.set_ylim(y_lims)
    ax.set_xlabel(x_label, fontsize=8)
    ax.set_ylabel(y_label, fontsize=8)
    if gridlines:
        ax.grid(axis="both", linewidth=0.5, color="lightgray")


def draw_ax_spines(ax, left, right, top, bottom, x_offset=False, y_offset=False):
    commands = [left, right, top, bottom]
    spines = ["left", "right", "top", "bottom"]

    for spine, command in zip(spines, commands):
        if command == True:
            ax.spines[spine].set_visible(True)
        else:
            ax.spines[spine].set_visible(False)

    if y_offset == True:
        ax.spines["left"].set_position(("outward", 3))
    if x_offset == True:
        ax.spines["bottom"].set_position(("outward", 8))
