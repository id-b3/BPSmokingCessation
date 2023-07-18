#!/usr/bin/env python3

import logging
import pandas as pd
import statsmodels.api as sm

logger = logging.getLogger("BronchialParameters")


def fit_analyse(data, bps, out_path, min_max_params=False):
    data["pack_year_categories"] = data["pack_year_categories"].replace(
        "0", "0 pack-years"
    )
    spirometry = ["fev1", "fev1_pp", "fev1_fvc", "fvc"]

    results = {}

    # Perform multivariate linear regression for each dependent variable
    for param in bps:
        for func in spirometry:
            # Extract independent variables
            independent_vars = [
                "sex",
                "age",
                "height",
                "weight",
                "pack_year_categories"
            ]

            # Normalising the data
            if min_max_params:
                for var in independent_vars:
                    if data[var].dtype == int or data[var].dtype == float:
                        data[var] = (data[var] - data[var].min()) / (
                            data[var].max() - data[var].min()
                        )
                data[func] = (data[func] - data[func].min()) / (
                    data[func].max() - data[func].min()
                )
                output_file = out_path / f"multivariate_report_{param}_{func}_normalised.txt"
            else:
                output_file = out_path / f"multivariate_report_{param}_{func}.txt"

            # Create formula for the model
            formula = func + " ~ " + " + ".join(independent_vars)

            # Fit the model and print the results
            model_init = sm.formula.ols(formula=formula, data=data).fit()
            logger.debug(model_init.summary())
            formula = func + " ~ " + " + ".join(independent_vars + [param])
            model = sm.formula.ols(formula=formula, data=data).fit()
            logger.debug(model.summary())

            # Add the change in R2, AIC and BIC to the dataframe
            rsq_change = model.rsquared_adj - model_init.rsquared_adj
            aic_change = model.aic - model_init.aic
            bic_change = model.bic - model_init.bic

            # Save the results to a dictionary
            results[(param, func)] = {
                "rsq_change": rsq_change,
                "aic_change": aic_change,
                "bic_change": bic_change,
            }

            # Save the results to a text file
            with open(output_file, "w") as f:
                f.write(str(model.summary()))

    df_results = pd.DataFrame(results)
    df_results.round(4)
    df_results.to_csv(out_path / "multivariate_results.csv")
