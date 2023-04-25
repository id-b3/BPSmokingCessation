#!/usr/bin/env python3

import sys
import pandas as pd

total_processed = 12041

df = pd.read_csv(sys.argv[1], low_memory=False)

df_spiro = df[df.GOLD_stage == '0']
df_resp = df_spiro[(df_spiro.copd_diagnosis == False)
                   & (df_spiro.asthma_diagnosis == False)
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
    "Healthy No-Status": len(df["smoking_status"].isnull())
}

counts["Healthy No-Status"] = counts["Healthy"] - sum(
    list(counts.values())[5:8])
head = ",".join(counts.keys())
vals = ",".join([str(num) for num in counts.values()])
with open(sys.argv[2], "w") as f:
    f.write(f"{head}\n")
    f.write(vals)

mermaid = f"flowchart TD\nA[fa:fa-users All Participants - {counts['Processed']}] -->|fa:fa-lungs Normal Spirometry\\nfa:fa-head-side-cough No Respiratory Disease\\nfa:fa-lungs-virus No Hx Lung Cancer\\nfa:fa-prescription-bottle-medical No Rx use for Resp Disease| B(fa:fa-heart-pulse Healthy General Population - {counts['Healthy']})\nB --> C[fa:fa-user Never-Smokers\\n{counts['Healthy Never-Smokers']}]\nB --> D[fa:fa-ban-smoking Ex-Smokers\\n{counts['Healthy Ex-Smokers']}]\nB --> E[fa:fa-smoking Current-Smokers\\n{counts['Healthy Current-Smokers']}]\nB -.-> F[No Smoking Hx\\n{counts['Healthy No-Status']}]"

with open(sys.argv[2].replace(".csv", ".md"), "w") as f:
    f.write(mermaid)
