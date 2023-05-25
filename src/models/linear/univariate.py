#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
from scipy.stats import pearsonr
import statsmodels.api as sm
from data.util.dataframe import min_max_scale


def fit_analyse(data: pd.DataFrame, bps: list, i_var: str, out_path: Path):
    """
    This function performs univariate analysis on a given data frame.

    Parameters:
    data (pd.DataFrame): The data frame to perform the analysis on.
    bps (list): A list of parameters to loop through and calculate Pearson's cc and R-squared.
    i_var (str): The independent variable to calculate correlation against.
    out_path (Path): The output file path where the results will be saved in CSV format.

    Returns:
    None

    Raises:
    None
    """

    results = []

    data = min_max_scale(data, ["age","height","weight","bmi"] + bps)

    for sex in ["Male", "Female"]:
        sex_data = data[data["sex"] == sex].copy()

        # Loop parameters and calculate Pearson's cc and R-squared
        for param in bps:
            for group in sex_data["smoking_status"].unique():
                data_param = sex_data.dropna(subset=[param, i_var])
                data_param = data_param[data_param.smoking_status == group]
                print(f"Calculating {param} wrt {i_var} for {sex} {group}")
                X = data_param[i_var].to_numpy()
                y = data_param[param].to_numpy()
                pearson, _ = pearsonr(X, y)
                model = sm.OLS(y, sm.add_constant(X)).fit()
                rsquared = model.rsquared
                pval = round(model.pvalues[1], 4)

                # Create a dictionary to store results
                result = {
                    "Group": f"{sex}_{group}",
                    "Parameter": param,
                    "Pearson Correlation": pearson,
                    "R-squared": rsquared,
                    "P-value": pval,
                }
                results.append(result)

    # Create a pandas DataFrame from the results dictionary
    results_df = pd.DataFrame.from_dict(results)
    results_df = results_df.round(2)

    # Output results to a CSV file
    results_df.to_csv((out_path / f"univariate_analysis_wrt_{i_var}.csv"), index=False)
