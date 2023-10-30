from pathlib import Path

import matplotlib.pyplot as plt

import figure_utils


def plot(plot_outcomes):
    """
    plot_outcomes[0] -> intercept
        [0] -> d1d_d1nd outcomes (mean, ci)
        [1] -> d1d_d1nd diff values
        [2] -> d2d1_d2d2 outcomes (mean, ci)
        [3] -> d2d1_d2d2 diff values
        [4] -> d1d_d2d1 outcomes (mean, ci)
        [5] -> d1d_d2d1 diff values
    plot_outcomes[1] -> slope
    plot_outcomes[2] -> r-squared
    plot_outcomes[3] -> mean absolute error
    plot_outcomes[4] -> regression diff
    """
    intercept = 0
    slope = 1
    r_squared = 2
    mae = 3

    d1d_d1nd_outcomes = 0
    d1d_d1nd_diff = 1
    d2d1_d2d2_outcomes = 2
    d2d1_d2d2_diff = 3
    d1d_d2d1_outcomes = 4
    d1d_d2d1_diff = 5

    save_path = figure_utils.create_figure_save_path("Figure_8")
    condition_names = [
        "Different hands\nsame day",
        "Same hand\nsame day",
        "Same hand\n1 week apart",
    ]
    x_ticks = [0.95, 2, 3.05]
    plt.figure(figsize=(3, 6))

    # ------------------------------------------------------------------------------------------------
    # Intercept
    # ------------------------------------------------------------------------------------------------

    plt.subplot(4, 1, intercept + 1)
    jit = 0.002
    alpha = 0.4
    markersize_ = 4
    mfc = "lightgrey"
    plt.plot([-0.5, 4], [0, 0], "-", color="darkgrey", linewidth=1)
    jitter = 0
    for value in plot_outcomes[intercept][d1d_d1nd_diff]:
        plt.plot(
            x_ticks[0] + jitter,
            value,
            markersize=markersize_,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            linestyle="",
            mec="none",
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[intercept][d2d1_d2d2_diff]:
        plt.plot(
            x_ticks[1] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[intercept][d1d_d2d1_diff]:
        plt.plot(
            x_ticks[2] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit

    # --------------------
    # mean [CI]
    # --------------------
    plt.plot(
        x_ticks[0] + (15 * jit),
        plot_outcomes[intercept][d1d_d1nd_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[0] + (15 * jit), x_ticks[0] + (15 * jit)],
        plot_outcomes[intercept][d1d_d1nd_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[1] + (15 * jit),
        plot_outcomes[intercept][d2d1_d2d2_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[1] + (15 * jit), x_ticks[1] + (15 * jit)],
        plot_outcomes[intercept][d2d1_d2d2_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[2] + (15 * jit),
        plot_outcomes[intercept][d1d_d2d1_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[2] + (15 * jit), x_ticks[2] + (15 * jit)],
        plot_outcomes[intercept][d1d_d2d1_outcomes][1],
        "-k",
        linewidth=1,
    )

    # ------------------------------------------------------------------------------------------------
    # Slope
    # ------------------------------------------------------------------------------------------------
    plt.subplot(4, 1, slope + 1)
    plt.plot([-0.5, 4], [0, 0], "-", color="darkgrey", linewidth=1)
    jitter = 0
    for value in plot_outcomes[slope][d1d_d1nd_diff]:
        plt.plot(
            x_ticks[0] + jitter,
            value,
            markersize=markersize_,
            marker="^",
            alpha=alpha,
            linestyle="",
            mec="none",
            mfc=mfc,
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[slope][d2d1_d2d2_diff]:
        plt.plot(
            x_ticks[1] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[slope][d1d_d2d1_diff]:
        plt.plot(
            x_ticks[2] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit

    # --------------------
    # mean [CI]
    # --------------------
    plt.plot(
        x_ticks[0] + (15 * jit),
        plot_outcomes[slope][d1d_d1nd_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[0] + (15 * jit), x_ticks[0] + (15 * jit)],
        plot_outcomes[slope][d1d_d1nd_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[1] + (15 * jit),
        plot_outcomes[slope][d2d1_d2d2_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[1] + (15 * jit), x_ticks[1] + (15 * jit)],
        plot_outcomes[slope][d2d1_d2d2_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[2] + (15 * jit),
        plot_outcomes[slope][d1d_d2d1_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[2] + (15 * jit), x_ticks[2] + (15 * jit)],
        plot_outcomes[slope][d1d_d2d1_outcomes][1],
        "-k",
        linewidth=1,
    )

    # ------------------------------------------------------------------------------------------------
    # R-squared
    # ------------------------------------------------------------------------------------------------
    plt.subplot(4, 1, r_squared + 1)
    plt.plot([-0.5, 4], [0, 0], "-", color="darkgrey", linewidth=1)
    jitter = 0
    for value in plot_outcomes[r_squared][d1d_d1nd_diff]:
        plt.plot(
            x_ticks[0] + jitter,
            value,
            markersize=markersize_,
            marker="^",
            alpha=alpha,
            linestyle="",
            mec="none",
            mfc=mfc,
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[r_squared][d2d1_d2d2_diff]:
        plt.plot(
            x_ticks[1] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[r_squared][d1d_d2d1_diff]:
        plt.plot(
            x_ticks[2] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit

    # --------------------
    # mean [CI]
    # --------------------
    plt.plot(
        x_ticks[0] + (15 * jit),
        plot_outcomes[r_squared][d1d_d1nd_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[0] + (15 * jit), x_ticks[0] + (15 * jit)],
        plot_outcomes[r_squared][d1d_d1nd_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[1] + (15 * jit),
        plot_outcomes[r_squared][d2d1_d2d2_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[1] + (15 * jit), x_ticks[1] + (15 * jit)],
        plot_outcomes[r_squared][d2d1_d2d2_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[2] + (15 * jit),
        plot_outcomes[r_squared][d1d_d2d1_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[2] + (15 * jit), x_ticks[2] + (15 * jit)],
        plot_outcomes[r_squared][d1d_d2d1_outcomes][1],
        "-k",
        linewidth=1,
    )

    # ------------------------------------------------------------------------------------------------
    # mean absolute error
    # ------------------------------------------------------------------------------------------------
    plt.subplot(4, 1, mae + 1)
    plt.plot([-0.5, 4], [0, 0], "-", color="darkgrey", linewidth=1)
    jitter = 0
    for value in plot_outcomes[mae][d1d_d1nd_diff]:
        plt.plot(
            x_ticks[0] + jitter,
            value,
            markersize=markersize_,
            marker="^",
            alpha=alpha,
            linestyle="",
            mec="none",
            mfc=mfc,
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[mae][d2d1_d2d2_diff]:
        plt.plot(
            x_ticks[1] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit
    jitter = 0
    for value in plot_outcomes[mae][d1d_d2d1_diff]:
        plt.plot(
            x_ticks[2] + jitter,
            value,
            mfc=mfc,
            marker="^",
            alpha=alpha,
            markersize=markersize_,
            linestyle="",
            mec="none",
        )
        jitter += jit

    # --------------------
    # mean [CI]
    # --------------------
    plt.plot(
        x_ticks[0] + (15 * jit),
        plot_outcomes[mae][d1d_d1nd_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[0] + (15 * jit), x_ticks[0] + (15 * jit)],
        plot_outcomes[mae][d1d_d1nd_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[1] + (15 * jit),
        plot_outcomes[mae][d2d1_d2d2_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[1] + (15 * jit), x_ticks[1] + (15 * jit)],
        plot_outcomes[mae][d2d1_d2d2_outcomes][1],
        "-k",
        linewidth=1,
    )

    plt.plot(
        x_ticks[2] + (15 * jit),
        plot_outcomes[mae][d1d_d2d1_outcomes][0],
        "^k",
        markersize=3,
    )
    plt.plot(
        [x_ticks[2] + (15 * jit), x_ticks[2] + (15 * jit)],
        plot_outcomes[mae][d1d_d2d1_outcomes][1],
        "-k",
        linewidth=1,
    )

    # ------------------------------------------------------------------------------------------------
    # Fixing look of plots
    # ------------------------------------------------------------------------------------------------

    plt.subplot(4, 1, 1)
    plt.ylim([-2, 2])
    plt.xlim([x_ticks[0] - (15 * jit), x_ticks[2] + (40 * jit)])
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
    plt.yticks([-2, -1, 0, 1, 2])
    plt.ylabel("Intercept", fontsize=8)
    figure_utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)
    plt.gca().text(-0.2, 2, "A", fontsize=12)

    plt.subplot(4, 1, 2)
    plt.ylim([-0.5, 0.5])
    plt.xlim([x_ticks[0] - (15 * jit), x_ticks[2] + (40 * jit)])
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
    plt.yticks([-0.5, -0.25, 0.0, 0.25, 0.5])
    plt.ylabel("Slope", fontsize=8)
    plt.gca().text(-0.2, 0.6, "B", fontsize=12)
    figure_utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)

    plt.subplot(4, 1, 3)
    plt.ylim([-0.15, 0.1])
    plt.xlim([x_ticks[0] - (15 * jit), x_ticks[2] + (40 * jit)])
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
    plt.yticks([-0.15, -0.1, -0.05, 0.0, 0.05, 0.1])
    plt.ylabel("R$^2$", fontsize=8)
    figure_utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)
    plt.gca().text(-0.2, 0.1, "C", fontsize=12)

    plt.subplot(4, 1, 4)
    plt.ylim([-1.5, 1.5])
    plt.xlim([x_ticks[0] - (15 * jit), x_ticks[2] + (40 * jit)])
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
    plt.ylabel("Mean absolute error (cm)", fontsize=8)
    plt.yticks([-1.5, -1.0, -0.5, 0.0, 0.5, 1.0, 1.5])
    figure_utils.draw_ax_spines(ax, True, False, False, False, y_offset=True)
    plt.gca().text(-0.2, 1.5, "D", fontsize=12)

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
    plt.xticks(
        [x_ticks[0] - (25 * jit), x_ticks[1] + (20 * jit), x_ticks[2] + (40 * jit)],
        condition_names,
        fontsize=8,
    )
    plt.subplots_adjust(left=0.325, right=0.85)
    plt.tight_layout()

    for i in range(4):
        plt.subplot(4, 1, i + 1)
        plt.yticks(fontsize=8)
        plt.xticks(fontsize=8)

    plt.savefig(save_path, dpi=300, bbox_inches="tight")
    path_svg = Path(save_path.parts[0], save_path.parts[1], save_path.stem + ".svg")
    plt.savefig(path_svg)
    plt.close()
