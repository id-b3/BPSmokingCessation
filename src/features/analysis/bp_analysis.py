#!/usr/bin/env python3

from pathlib import Path
import argparse
import random

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
import statsmodels.api as sm
from scipy.stats import f_oneway, ttest_ind


def set_figure_style():
    fnt_s = 14
    fnt_m = 20
    plt.rc('font', size=fnt_s)
    plt.rc('axes', titlesize=fnt_m)
    plt.rc('axes', labelweight="bold")
    plt.rc('axes', labelsize=fnt_s)


def calculate_stats(df_desc: pd.DataFrame, param: str) -> dict:
    """
    This function takes a DataFrame `df_desc` and a column name `param`,
    then calculates and returns the following
    descriptive statistics as a dictionary:
    1. Mean
    2. Standard Deviation (SD)
    3. 95% Confidence Interval (CI)
    4. 95% Range

    Args:
        df_desc (pd.DataFrame): The input DataFrame containing the data.
        param (str):            The name of the column for which to calculate
                                the descriptive statistics.

    Returns:
        dict: A dictionary containing the calculated descriptive statistics.
    """

    # Calc Mean and SD
    mean = df_desc[param].mean()
    sd = df_desc[param].std()
    # Calc 95% CI
    n = len(df_desc[param])
    se = sd / np.sqrt(n)
    ci = 1.96 * se
    ci_low = mean - ci
    ci_high = mean + ci
    # Calc 95% range
    range_low = df_desc[param].quantile(0.025)
    range_high = df_desc[param].quantile(0.975)

    result = {
        "Mean": round(mean, 3),
        "SD": round(sd, 3),
        "95% CI": f"[{round(ci_low, 3)}, {round(ci_high, 3)}]",
        "95% Range": f"[{round(range_low, 3)}-{round(range_high, 3)}]"
    }

    return result


def analyse(df: pd.DataFrame, param_list: list, outpath: Path):

    out_scatter = outpath / "scatterplots"
    out_dist = outpath / "distplots"
    out_box = outpath / "boxplots"
    out_mlr = outpath / "mlr"
    out_lr = outpath / "lr"
    outpath.mkdir(exist_ok=True, parents=True)
    out_scatter.mkdir(exist_ok=True, parents=True)
    out_dist.mkdir(exist_ok=True, parents=True)
    out_box.mkdir(exist_ok=True, parents=True)
    (out_mlr / "text").mkdir(exist_ok=True, parents=True)
    (out_mlr / "csv").mkdir(exist_ok=True, parents=True)
    (out_lr / "text").mkdir(exist_ok=True, parents=True)
    (out_lr / "csv").mkdir(exist_ok=True, parents=True)

    df[["Gender", "Age", "Height", "Weight", "Total Lung Volume"
        ]].describe().to_csv(f"{str(outpath)}/demographics.csv")

    df_male = df[df.Gender == 'Male']
    df_male = df_male.sort_values('Age Category')
    df_female = df[df.Gender == 'Female']
    df_female = df_female.sort_values('Age Category')

    sns.regplot(x=df["Height"], y=df["Total Lung Volume"])
    plt.savefig(f"{str(out_scatter)}/length_at_scan_tlv.jpg")
    plt.close()

    sns.regplot(x=df["Weight"], y=df["Age"])
    plt.savefig(f"{str(out_scatter)}/weight_at_scan_age.jpg")
    plt.close()

    dict_anovas = {}
    dict_ttest = {}
    dict_desc = {"Male": {}, "Female": {}}

    for param in tqdm(param_list):
        # Descriptive stats and ranges
        dict_desc["Male"][param] = calculate_stats(df_male, param)
        dict_desc["Female"][param] = calculate_stats(df_female, param)

        # Distribution plots for gender
        sns.displot(df, x=param, hue="Gender", kind="kde")
        plt.tight_layout()
        plt.savefig(f"{str(out_dist)}/gender_{param}.jpg")
        plt.close()

        # Distribution plots for age
        sns.displot(df, x=param, hue="Age Category", kind="kde")
        plt.savefig(f"{str(out_dist)}/age_{param}.jpg")
        plt.close()

        # Age comparison graphs
        fig = sns.boxplot(data=df, x="Age Category", y=param, hue="Gender")
        plt.savefig(f"{str(out_box)}/age_{param}.jpg")
        plt.close()

        # Gender comparison graphs
        fig = sns.boxplot(data=df, x="Gender", y=param)
        fig.figure.savefig(f"{str(out_box)}/gender_{param}.jpg")
        plt.close()

        # Multivariate Regression Analysis using Ordinary Least Squares
        X = df[["MALE", "Age", "Weight", "Total Lung Volume"]]
        X = sm.add_constant(X)
        y = df[param]
        model = sm.OLS(y, X).fit()
        with open(f"{str(out_mlr)}/text/{param}.txt", "w") as fh:
            fh.write(model.summary().as_text())
        with open(f"{str(out_mlr)}/csv/{param}.csv", "w") as fh:
            fh.write(model.summary().as_csv())

        # Simple Linear Regression
        for x in ["MALE", "FEMALE", "Age", "Weight", "Total Lung Volume"]:
            model = sm.OLS(y, df[x]).fit()
            with open(f"{str(out_lr)}/text/{x}_{param}.txt", "w") as fh:
                fh.write(model.summary().as_text())
            with open(f"{str(out_lr)}/csv/{x}_{param}.csv", "w") as fh:
                fh.write(model.summary().as_csv())
            sns.regplot(x=df[x], y=y)
            plt.savefig(f"{str(out_scatter)}/{x}_{param}.jpg")
            plt.close()

        # T-Test by gender
        t_stat, p_val = ttest_ind(df_male[param], df_female[param])
        dict_ttest[f"{param}"] = round(p_val, 4)

        # ANOVA for age
        male_anova = f_oneway(
            *[s for idx, s in df_male.groupby("Age Category")[param]])
        female_anova = f_oneway(
            *[s for idx, s in df_female.groupby("Age Category")[param]])

        dict_anovas[f"male_{param}"] = male_anova
        dict_anovas[f"female_{param}"] = female_anova

    pd.DataFrame.from_dict(dict_anovas).to_csv(f"{str(outpath)}/anova.csv")
    pd.DataFrame.from_dict({
        't-test': dict_ttest
    }, orient='columns').to_csv(f"{str(outpath)}/ttest.csv")
    desc_df = pd.concat({k: pd.DataFrame(v).T
                         for k, v in dict_desc.items()},
                        axis=0)
    desc_df = desc_df.round(2)
    desc_df.to_csv(f"{str(outpath)}/descriptive_stats.csv")


def main(args):

    set_figure_style()
    outpath = Path(args.out_path)

    df = pd.read_csv(args.in_file)
    df = df[(df.weight_at_scan > 20) & (df.bp_tcount > 100) &
            (df.age_at_scan > 0) & (df.age_at_scan < 100) &
            (df.length_at_scan > 100) & (~df.bp_seg_error) &
            (df.never_smoker.notna()) & (df.GOLD_stage == '0') &
            (df.copd_diagnosis != True) & (df.asthma_diagnosis != True)]
    df["wap_avg"] = df[["bp_wap_3", "bp_wap_4", "bp_wap_5"]].mean(axis=1)
    df["wt_avg"] = df[["bp_wt_3", "bp_wt_4", "bp_wt_5"]].mean(axis=1)
    df["la_avg"] = df[["bp_la_3", "bp_la_4", "bp_la_5"]].mean(axis=1)

    one_hot = pd.get_dummies(df.gender)
    df = df.join(one_hot)

    param_label = {
        "gender": "Gender",
        "age_at_scan": "Age",
        "length_at_scan": "Height",
        "weight_at_scan": "Weight",
        "age_10yr": "Age Category",
        "bp_pi10": "Pi10",
        "wt_avg": "Wall Thickness",
        "la_avg": "Luminal Area",
        "wap_avg": "Wall Area Percent",
        "bp_tcount": "Total Airway Count",
        "bp_airvol": "Total Airway Volume",
        "bp_tlv": "Total Lung Volume"
    }
    df.rename(columns=param_label, inplace=True)
    df["Gender"] = df.apply(lambda row: row["Gender"].capitalize(), axis=1)

    analysis_params = [
        "Pi10", "Wall Thickness", "Luminal Area", "Wall Area Percent",
        "Total Airway Count", "Total Airway Volume"
    ]

    df_groups = {
        "all": df,
        "never-smokers": df[df.never_smoker],
        "ex-smokers": df[df.ex_smoker],
        "current-smoker": df[df.current_smoker]
    }
    for group, data in df_groups.items():
        group_outpath = outpath / group
        analyse(data, analysis_params, group_outpath)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input summary file.")
    parser.add_argument("out_path", type=str, help="Output directory path.")
    parser.add_argument("-s",
                        "--seed",
                        type=int,
                        default=random.randint(0, 10000),
                        help="Sample selection seed")
    args = parser.parse_args()
    main(args)
