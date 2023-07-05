#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import numpy as np
import statsmodels.api as sm
import matplotlib.pyplot as plt


def analyse(data: pd.DataFrame, bps: list, out_path: Path):
    # Create empty lists to store results
    results = []

    data['years_since_quit'] = data['age'] - data['smoking_end-age']
    data['years_quit'] = pd.cut(data['years_since_quit'],
                                [0, 5, 10, 15, 20, 100],
                                right=False,
                                labels=[
                                    '<5 years', '5-10 years', '10-15 years',
                                    '15-20 years', '20+ years'
                                ])

    # Loop over each parameter and calculate Pearson's correlation coefficient and R-squared
    for param in bps:
        data_param = data.dropna(
            subset=[param, 'years_since_quit', 'pack_year_categories'])

        independent_vars = [
            'sex', 'age', 'height', 'weight', 'pack_year_categories',
            'years_since_quit'
        ]

        formula = f"{param} ~ {' + '.join(independent_vars)}"
        model = sm.formula.ols(formula=formula, data=data_param).fit()
        with open(str(out_path / f"cessation_{param}.txt"), "w") as f:
            f.write(model.summary().as_text())
        rsquared = model.rsquared
        pval = round(model.f_pvalue, 4)

        # Create a dictionary to store results
        result = {'Parameter': param, 'R-squared': rsquared, 'P-value': pval}
        results.append(result)

        fig, ax = plt.subplots(figsize=(12, 6))

        x_values = np.linspace(data["years_since_quit"].min(),
                               data["years_since_quit"].max(), 100)
        y_values = model.params['Intercept'] + model.params['sex[T.Male]'] + (
            60 * model.params['age']
        ) + (1.84 * model.params['height']) + (82 * model.params['weight']) + model.params['years_since_quit'] * x_values

        ax.plot(x_values, y_values, color='red')
        # sns.regplot(x=data_param['years_since_quit'],
        #             y=model.predict(sm.add_constant(X)),
        #             scatter=False,
        #             ax=ax)
        ax.set_ylim(data_param[param].min(), data_param[param].max())
        ax.set_title(f"{param} with smoking cessation")
        ax.set_xlabel("Duration of smoking cessation")
        ax.set_ylabel(param)
        plt.tight_layout()
        fig.savefig(str(out_path / f"smoking_cessation_{param}.jpg"), dpi=300)


# Create a pandas DataFrame from the results dictionary
    results_data = pd.DataFrame.from_dict(results)
    results_data = results_data.round(2)

    # Output results to a CSV file
    results_data.to_csv(str(out_path / "cessation_results_mlr.csv"), index=False)
