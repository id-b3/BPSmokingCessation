#!/usr/bin/env python3
import argparse
import pandas as pd
from pathlib import Path

from data.util.subgroup import get_healthy, normalise_bps
from features.descriptive import demographics, flowchart

runs = [
    "descriptive", "comparative", "regressive", "modelling", "visualisation"
]


def main(args):
    data_all = pd.read_csv(args.in_file, low_memory=False)
    bps = args.param_list.split(',')
    main_out_dir = Path(args.out_directory)

    # Only use healthy participants if specified
    if args.healthy:
        data = get_healthy(data_all)
        main_out_dir = main_out_dir / "healthy"
    else:
        data = data_all.copy()
        main_out_dir = main_out_dir / "all"

    # Normalise parameters if specified (height is default)
    if args.normalised:
        data = normalise_bps(data, bps)
        main_out_dir = main_out_dir / "normalised"
    else:
        main_out_dir = main_out_dir / "not-normalised"

    # Run the analysis based on the desired run
    for run in runs:
        if args.to_run == run or args.to_run == "all":
            out_path = main_out_dir / run
            out_path.mkdir(parents=True, exist_ok=True)
            if run == "descriptive":
                demographics.calc_demographics(data, bps, out_path)
                flowchart.calc_inclusion_chart(data, out_path)
            elif run == "comparative":
                pass
            elif run == "regressive":
                pass
            elif run == "modelling":
                pass
            elif run == "visualisation":
                pass


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument("param_list",
                        type=str,
                        help="Comma separated list of params to process.")
    parser.add_argument("out_directory",
                        type=str,
                        help="Output report destination.")
    parser.add_argument(
        "to_run",
        type=str,
        help=(
            "Which analysis to run.\n Choose from: "
            "descriptive, comparative, regressive, modelling, visualisation"))
    parser.add_argument("--healthy", action="store_true", help="Healthy only")
    parser.add_argument("--normalised",
                        action="store_true",
                        help="Normalise parameters")
    args = parser.parse_args()
    main(args)
