#!/usr/bin/env python

import sys
from pathlib import Path
import pandas as pd

df = pd.read_csv(sys.stdin, index_col=0)
df = df[~df.index.duplicated(keep="first")]
outpath = Path("./data/processed/")
print(df.bp_pi10.describe())

sizes = {}
# ------ Only use ex-smokers
df = df[df.smoking_status == "ex_smoker"]
# ------ Remove participants with missing demographic data
df = df.dropna(subset=["age", "sex", "height", "weight"])
df = df[df.smoking_cessation_duration <= 50]
df = df[df.bmi <= 45]
df = df[df.pack_years >= 1]
# ------ REMOVE segmentations with errors
sizes["total"] = len(df)
df = df[~df.bp_seg_error]
sizes["error"] = sizes["total"] - len(df)
df = df[(df.bp_leak_score != 0) | (df.bp_segmental_score != 0) |
        (df.bp_subsegmental_score != 0)]
sizes["screened"] = sizes["total"] - sizes["error"] - len(df)
# ------ SAVE DF
df.to_csv(str(outpath / "final_bp_db.csv"))

print(f"Removed:\n {sizes}")

