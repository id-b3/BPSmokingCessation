#!/usr/bin/env python3

import argparse
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm

from src.data.subgroup import get_healthy

# Define command line arguments
parser = argparse.ArgumentParser()
parser.add_argument("input_csv", help="Input CSV file name")
parser.add_argument("parameters",
                    help="Comma-separated list of parameter names")
parser.add_argument("output", help="Output CSV file name")
parser.add_argument("--healthy",
                    action="store_true",
                    help="Only include 'never_smoker' group")

args = parser.parse_args()
df = pd.read_csv(args.input_csv)

# Filter by smoking status if healthy flag is set
if args.healthy:
    df = get_healthy(df)

# Split parameter names into a list
params = args.parameters.split(",")
results = []

for gender in ["Male", "Female"]:
    gender_df = df[df['gender'] == gender]

    # Loop parameters and calculate Pearson's cc and R-squared
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
