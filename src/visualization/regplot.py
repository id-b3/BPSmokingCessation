#!/usr/bin/env python3

import csv
import argparse
from pathlib import Path

import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import statsmodels.formula.api as smf
import scipy.stats as stats


def main(args):
    df = pd.read_csv(args.in_db, low_memory=False)
    if args.healthy:
        df = df[(df.GOLD_stage == "0")]
        df = df[(df.copd_diagnosis == False)
                & (df.asthma_diagnosis == False)
                & (df.cancer_type != "LONGKANKER") &
                (df.cancer_type != "BORST LONG")]
    df.columns = df.columns.str.replace('bp_', '').str.replace(
        '_avg', '').str.replace('_', ' ').str.title()

    bps = args.param_list.replace('bp_', '').replace('_avg', '').replace(
        '_', ' ').title().split(',')

    df = df[df["Age At Scan"] <= 85]

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
    df = df.rename(columns={'Age At Scan': 'Age'})

    sns.set_theme(style="whitegrid")
    fit_tests = []

    # Normalisation
    def min_max_scale(df, param):
        df[param] = (df[param] - df[param].min()) / (df[param].max() - df[param].min())
        return df

    df = min_max_scale(df, "Age")

    for param in bps:
        df = min_max_scale(df, param)
        for status in ["Never Smoker", "Ex Smoker", "Current Smoker"]:
            # fit linear regression model
            model_linear = smf.ols(f'{param} ~ Age', data=df[df[status] == True]).fit()
            sse_linear = model_linear.ssr

            # fit polynomial regression model
            model_poly = smf.ols(f'{param} ~ Age + I(Age**2)', data=df[df[status] == True]).fit()
            sse_poly = model_poly.ssr

            # perform F-test
            n = len(df)
            k_linear = 2
            k_poly = 3
            alpha = 0.00238
            f_stat = ((sse_linear - sse_poly) / (k_poly - k_linear)) / \
                (sse_poly / (n - k_poly))
            f_crit = stats.f.ppf(1 - alpha, k_poly - k_linear, n - k_poly)

            f_result = [param, status, sse_linear, sse_poly, f_stat, f_crit]

            if f_stat > f_crit:
                print(f'Polynomial model is a better fit for {param} for {status}')
                order = 1
                f_result.append("poly")
            else:
                print(f'Linear model is sufficient for {param} for {status}')
                order = 1
                f_result.append("linear")
            fit_tests.append(f_result)

        fig = sns.lmplot(data=df,
                         x="Age",
                         y=param,
                         hue="Smoking Status",
                         order=order,
                         truncate=False,
                         scatter=False)
        sns.despine(left=True)
        fig.fig.savefig(f"{str(out_path / param)}.png", dpi=300)
        plt.close()

        with open(f"{str(out_path)}/regression_fit_comparisons.csv",
                  mode="w",
                  newline='') as f:
            writer = csv.writer(f, delimiter=',')
            writer.writerow([
                "parameter", "smoking_group", "sse_linear", "sse_poly", "f_stat", "f_crit", "better model"
            ])
            writer.writerows(fit_tests)


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
