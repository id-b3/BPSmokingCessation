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

# Create separate models for male and female groups
for gender in ['Male', 'Female']:
    gender_data = data[data['gender'] == gender]

    # Perform multivariate linear regression for each dependent variable
    params = args.params.split(',')
    for param in params:
        # Extract independent variables
        independent_vars = [
            'age_at_scan', 'weight_at_scan', 'pack_year_categories',
            'never_smoker', 'ex_smoker', 'current_smoker', 'length_at_scan'
        ]

        for var in independent_vars:
            if gender_data[var].dtype == int or gender_data[var].dtype == float:
                gender_data[var] = (gender_data[var] - gender_data[var].min()
                                    ) / (gender_data[var].max() -
                                         gender_data[var].min())

        # Create formula for the model
        formula = param + ' ~ ' + ' + '.join(independent_vars)

        # Fit the model and print the results
        model = sm.formula.ols(formula=formula, data=gender_data).fit()
        print(model.summary())

        # Save the results to a text file
        output_file = args.output_dir + '/' + gender + '_' + param + '_report.txt'
        with open(output_file, 'w') as f:
            f.write(str(model.summary()))

    # Compute overall summary performance of each model per group
    output_file = args.output_dir + '/' + gender + '_summary_report.txt'
    with open(output_file, 'w') as f:
        f.write('Summary report for ' + gender + '\n\n')
        for param in params:
            # Extract independent variables
            independent_vars = [
                'age_at_scan', 'weight_at_scan', 'pack_years',
                'smoking_status', 'bp_tlv'
            ]

            # Create formula for the model
            formula = param + ' ~ ' + ' + '.join(independent_vars)

            # Fit the model and extract relevant summary statistics
            model = sm.formula.ols(formula=formula, data=gender_data).fit()
            r_squared = round(model.rsquared, 3)
            adj_r_squared = round(model.rsquared_adj, 3)
            f_statistic = round(model.fvalue, 3)
            p_value = round(model.f_pvalue, 3)

            # Write summary statistics to file
            f.write(param + '\n')
            f.write('R-squared: ' + str(r_squared) + '\n')
            f.write('Adjusted R-squared: ' + str(adj_r_squared) + '\n')
            f.write('F-statistic: ' + str(f_statistic) + '\n')
            f.write('P-value: ' + str(p_value) + '\n\n')
