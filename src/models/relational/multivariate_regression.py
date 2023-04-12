#!/usr/bin/env python3

import pandas as pd
import statsmodels.api as sm
import argparse

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
    data = data[(data.GOLD_stage == "0")]
    data = data[(data.copd_diagnosis == False)
                & (data.asthma_diagnosis == False)
                & (data.cancer_type != "LONGKANKER") &
                (data.cancer_type != "BORST LONG")]


def get_smoking_status(row):
    if row["current_smoker"] is True:
        return "current_smoker"
    if row["ex_smoker"] is True:
        return "ex_smoker"
    if row["never_smoker"] is True:
        return "never_smoker"
    else:
        return None


data["smoking_status"] = data.apply(get_smoking_status, axis=1)
data = data.dropna(subset=["smoking_status"])

# Create separate models for male and female groups
for gender in ['Male', 'Female']:
    gender_data = data[data['gender'] == gender]

    # Perform multivariate linear regression for each dependent variable
    params = args.params.split(',')
    for param in params:
        # Extract independent variables
        independent_vars = [
            'age_at_scan', 'weight_at_scan', 'pack_years', 'smoking_status',
            'bp_tlv'
        ]

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
