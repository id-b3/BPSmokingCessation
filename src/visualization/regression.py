#!/usr/bin/env python3

from pathlib import Path
import logging
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import scipy.stats as stats
from tqdm import tqdm

from data.util.dataframe import min_max_scale
from .prettifiers import prettify_axes

logger = logging.getLogger("BronchialParameters")
debug = (logger.level == logging.DEBUG)

def make_plots(data: pd.DataFrame,
               bps: list,
               out_path: Path,
               min_max_params: bool = False):
    """
    Creates scatter plots with linear regression fits to visualize the relationship between bronchial parameters (bp) and
    various demographic and anthropometric factors such as age, length, weight, and bmi. The plots are saved in a given
    output directory.

    Args:
        data (pd.DataFrame): A pandas dataframe with columns for age, height, weight, bmi, bp,
        smoking_status, and sex.
        bps (list): A list of strings containing the names of the bronchial parameters columns to be plotted.
        out_path (Path): A Path object pointing to the directory where the output plots will be saved.

    Returns:
        None

    Raises:
        No exceptions are explicitly raised within this function.

    """

    sns.set_theme(style="whitegrid")
    out_path = out_path / "regression"
    out_path.mkdir(parents=True, exist_ok=True)

    if min_max_params:
        data = min_max_scale(data, ["age", "height", "weight", "bmi"] + bps)

    for param in tqdm(bps):

        for var in ["age", "height", "weight", "fev1_fvc", "fev1_pp", "smoking_cessation_duration"]:
            data_reg = data[[var, param, "smoking_status", "sex"]].dropna()
            r, p = stats.pearsonr(data_reg[var], data_reg[param])

            fig = sns.lmplot(
                data=data_reg,
                x=var,
                y=param,
                hue="sex",
                truncate=False,
                scatter=debug,
                scatter_kws={"alpha": 0.3},
            )
            fig.set(ylim = (data_reg[param].quantile(0.1), data_reg[param].quantile(0.9)))
            logger.debug("Pearson for {} and {}: {}".format(var, param, r))
            sns.despine(left=True)
            if min_max_params:
                fig.set(ylim=(0, 1))
            prettify_axes(fig)
            fig.fig.savefig(f"{str(out_path / param)}_{var}_regression.png",
                            dpi=300)
            plt.close()
