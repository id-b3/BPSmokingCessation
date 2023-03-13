#!/usr/bin/env python

import sys
from pathlib import Path
import pandas as pd

df = pd.read_csv(sys.stdin, index_col=0)
outpath = Path("./data/processed/")

# ------ REMOVE segmentations with errors
df = df[~df.bp_seg_error]
df = df[(df.bp_leak_score != 0) | (df.bp_segmental_score != 0) |
        (df.bp_subsegmental_score != 0)]
# ------ REMOVE outliers
df = df[(df.bp_tcount <= 500)]
# ------ SAVE DF
df.to_csv(str(outpath / "final_bp_db.csv"))
