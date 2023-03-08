#!/usr/bin/env python3

import pandas as pd

df = pd.read_csv("data/processed/final_bp_db.csv")
print(f"Total num participants: {len(df)}")

df_nocopd = df[df.GOLD_stage == '0']
print(f"Normal spirometry participants: {len(df_nocopd)}")

df_noresp = df_nocopd[(df_nocopd.copd_diagnosis == False)
               & (df_nocopd.asthma_diagnosis == False) &
               (df_nocopd.cancer_type != "LONGKANKER") &
               (df_nocopd.cancer_type != "BORST LONG")]
print(f"No resp disease participants: {len(df_noresp)}")

print(f"Never smokers: {len(df_noresp[df_noresp.never_smoker == True])}")
print(f"Ex smokers: {len(df_noresp[df_noresp.ex_smoker == True])}")
print(f"Current smokers: {len(df_noresp[df_noresp.current_smoker == True])}")
print(f"Unknown smoking: {len(df_noresp[df_noresp.never_smoker == ''])}")
