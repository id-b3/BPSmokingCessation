import pandas as pd
import numpy as np


def get_healthy(df):
    """
    This function takes a pandas DataFrame as input and returns
    a subset of the DataFrame containing healthy individuals.

    Parameters:
    df (pandas.DataFrame): The DataFrame containing the data to filter

    Returns:
    pandas.DataFrame: A subset of the original DataFrame containing
                      individuals who meet the filter criteria
    """

    df_healthy = df[(df.GOLD_stage == "0") & (df.copd_diagnosis == False)
                    & (df.asthma_diagnosis == False) &
                    (df.cancer_type != "LONGKANKER") &
                    (df.cancer_type != "BORST LONG")]
    return df_healthy
