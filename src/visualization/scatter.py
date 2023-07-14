#!/usr/bin/env python3

import seaborn as sns
import matplotlib.pyplot as plt

from .prettifiers import prettify_axes


def make_plots(data, params, out_path):

    if len(params) != 2:
        raise ValueError("params must be a list of length 2")

    data["pack_years"] = data["pack_years"].astype(float)

    data = data[data.pack_years >= 1]

    out_path = out_path / "scatter"
    out_path.mkdir(parents=True, exist_ok=True)

    sns.set_theme(style="whitegrid")
    fig = sns.jointplot(
        data=data,
        x=params[0],
        y=params[1],
        kind="reg",
        scatter_kws={"alpha": 0.1},
        marginal_kws={"binwidth": 2},
    )
    fig.ax_joint.set_xlim(0, None)
    fig.ax_joint.set_ylim(0, 60)
    # fig.plot_marginals(sns.histplot, kde=True, alpha=0.5, binwidth=2)
    sns.despine(left=True)
    # prettify_axes(fig)
    fig.savefig(f"{str(out_path)}/scatter.png", dpi=300)
    plt.close()
