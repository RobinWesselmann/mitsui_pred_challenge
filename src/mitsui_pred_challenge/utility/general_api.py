"""Functions that can be used for general tasks in the project"""

import pandas as pd
import numpy as np


def prepare_target_pairs(df) -> dict:
    """ Prepare target pairs for analysis.

    Args:
        df (pd.DataFrame): DataFrame containing target pairs incl. lag assignment. 

    Returns:
        dict: Resolved relationships between targets and assets, grouped by lag.
    """

    output_dict = dict()
    distinct_lags = df["lag"].unique().tolist()

    for i, lag in enumerate(distinct_lags):

        df_tmp = df[df["lag"] == i+1].copy()
        df_tmp.loc[:, "asset_1"] = df_tmp["pair"].str.split("-").str[0]
        df_tmp.loc[:, "asset_2"] = df_tmp["pair"].str.split("-").str[1]

        output_dict[f"lag_{i+1}"] = df_tmp[["target", "asset_1", "asset_2"]]
    
    return output_dict