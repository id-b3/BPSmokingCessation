#!/usr/bin/env python3
import argparse
import pandas as pd
import numpy as np
from scipy.stats import ttest_ind, t
from pathlib import Path

from src.data.subgroup import get_healthy


# Define a function to prettify variable names
def prettify(var_name):
    return var_name.replace('_', ' ').title()


def main(args):
    data = pd.read_csv(args.in_file, low_memory=False)

    if args.healthy:
        data = get_healthy(data)

    # Define the descriptive stats function
    def descriptive_stats(df, group, result_dict):
        male_df = df[(df['gender'] == 'Male')]
        female_df = df[(df['gender'] == 'Female')]
        male_count = len(male_df)
        female_count = len(female_df)

        result_dict[f'Male Mean±SD {group.title()}'] = []
        result_dict[f'Female Mean±SD {group.title()}'] = []
        result_dict[f'p-val {group.title()}'] = []
        result_dict[f'Male 99% CI {group.title()}'] = []
        result_dict[f'Male 95% Range {group.title()}'] = []
        result_dict[f'Female 99% CI {group.title()}'] = []
        result_dict[f'Female 95% Range {group.title()}'] = []

        result_dict[f'Male Mean±SD {group.title()}'].append(
            f'{male_count} ({male_count/len(data)*100:.1f})')
        result_dict[f'Female Mean±SD {group.title()}'].append(
            f'{female_count} ({female_count/len(data)*100:.1f})')
        result_dict[f'p-val {group.title()}'].append('NA')
        result_dict[f'Male 99% CI {group.title()}'].append('NA')
        result_dict[f'Female 99% CI {group.title()}'].append('NA')
        result_dict[f'Male 95% Range {group.title()}'].append('NA')
        result_dict[f'Female 95% Range {group.title()}'].append('NA')

        for var in [
                'age_at_scan', 'length_at_scan', 'weight_at_scan', 'bp_tlv',
                'pack_years', 'fev1', 'fev1_pp', 'fvc', 'fev1_fvc', 'bp_pi10',
                'bp_wap_avg', 'bp_la_avg', 'bp_wt_avg', 'bp_afd', 'bp_tcount',
                'bp_airvol'
        ]:

            male_data = male_df[var].dropna()
            female_data = female_df[var].dropna()

            male_mean = male_data.mean()
            male_std = male_data.std()
            male_se = male_std / np.sqrt(len(male_data))
            male_ci = t.interval(0.99,
                                 len(male_data) - 1,
                                 loc=male_mean,
                                 scale=male_se)
            male_range = f"[{male_data.quantile(0.025)}-{male_data.quantile(0.975)}]"
            female_mean = female_data.mean()
            female_std = female_data.std()
            female_se = female_std / np.sqrt(len(female_data))
            female_ci = t.interval(0.99,
                                 len(female_data) - 1,
                                 loc=female_mean,
                                 scale=female_se)
            female_range = f"[{female_data.quantile(0.025)}-{female_data.quantile(0.975)}]"

            t_stat, p_value = ttest_ind(male_data, female_data)

            if group == 'never_smoker' and var not in result_dict['Variable']:
                result_dict['Variable'].append(prettify(var))

            result_dict[f'Male Mean±SD {group.title()}'].append(
                f'{male_mean:.2f}±{male_std:.2f}')
            result_dict[f'Female Mean±SD {group.title()}'].append(
                f'{female_mean:.2f}±{female_std:.2f}')
            result_dict[f'p-val {group.title()}'].append(f'{p_value:.4f}')
            result_dict[f'Male 99% CI {group.title()}'].append(male_ci)
            result_dict[f'Female 99% CI {group.title()}'].append(female_ci)
            result_dict[f'Male 95% Range {group.title()}'].append(male_range)
            result_dict[f'Female 95% Range {group.title()}'].append(female_range)

    # Calculate descriptive statistics and t-test p-values
    result_dict = {'Variable': ["Participants"]}
    for group in ['all', 'never_smoker', 'ex_smoker', 'current_smoker']:
        if group == 'all':
            descriptive_stats(data, group, result_dict)
            data.describe().to_csv(
                str(Path(args.out_file).parent / "demographics_all.csv"))
        else:
            descriptive_stats(data[data.smoking_status == group], group,
                              result_dict)

    # Create a DataFrame with the results
    result_df = pd.DataFrame(result_dict)
    result_df.to_csv(args.out_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument("out_file",
                        type=str,
                        help="Output report destination.")
    parser.add_argument("--healthy", action="store_true", help="Healthy only")
    args = parser.parse_args()
    main(args)
