#!/usr/bin/env python3

from pathlib import Path
import argparse
import random

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

from tqdm import tqdm
import statsmodels.api as sm
from scipy.stats import f_oneway


def set_figure_style():
    fnt_s = 14
    fnt_m = 20
    fnt_l = 26
    plt.rc('font', size=fnt_s)
    plt.rc('axes', titlesize=fnt_m)
    plt.rc('axes', labelweight="bold")
    plt.rc('axes', labelsize=fnt_s)
    # plt.rc('legend', titleweight="bold")
    # plt.rc('figure', titlesize=fnt_l)


def main(args):

    outpath = Path(args.out_path)
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

    df = pd.read_csv(args.in_file)
    df = df[(df.weight_at_scan > 20) & (df.bp_tcount > 100) &
            (df.age_at_scan > 0) & (df.age_at_scan < 100) &
            (df.length_at_scan > 100) & (df.bp_seg_error == False)]
    df["wap_avg"] = df[["bp_wap_3", "bp_wap_4", "bp_wap_5"]].mean(axis=1)
    df["wt_avg"] = df[["bp_wt_3", "bp_wt_4", "bp_wt_5"]].mean(axis=1)
    df["la_avg"] = df[["bp_la_3", "bp_la_4", "bp_la_5"]].mean(axis=1)
    df = df.sample(n=282, random_state=args.seed)
    with open(f"{str(outpath)}/seed_n_gender.txt", "w") as f:
        f.write(f"Sample Seed: {args.seed}\n{df['gender'].value_counts()}")
    df[["gender", "age_at_scan", "length_at_scan", "weight_at_scan",
        "bp_tlv"]].describe().to_csv(f"{str(outpath)}/demographics.csv")

    bins = [0, 55, 65, 75, 100]
    labels = ["45-55", "56-65", "66-75", "76-100"]
    df["age_category"] = pd.cut(df["age_at_scan"], bins=bins, labels=labels)
    one_hot = pd.get_dummies(df.gender)
    df = df.join(one_hot)

    param_label = {
        "gender": "Gender",
        "age_at_scan": "Age",
        "length_at_scan": "Height",
        "weight_at_scan": "Weight",
        "age_category": "Age Category",
        "bp_pi10": "Pi10",
        "wt_avg": "Wall Thickness",
        "la_avg": "Luminal Area",
        "wap_avg": "Wall Area Percent",
        "bp_tcount": "Total Airway Count",
        "bp_airvol": "Total Airway Volume",
        "bp_tlv": "Total Lung Volume"
    }

    analysis_params = [
        "Pi10", "Wall Thickness", "Luminal Area", "Wall Area Percent",
        "Total Airway Count", "Total Airway Volume"
    ]

    df.rename(columns=param_label, inplace=True)

    df["Gender"] = df.apply(lambda row: row["Gender"].capitalize(), axis=1)
    df_male = df[df.Gender == 'Male']
    df_female = df[df.Gender == 'Female']

    set_figure_style()

    sns.regplot(x=df["Height"], y=df["Total Lung Volume"])
    plt.savefig(f"{str(out_scatter)}/length_at_scan_tlv.jpg")
    plt.close()

    sns.regplot(x=df["Weight"], y=df["Age"])
    plt.savefig(f"{str(out_scatter)}/weight_at_scan_age.jpg")
    plt.close()

    list_anovas = {}

    for param in tqdm(analysis_params):
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

        # ANOVA for age
        male_anova = f_oneway(
            *[s for idx, s in df_male.groupby("Age Category")[param]])
        female_anova = f_oneway(
            *[s for idx, s in df_female.groupby("Age Category")[param]])

        list_anovas[f"male_{param}"] = male_anova
        list_anovas[f"female_{param}"] = female_anova

    df_anova = pd.DataFrame.from_dict(list_anovas)
    df_anova.to_csv(f"{str(outpath)}/anova.csv")


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input summary file.")
    parser.add_argument("out_path", type=str, help="Output directory path.")
    parser.add_argument("-s", "--seed", type=int, default=random.randint(0, 10000), help="Sample selection seed")
    args = parser.parse_args()
    main(args)
