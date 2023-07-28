#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


def analyse(data: pd.DataFrame, bps: list, out_path: Path):
    # Create empty lists to store results
    results = []

    data['years_quit'] = pd.cut(data['smoking_cessation_duration'],
                                [0, 5, 10, 15, 20, 100],
                                right=False,
                                labels=[
                                    '<5 years', '5-10 years', '10-15 years',
                                    '15-20 years', '20+ years'
                                ])

    results = {}

    # Loop over each parameter and calculate Pearson's correlation coefficient and R-squared
    fig = plt.figure(figsize=(8,6))
    gs = fig.add_gridspec(2, 2, hspace=0.05, wspace=0.25)
    axs = gs.subplots(sharex=True)
    
    for idx, param in enumerate(bps):
        for group in ["healthy", "unhealthy"]:
            data_group = data[data["health_status"] == group]
            data_param = data_group.dropna(
                subset=[param, 'smoking_cessation_duration', 'pack_year_categories'])

            independent_vars = [
                'sex', 'age', 'height', 'weight', 'pack_year_categories',
            ]

            formula = f"{param} ~ {' + '.join(independent_vars)}"
            model_init = sm.formula.ols(formula=formula, data=data_param).fit()
            formula = f"{param} ~ {' + '.join(independent_vars + ['smoking_cessation_duration'])}"
            model = sm.formula.ols(formula=formula, data=data_param).fit()
            with open(str(out_path / f"cessation_{param}_{group}.txt"), "w") as f:
                f.write(model.summary().as_text())

            # Add the change in R2, AIC and BIC to the dataframe
            rsq_change = model.rsquared_adj - model_init.rsquared_adj
            aic_change = model.aic - model_init.aic
            bic_change = model.bic - model_init.bic

            # Save the results to a dictionary
            results[param] = {
                "rsq_change": rsq_change,
                "aic_change": aic_change,
                "bic_change": bic_change,
            }

            x_values = np.linspace(data["smoking_cessation_duration"].min(),
                                   data["smoking_cessation_duration"].max(), 100)
            y_values = model.params['Intercept'] + model.params['sex[T.Male]'] + (
                60 * model.params['age']
            ) + (1.84 * model.params['height']) + (82 * model.params['weight']) + model.params['smoking_cessation_duration'] * x_values

            if group == "healthy":
                axs[(idx//2), (idx%2)].plot(x_values, y_values, color='blue')
            else:
                axs[(idx//2), (idx%2)].plot(x_values, y_values, color='red')
            results_data = pd.DataFrame.from_dict(results)
            results_data = results_data.round(4)

            # Output results to a CSV file
            results_data.to_csv(str(out_path / f"cessation_results_mlr_{group}.csv"), index=False)

        axs[(idx//2), (idx%2)].set_ylim(data[param].quantile(0.1), data[param].quantile(0.9))
        axs[(idx//2), (idx%2)].set_ylabel(param.replace('_avg', '').replace('bp_', '').upper())
        axs[(idx//2), (idx%2)].grid(axis='x', color='0.95')
    plt.legend(['Healthy', 'Unhealthy'])
    fig.savefig(str(out_path / f"smoking_cessation.jpg"), dpi=300)

