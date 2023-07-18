#!/usr/bin/env python3
import argparse
import logging
import logging.config
import pandas as pd
from pathlib import Path

from data.util.dataframe import get_group
from features.descriptive import demographics, flowchart
from features.comparative import cessation
from models.linear import univariate, multivariate
from visualization import violin, regression

runs = [
    "descriptive", "comparative", "regression", "clustering", "visualisation"
]
demo_params = [
    "age",
    "height",
    "weight",
    "bp_tlv",
    "pack_years",
    "fev1",
    "fev1_pp",
    "fvc",
    "fev1_fvc",
    "bp_pi10",
    "bp_wap_avg",
    "bp_la_avg",
    "bp_wt_avg",
    "bp_afd",
    "bp_tcount",
    "bp_airvol",
]
# Whether to scale all parameters to [0, 1] before plotting/regression
min_max_params = False

src_dir = Path(__file__).resolve().parent
logging.config.fileConfig(src_dir / "logging.conf")
logger = logging.getLogger("BronchialParameters")


def main(args):
    if args.debug:
        logger.setLevel(logging.DEBUG)

    data_all = pd.read_csv(args.in_file, low_memory=False)
    # Filter the dataset by pack years.
    data_all = data_all[data_all.pack_years >= args.pack_years]
    bps = args.param_list.split(",")
    main_out_dir = Path(args.out_directory)

    # Select group to analyse
    if args.health_stat == "healthy":
        data = get_group(data_all, "healthy")
        main_out_dir = main_out_dir / "healthy"
    elif args.health_stat == "unhealthy":
        data = get_group(data_all, "unhealthy")
        main_out_dir = main_out_dir / "unhealthy"
    elif args.health_stat == "all":
        data = get_group(data_all, "all")
        data = data[data["asthma_diagnosis"] == False]
        main_out_dir = main_out_dir / "all"
    else:
        raise ValueError("Invalid health status: " + args.heath_stat)

    run_funcs = {
        runs[0]:
        lambda: (
            demographics.calc_demographics(data.copy(deep=True), demo_params,
                                           out_path, "health_status"),
            flowchart.make_chart(data_all.copy(deep=True), out_path),
        ),
        runs[1]:
        lambda: (cessation.analyse(data.copy(deep=True), bps, out_path), ),
        runs[2]:
        lambda: (
            univariate.fit_analyse(data.copy(deep=True), bps, "fev1", out_path,
                                   min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "fvc", out_path,
                                   min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "fev1_fvc",
                                   out_path, min_max_params),
            univariate.fit_analyse(data.copy(deep=True), bps, "fev1_pp",
                                   out_path, min_max_params),
            univariate.fit_analyse(
                data.copy(deep=True),
                bps,
                "smoking_cessation_duration",
                out_path,
                min_max_params,
            ),
            multivariate.fit_analyse(data.copy(deep=True), bps, out_path,
                                     min_max_params),
        ),
        runs[3]:
        lambda: (),
        runs[4]:
        lambda: (
            violin.make_plots(data.copy(deep=True), bps, out_path),
            regression.make_plots(data.copy(deep=True), bps, out_path,
                                  min_max_params),
        ),
    }

    # Run the analysis based on the desired run
    for run in args.to_run:
        logger.info(f"Running {run} analysis...")
        out_path = main_out_dir / run
        out_path.mkdir(parents=True, exist_ok=True)
        run_funcs[run]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser(
        description="Analyse Bronchial Parameters.")
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument("out_directory",
                        type=str,
                        help="Output report destination.")
    parser.add_argument(
        "--param_list",
        type=str,
        default="bp_pi10,bp_wt_avg,bp_la_avg,bp_wap_avg",
        help="Comma separated list of params to process.",
    )
    parser.add_argument(
        "--to_run",
        default=["descriptive"],
        nargs="+",
        choices=runs,
        help="Runs to execute. Default: descriptive.",
    )
    parser.add_argument(
        "--health_stat",
        default="healthy",
        choices=["healthy", "unhealthy", "all"],
        help="Health status.",
    )
    parser.add_argument("--pack_years",
                        type=float,
                        default=10.0,
                        help="Pack years.")
    parser.add_argument("--debug", action="store_true", help="Debug mode.")
    args = parser.parse_args()
    main(args)
