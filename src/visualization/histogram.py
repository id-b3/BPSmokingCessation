#!/usr/bin/env python

import sys
import logging
from pathlib import Path

import seaborn as sns
import pandas as pd

output_path = Path("./reports/figures/histograms/")


def main():
    logger = logging.getLogger(__name__)
    logger.info('Reading data from stdin...')

    df = pd.read_csv(sys.stdin)
    col_name = df.columns[0]
    logger.info(f'Plotting histplot for {col_name}')

    histplot = sns.displot(df)
    histplot.figure.savefig(str(output_path / f"{col_name}.jpg"))


if __name__ == "__main__":
    log_fmt = '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    logging.basicConfig(level=logging.INFO, format=log_fmt)
    main()
