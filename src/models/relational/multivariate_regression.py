#!/usr/bin/env python3

import pandas as pd
import statsmodels.api as sm
import argparse

from src.data.subgroup import get_healthy

# Create argument parser
parser = argparse.ArgumentParser(
    description='Perform multivariate linear regression analysis.')
parser.add_argument('input_csv',
                    type=str,
                    help='Input CSV file containing the dataset.')
parser.add_argument('params',
                    type=str,
                    help='Comma-separated list of dependent variables.')
parser.add_argument('output_dir',
                    type=str,
                    help='Output directory for the reports.')
parser.add_argument('--healthy',
                    action='store_true',
                    help='If set, only includes data from healthy subjects.')
args = parser.parse_args()

# Load data from CSV file
data = pd.read_csv(args.input_csv)

# Filter data by healthy status, if requested
if args.healthy:
    data = get_healthy(data)

data['pack_year_categories'] = data['pack_year_categories'].replace(
    '0', '0 pack-years')
# Perform multivariate linear regression for each dependent variable
params = args.params.split(',')
for param in params:
    # Extract independent variables
    independent_vars = ['gender', 'age_at_scan', 'bmi', 'current_smoker', 'pack_year_categories']

    # Normalising the data
    for var in independent_vars:
        if data[var].dtype == int or data[var].dtype == float:
            data[var] = (data[var] - data[var].min()) / (data[var].max() -
                                                         data[var].min())

    # Create formula for the model
    formula = param + ' ~ ' + ' + '.join(independent_vars)

    # Fit the model and print the results
    model = sm.formula.ols(formula=formula, data=data).fit()
    print(model.summary())

    # Save the results to a text file
    output_file = args.output_dir + '/' + 'normalised_' + param + '_report.txt'
    with open(output_file, 'w') as f:
        f.write(str(model.summary()))
