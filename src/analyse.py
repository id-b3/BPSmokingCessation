#!/usr/bin/env python3
import argparse
import logging
import logging.config
import pandas as pd
from pathlib import Path

from data.util.dataframe import get_healthy, normalise_bps
from features.descriptive import demographics, flowchart
from features.comparative import smoking
from models.linear import univariate, multivariate
from visualization import violin, regression, percentile

runs = [
    "descriptive", "comparative", "regression", "clustering", "visualisation"
]
group_opts = ["age_10yr", "smoking_status"]
demo_params = [
    'age', 'height', 'weight', 'bp_tlv', 'pack_years',
    'fev1', 'fev1_pp', 'fvc', 'fev1_fvc', 'bp_pi10', 'bp_wap_avg', 'bp_la_avg',
    'bp_wt_avg', 'bp_afd', 'bp_tcount', 'bp_airvol'
]
# Whether to scale all parameters to [0, 1] before plotting/regression
min_max_params = False

src_dir = Path(__file__).resolve().parent
logging.config.fileConfig(src_dir / "logging.conf")
logger = logging.getLogger("BronchialParameters")


def main(args):
    data_all = pd.read_csv(args.in_file, low_memory=False)
    bps = args.param_list.split(",")
    main_out_dir = Path(args.out_directory)

    # Only use healthy participants if specified
    if args.healthy:
        data = get_healthy(data_all)
        main_out_dir = main_out_dir / "healthy"
    else:
        data = data_all.copy()
        main_out_dir = main_out_dir / "all"

    main_out_dir = main_out_dir / args.group_by

    # Normalise parameters if specified (height is default)
    if args.normalised:
        data = normalise_bps(data, bps)
        main_out_dir = main_out_dir / "normalised"
    else:
        main_out_dir = main_out_dir / "not-normalised"


    run_funcs = {
        runs[0]:
        lambda: (
            demographics.calc_demographics(data.copy(deep=True), demo_params, out_path,
                                           args.group_by),
            flowchart.make_chart(data_all.copy(deep=True), out_path),
        ),
        runs[1]:
        lambda: (smoking.compare(data.copy(deep=True), bps, out_path)),
        runs[2]:
        lambda: (
            univariate.fit_analyse(data.copy(deep=True), bps, "height",
                                   out_path, min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "age",
                                   out_path, min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "weight",
                                   out_path, min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "bmi", out_path, min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "pack_years",
                                   out_path, min_max_params),
            multivariate.fit_analyse(data.copy(deep=True), bps, out_path,
                                     min_max_params),
        ),
        runs[3]:
        lambda: (),
        runs[4]:
        lambda: (
            percentile.make_plots(data.copy(deep=True), bps, out_path),
            violin.make_plots(data.copy(deep=True), bps, out_path),
            regression.make_plots(data.copy(deep=True), bps, out_path, min_max_params),
        ),
    }

    # Run the analysis based on the desired run
    for run in args.to_run:
        logger.info(f"Running {run} analysis...")
        out_path = main_out_dir / run
        out_path.mkdir(parents=True, exist_ok=True)
        run_funcs[run]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Analyse Bronchial Parameters.")
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument("param_list",
                        type=str,
                        help="Comma separated list of params to process.")
    parser.add_argument("out_directory",
                        type=str,
                        help="Output report destination.")
    parser.add_argument(
        "--to_run",
        default=["descriptive"],
        nargs="+",
        choices=runs,
        help="Runs to execute. Default: descriptive.",
    )
    parser.add_argument(
        "--group_by",
        default="smoking_status",
        choices=group_opts,
        help="Split data by. Default: smoking_status.",
    )
    parser.add_argument("--healthy", action="store_true", help="Healthy only")
    parser.add_argument("--normalised",
                        action="store_true",
                        help="Normalise parameters")
    args = parser.parse_args()
    main(args)
