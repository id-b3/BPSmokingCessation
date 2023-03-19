#!/usr/bin/env python3

import argparse
from pathlib import Path

import pandas as pd
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

    for param in bps:
        fig = sns.lmplot(data=df,
                         x="Age At Scan",
                         y=param,
                         hue="Smoking Status",
                         robust=True)
        sns.despine(left=True)
        fig.fig.savefig(f"{str(out_path / param)}.png", dpi=300)
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
