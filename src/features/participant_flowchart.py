#!/usr/bin/env python3

import sys
import pandas as pd

total_processed = 12041

df = pd.read_csv(sys.argv[1])

df_spiro = df[df.GOLD_stage == '0']
df_resp = df_spiro[(df_spiro.copd_diagnosis == False)
                   & df_spiro.asthma_diagnosis == False
                   & (df_spiro.cancer_type != "LONGKANKER")
                   & (df_spiro.cancer_type != "BORST LONG")]

counts = {
    "Processed": total_processed,
    "Poor Segmentations": total_processed - len(df),
    "Abnormal Spirometry": (len(df) - len(df_spiro)),
    "Respiratory Disease": (len(df_spiro) - len(df_resp)),
    "Healthy": len(df_resp),
    "Healthy Never-Smokers": len(df_resp[df_resp.never_smoker == True]),
    "Healthy Ex-Smokers": len(df_resp[df_resp.ex_smoker == True]),
    "Healthy Current-Smokers": len(df_resp[df_resp.current_smoker == True]),
    "Healthy No-Status": 0
}

counts["Healthy No-Status"] = counts["Healthy"] - sum(
    list(counts.values())[5:8])
head = ",".join(counts.keys())
vals = ",".join([str(num) for num in counts.values()])
with open(sys.argv[2], "w") as f:
    f.write(f"{head}\n")
    f.write(vals)
