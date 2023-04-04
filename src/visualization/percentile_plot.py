#!/usr/bin/env python3

import argparse
from pathlib import Path

import pandas as pd
import numpy as np
import seaborn as sns
import matplotlib.pyplot as plt


def main(args):
    df = pd.read_csv(args.in_db)
    if args.healthy:
        df = df[(df.GOLD_stage == "0")]
        df = df[(df.copd_diagnosis == False)
                & (df.asthma_diagnosis == False)
                & (df.cancer_type != "LONGKANKER") &
                (df.cancer_type != "BORST LONG")]

    # Create age categories
    age_label_2 = [
        40, 42, 44, 46, 48, 50, 52, 54, 56, 58, 60, 62, 64, 66, 68, 70, 72, 74,
        76, 78, 80, 82
    ]
    age_cut_2 = np.linspace(40, 88, 22)
    age_cut_2 = np.append(age_cut_2, 100)

    df['age_2yr'] = pd.cut(df['age_at_scan'],
                           bins=age_cut_2,
                           labels=age_label_2,
                           right=False)

    df.columns = df.columns.str.replace('_', ' ').str.title()

    bps = args.param_list.replace('_', ' ').title().split(',')

    out_path = Path(args.out_dir)
    out_path.mkdir(parents=True, exist_ok=True)

    def _get_smoking_status(row):
        if row["Current Smoker"] is True:
            return "Current Smoker"
        if row["Ex Smoker"] is True:
            return "Ex Smoker"
        if row["Never Smoker"] is True:
            return "Never Smoker"
        else:
            return None

    df["Smoking Status"] = df.apply(_get_smoking_status, axis=1)

    sns.set_theme(style="whitegrid")

    df["Age 5Yr"] = df["Age 5Yr"].replace({
        '40-45': 40,
        '45-50': 45,
        '50-55': 50,
        '55-60': 55,
        '60-65': 60,
        '65-70': 65,
        '70-75': 70,
        '75-80': 75,
        '80-85': 80,
        '85+': 85
    })

    for param in bps:
        fig, axs = plt.subplots(ncols=3, nrows=2)
        for g_idx, gender in enumerate(["MALE", "FEMALE"]):
            for sm_idx, sm_stat in enumerate(["Never Smoker", "Ex Smoker", "Current Smoker"]):
                percentiles = df[(df["Smoking Status"] == sm_stat)
                                 & (df["Gender"] == gender)].groupby(
                                     "Age 2Yr")[param].quantile(
                                         [0.1, 0.3, 0.5, 0.7,
                                          0.9]).reset_index()
                percentiles = percentiles.rename(
                    columns={"level_1": "Percentile"})
                percentiles.Percentile = percentiles["Percentile"].apply(
                    lambda x: f"{x * 100:.0f}%")

                sns.lmplot(data=percentiles,
                           ax=axs[g_idx][sm_idx],
                           x="Age 2Yr",
                           y=param,
                           hue="Percentile",
                           scatter=False,
                           truncate=False,
                           palette=sns.color_palette(
                               ["red", "orange", "green", "orange", "red"]),
                           ci=None,
                           robust=True,
                           line_kws={"alpha": 0.5})

                # Additional customization of the x-axis
                plt.xlabel("Age")
                plt.ylabel(param.replace("Bp ", ""))
                plt.title(f"{gender.title()} {sm_stat}")
                plt.tight_layout()

                fig.savefig(
                    f"{str(out_path / param)} {gender} {sm_stat}.png", dpi=300)
                plt.close()


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_db", type=str, help="Input dfbase csv")
    parser.add_argument("out_dir",
                        type=str,
                        help="Output folder for violin plots.")
    parser.add_argument("param_list",
                        type=str,
                        help="Comma separated list of params to process.")
    parser.add_argument("--healthy",
                        action="store_true",
                        help="Only analyse healthy")
    args = parser.parse_args()
    main(args)
