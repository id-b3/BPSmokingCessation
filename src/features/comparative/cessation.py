#!/usr/bin/env python3

from pathlib import Path
import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns


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
    fig = plt.figure(figsize=(8,8))
    gs = fig.add_gridspec(3, 2, hspace=0.05, wspace=0.25)
    axs = gs.subplots(sharex=True)

    fig_res = plt.figure(figsize=(8,8))
    gs_res = fig_res.add_gridspec(3, 2, hspace=0.15, wspace=0.25)
    axs_res = gs_res.subplots()

    bps = bps + ['fev1_pp', 'fev1_fvc']

    for idx, param in enumerate(bps):
        for group in ["healthy", "unhealthy"]:
            axis = axs[(idx//2), (idx%2)]
            axis_res = axs_res[(idx//2), (idx%2)]
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

            df_resid = data_param.copy()
            df_resid["fitted"] = model.fittedvalues
            df_resid = df_resid[(df_resid.age >= 45) & (df_resid.age <= 70)]
            if group == "healthy":
                sns.regplot(data=df_resid, x='smoking_cessation_duration', y="fitted", color='blue', scatter=False, ax=axis, label="Healthy")
                sns.regplot(x=model.fittedvalues, y=model.resid, color="blue", scatter_kws={'alpha': 0.1}, ax=axis_res, label="Healthy")
            else:
                sns.regplot(data=df_resid, x='smoking_cessation_duration', y="fitted", color='red', scatter=False, ax=axis, label="Unhealthy")
                sns.regplot(x=model.fittedvalues, y=model.resid, color="red", scatter_kws={'alpha': 0.1}, ax=axis_res, label="Unhealthy")

            results_data = pd.DataFrame.from_dict(results)
            results_data = results_data.round(4)

            # Output results to a CSV file
            results_data.to_csv(str(out_path / f"cessation_results_mlr_{group}.csv"), index=False)

        axis.set_ylim(data[param].quantile(0.05), data[param].quantile(0.9))
        axis.set_ylabel(param.replace('_avg', '').replace('bp_', '').replace('fev1_pp', 'fev1 pp').replace('fev1_fvc', 'fev1/fvc').upper(), fontweight='bold')
        axis.set_xlabel("Smoking Cessation Duration")
        axis.grid(axis='x', color='0.95')
        axis_res.set_ylabel(param.replace('_avg', '').replace('bp_', '').replace('fev1_pp', 'fev1 pp').replace('fev1_fvc', 'fev1/fvc').upper(), fontweight='bold')
        axis_res.grid(axis='x', color='0.95')
    axs[0, 0].legend()
    axs_res[0, 0].legend()
    fig.savefig(str(out_path / f"smoking_cessation.jpg"), dpi=300)
    fig_res.savefig(str(out_path / f"smoking_cessation_res.jpg"), dpi=300)
    plt.show()

