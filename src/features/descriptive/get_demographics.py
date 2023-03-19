#!/usr/bin/env python3
import argparse
import pandas as pd
from scipy.stats import ttest_ind


# Define a function to prettify variable names
def prettify(var_name):
    return var_name.replace('_', ' ').title()


def main(args):
    data = pd.read_csv(args.in_file)
    # Calculate descriptive statistics and t-test p-values
    result_dict = {'Variable': ["Participants"]}

    for group in ['never_smoker', 'ex_smoker', 'current_smoker']:
        result_dict[f'Male Mean±SD {group.title()}'] = []
        result_dict[f'Female Mean±SD {group.title()}'] = []
        result_dict[f'p-val {group.title()}'] = []

        male_df = data[(data['gender'] == 'MALE') & (data[group] == True)]
        female_df = data[(data['gender'] == 'FEMALE') & (data[group] == True)]
        male_count = len(male_df)
        female_count = len(female_df)

        result_dict[f'Male Mean±SD {group.title()}'].append(
            f'{male_count} ({male_count/len(data)*100:.1f})%')
        result_dict[f'Female Mean±SD {group.title()}'].append(
            f'{female_count} ({female_count/len(data)*100:.1f}%)')
        result_dict[f'p-val {group.title()}'].append('NA')

        for var in [
                'age_at_scan', 'length_at_scan', 'weight_at_scan', 'bp_tlv',
                'pack_years', 'fev1', 'fev1_pp', 'fvc', 'fev1_fvc', 'bp_pi10',
                'bp_wap_avg', 'bp_la_avg', 'bp_wt_avg', 'bp_ir_avg',
                'bp_or_avg', 'bp_tcount', 'bp_airvol'
        ]:

            male_data = male_df[var].dropna()
            female_data = female_df[var].dropna()

            male_mean = male_data.mean()
            male_std = male_data.std()

            female_mean = female_data.mean()
            female_std = female_data.std()

            t_stat, p_value = ttest_ind(male_data, female_data)

            if group == 'never_smoker' and var not in result_dict['Variable']:
                result_dict['Variable'].append(prettify(var))

            result_dict[f'Male Mean±SD {group.title()}'].append(
                f'{male_mean:.1f}±{male_std:.1f}')
            result_dict[f'Female Mean±SD {group.title()}'].append(
                f'{female_mean:.1f}±{female_std:.1f}')
            result_dict[f'p-val {group.title()}'].append(f'{p_value:.2f}')

    # Create a DataFrame with the results
    result_df = pd.DataFrame(result_dict)
    result_df.to_csv(args.out_file, index=False)


if __name__ == '__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument("in_file", type=str, help="Input database csv.")
    parser.add_argument("out_file",
                        type=str,
                        help="Output report destination.")
    args = parser.parse_args()
    main(args)
