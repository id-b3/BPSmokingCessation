#!/usr/bin/env python3

import argparse
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="Input CSV file name")
parser.add_argument("parameters",
                    help="Comma-separated list of parameter names")
parser.add_argument("output", help="Output CSV file name")
parser.add_argument("--healthy",
                    action="store_true",
                    help="Only include 'never_smoker' group")

# Parse arguments
args = parser.parse_args()

# Read input CSV file
df = pd.read_csv(args.input_csv)

# Filter by smoking status if healthy flag is set
if args.healthy:
    df = df[(df.GOLD_stage == "0")]
    df = df[(df.copd_diagnosis == False)
            & (df.asthma_diagnosis == False)
            & (df.cancer_type != "LONGKANKER") &
            (df.cancer_type != "BORST LONG")]

# Split parameter names into a list
params = args.parameters.split(",")

# Create empty lists to store results
results = []


def get_smoking_status(row):
    if row["current_smoker"] is True:
        return "current_smoker"
    if row["ex_smoker"] is True:
        return "ex_smoker"
    if row["never_smoker"] is True:
        return "never_smoker"
    else:
        return None


df["smoking_status"] = df.apply(get_smoking_status, axis=1)
df = df.dropna(subset=["smoking_status"])

for gender in ["MALE", "FEMALE"]:
    gender_df = df[df['gender'] == gender]
    # Loop over each parameter and calculate Pearson's correlation coefficient and R-squared
    for param in params:
        for group in df["smoking_status"].unique():
            df_param = gender_df.dropna(subset=[param, 'age_at_scan'])
            df_param = df_param[df_param.smoking_status == group]
            X = df_param[['age_at_scan']].values
            y = df_param[[param]].values
            pearson, _ = pearsonr(X.T[0], y.T[0])
            model = sm.OLS(y, sm.add_constant(X)).fit()
            rsquared = model.rsquared
            pval = round(model.pvalues[1], 4)

            # Create a dictionary to store results
            result = {
                'Group': f"{gender}_{group}",
                'Parameter': param,
                'Pearson Correlation': pearson,
                'R-squared': rsquared,
                'P-value': pval
            }
            results.append(result)

# Create a pandas DataFrame from the results dictionary
results_df = pd.DataFrame.from_dict(results)
results_df = results_df.round(2)

# Output results to a CSV file
results_df.to_csv(args.output, index=False)
