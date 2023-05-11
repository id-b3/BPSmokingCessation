#!/usr/bin/env python3
import argparse
import pandas as pd
from pathlib import Path

from data.util.subgroup import get_healthy, normalise_bps
from features.descriptive import demographics, flowchart
from features.comparative import compare_sex

runs = ["descriptive", "comparative", "regression", "clustering", "visualisation"]


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

    # Normalise parameters if specified (height is default)
    if args.normalised:
        data = normalise_bps(data, bps)
        main_out_dir = main_out_dir / "normalised"
    else:
        main_out_dir = main_out_dir / "not-normalised"

    run_funcs = {
        runs[0]: lambda: (
            demographics.calc_demographics(data, bps, out_path),
            flowchart.make_chart(data, out_path),
        ),
        runs[1]: lambda: (
            compare_sex.compare(data, bps, out_path)
        ),
        runs[2]: lambda: (),
        runs[3]: lambda: (),
        runs[4]: lambda: (),
    }

    # Run the analysis based on the desired run
    for run in args.to_run:
        print(run)
        out_path = main_out_dir / run
        out_path.mkdir(parents=True, exist_ok=True)
        run_funcs[run]()


if __name__ == "__main__":
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument(
        "param_list", type=str, help="Comma separated list of params to process."
    )
    parser.add_argument("out_directory", type=str, help="Output report destination.")
    parser.add_argument(
        "--to_run",
        default=["descriptive"],
        nargs="+",
        choices=runs,
        help="Runs to execute. Default: descriptive.",
    )
    parser.add_argument("--healthy", action="store_true", help="Healthy only")
    parser.add_argument(
        "--normalised", action="store_true", help="Normalise parameters"
    )
    args = parser.parse_args()
    main(args)
