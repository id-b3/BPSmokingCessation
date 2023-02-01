#!/usr/bin/env python

import sys
from pathlib import Path
import numpy as np
import pandas as pd

df = pd.read_csv(sys.stdin, index_col=0)
outpath = Path("./data/processed/")


# ------ PARTICIPANT CHARACTERISTICS
# Fill in missing gender values, drop the other columns
df['gender'].fillna(df['gender_first'], inplace=True)
df['age_at_scan'].replace('#NUM!', np.nan, inplace=True)
df['age_at_scan'] = df['age_at_scan'].astype(float)
df['weight_at_scan'].fillna(df['bodyweight_kg_all_m_1_max2'], inplace=True)
df['length_at_scan'].fillna(df['bodylength_cm_all_m_1_max2'], inplace=True)
df['length_at_scan'].fillna(df['bodylength_cm_all_m_1_max'], inplace=True)

df.drop([
    'gender_first', 'gender_first2', 'bodyweight_kg_all_m_1_max2',
    'bodyweight_kg_all_m_1_max', 'bodylength_cm_all_m_1_max2',
    'bodylength_cm_all_m_1_max'
],
        axis=1,
        inplace=True)

# Create age categories
age_label_5 = [
    '40-45', '45-50', '50-55', '55-60', '60-65', '65-70', '70-75', '75-80',
    '80-85', '85-90', '90-95', '95-100'
]
age_cut_5 = np.linspace(40, 100, 13)

df['age_5yr'] = pd.cut(df['age_at_scan'],
                       bins=age_cut_5,
                       labels=age_label_5,
                       right=False)

age_label_10 = [
    '40-50', '50-60', '60-70', '70-80', '80-90', '90-100'
]
age_cut_10 = np.linspace(40, 100, 7)

df['age_10yr'] = pd.cut(df['age_at_scan'],
                        bins=age_cut_10,
                        labels=age_label_10,
                        right=False)

# ------ SMOKING
# Smoking merge and fill
df['never_smoker'] = df['never_smoker_adu_c_12'].fillna(
    df['never_smoker_adu_c_1'])
df['ever_smoker'] = df['ever_smoker_adu_c_22'].fillna(
    df['ever_smoker_adu_c_2'])
df['current_smoker'] = df['current_smoker_adu_c_22'].fillna(
    df['current_smoker_adu_c_2'])
df['ex_smoker'] = df['ex_smoker_adu_c_22'].fillna(df['ex_smoker_adu_c_2'])
df['pack_years'] = df['packyears_cumulative_adu_c_22'].fillna(
    df['packyears_cumulative_adu_c_2'])
df['recent_starter'] = df['recent_starter_adu_c_22'].fillna(
    df['recent_starter_adu_c_2'])
df['recent_starter'] = df['recent_starter_adu_c_22'].fillna(
    df['recent_starter_adu_c_2'])
df['smoking_endage'] = df['smoking_endage_adu_c_22'].fillna(
    df['smoking_endage_adu_c_2'])

df.drop([
    'ever_smoker_adu_c_2', 'ever_smoker_adu_c_22', 'never_smoker_adu_c_1',
    'never_smoker_adu_c_12', 'current_smoker_adu_c_2',
    'current_smoker_adu_c_22', 'ex_smoker_adu_c_2', 'ex_smoker_adu_c_22',
    'packyears_cumulative_adu_c_2', 'packyears_cumulative_adu_c_22',
    'recent_starter_adu_c_2', 'recent_starter_adu_c_22',
    'smoking_endage_adu_c_2', 'smoking_endage_adu_c_22',
    'smoking_endage_adu_q_1', 'smoking_endage_adu_q_12'
],
        axis=1,
        inplace=True)

# ------ RESPIRATORY DISEASE
df['copd_diagnosis'] = df['copd_presence_adu_q_2'].fillna(
    df['copd_presence_adu_q_1'].fillna(
        df['spirometry_copd_all_q_1_max'].fillna(df['elon_copd_adu_q_13'])))
df['asthma_diagnosis'] = df['asthma_diagnosis_adu_q_1'].fillna(
    df['spirometry_astma_all_q_1_max'].fillna(
        df['spirometry_astma_all_q_1_max2'].fillna(
            df['elon_asthma_adu_q_06'])))
df['cancer_type'] = df['cancer_type_adu_q_1'].fillna(df['cancer_type_adu_q_2'])

df['copd_diagnosis'].replace([1, 2], ['True', 'False'], inplace=True)
df['asthma_diagnosis'].replace([1, 2], ['True', 'False'], inplace=True)

df['breathing_problems_adu_q_1'].replace([1, 2], ['BREATHING', 'False'],
                                         inplace=True)
df['coughing_presence_adu_q_1'].replace([1, 2], ['COUGHING', 'False'],
                                        inplace=True)
df['wheezing_presence_adu_q_1'].replace([1, 2], ['WHEEZE', 'False'],
                                        inplace=True)
df['elon_wheeze_adu_q_01'].replace([1, 2], ['WHEEZE', 'False'], inplace=True)

df['resp_other'] = df['wheezing_presence_adu_q_1'].fillna(
    df['elon_wheeze_adu_q_01'].fillna(df['coughing_presence_adu_q_1'].fillna(
        df['breathing_problems_adu_q_1'])))

df.drop([
    'copd_presence_adu_q_1', 'copd_presence_adu_q_2',
    'spirometry_copd_all_q_1_max', 'spirometry_astma_all_q_1_max',
    'spirometry_astma_all_q_1_max2', 'elon_copd_adu_q_13',
    'elon_asthma_adu_q_06', 'asthma_diagnosis_adu_q_1', 'cancer_type_adu_q_1',
    'cancer_type_adu_q_2', 'breathing_problems_adu_q_1',
    'coughing_presence_adu_q_1', 'wheezing_presence_adu_q_1',
    'elon_wheeze_adu_q_01'
],
        inplace=True,
        axis=1)

# ------ SPIROMETRY
df['fev1'] = df['spirometry_fev1_all_m_1_max2'].fillna(
    df['spirometry_fev1_all_m_1_max'])
df['fvc'] = df['spirometry_fvc_all_m_1_max2'].fillna(
    df['spirometry_fvc_all_m_1_max'])
df['fev1_pp'] = df['fev1_percpredicted_all_c_1_max2'].fillna(
    df['fev1_percpredicted_all_c_1_max'])
df['fev1fvc_lln'] = df['fev1fvc_lowerlimit_all_c_1_max2'].fillna(
    df['fev1fvc_lowerlimit_all_c_1_max'])
df['fev1_fvc'] = df.fev1 / df.fvc

df.drop([
    'spirometry_fev1_all_m_1_max2', 'spirometry_fev1_all_m_1_max',
    'spirometry_fvc_all_m_1_max', 'spirometry_fvc_all_m_1_max2',
    'fev1_percpredicted_all_c_1_max2', 'fev1_percpredicted_all_c_1_max',
    'fev1fvc_lowerlimit_all_c_1_max2', 'fev1fvc_lowerlimit_all_c_1_max',
    'fev1_lowerlimit_all_c_1_max2', 'fev1_lowerlimit_all_c_1_max',
    'fvc_lowerlimit_all_c_1_max2', 'fvc_lowerlimit_all_c_1_max'
],
        inplace=True,
        axis=1)

# ------ COPD GOLD Staging
# GOLD 0: FEV1/FVC > fev1fvc_lln
# GOLD 1: FEV1/FVC < fev1fvc_lln & fev1_pp > 80
# GOLD 2: FEV1/FVC < fev1fvc_lln & fev1_pp 50-80
# GOLD 3: FEV1/FVC < fev1fvc_lln & fev1_pp 50-30
# GOLD 4: FEV1/FVC < fev1fvc_lln & fev1_pp < 30

criteria = [
    ((df.fev1_pp >= 80) & (df.fev1_fvc < df.fev1fvc_lln)),
    ((df.fev1_pp < 80) & (df.fev1_pp >= 50) & (df.fev1_fvc < df.fev1fvc_lln)),
    ((df.fev1_pp < 50) & (df.fev1_pp >= 30) & (df.fev1_fvc < df.fev1fvc_lln)),
    ((df.fev1_pp < 30) & (df.fev1_fvc < df.fev1fvc_lln))
]

goldstg = ("GOLD-1", "GOLD-2", "GOLD-3", "GOLD-4")
df["GOLD_stage"] = np.select(criteria, goldstg)

# ------ REMOVE segmentations with errors
df = df[df.bp_seg_error == False]
df = df[(df.bp_leak_score != 0) | (df.bp_segmental_score != 0) |
        (df.bp_subsegmental_score != 0)]

# ------ SAVE DF
df.to_csv(str(outpath / "final_bp_db.csv"))
