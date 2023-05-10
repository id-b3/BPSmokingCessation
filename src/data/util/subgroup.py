import pandas as pd


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


def normalise_bps(df: pd.DataFrame,
                  bps: list,
                  norm_to: str = "length_at_scan") -> pd.DataFrame:
    """
    Normalizes the base pairs (bps) data in a pandas dataframe (df) with respect to a specified column (norm_to).
    Parameters
    ----------
    df : pandas.DataFrame
        A pandas dataframe containing the base pairs data.
    bps : list
        A list of column names in the dataframe to be normalized.
    norm_to : str, optional
        The name of the column to normalize the bps data to. Default is "length_at_scan".
    
    Returns
    -------
    pandas.DataFrame
        A new pandas dataframe with the normalized bps data.
    """
    # Calculate the normalization factor
    norm_factor = df[norm_to]

    # Normalize the bps data
    for bp in bps:
        df[bp] = df[bp] / norm_factor

    return df
