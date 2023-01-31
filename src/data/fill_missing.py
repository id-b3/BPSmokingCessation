import sys
import pandas as pd

df = pd.read_csv(sys.stdin, index_col=0)

# ------ PARTICIPANT CHARACTERISTICS
# Fill in missing gender values, drop the other columns
df['gender'].fillna(df['gender_first'], inplace=True)
df['age_at_scan'].replace('#NUM!', 0, inplace=True)
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
