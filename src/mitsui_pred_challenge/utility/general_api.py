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

    for lag in distinct_lags:

        df_tmp = df[df["lag"] == lag].copy()
        df_tmp.loc[:, "asset_1"] = df_tmp["pair"].str.split("-").str[0]
        df_tmp.loc[:, "asset_2"] = df_tmp["pair"].str.split("-").str[1]

        output_dict[f"lag_{lag}"] = df_tmp[["target", "asset_1", "asset_2"]]
    
    return output_dict


def determine_relevant_assets(pair_df) -> list:
    """Determines the relevant assets to be considered (given a pair_dataframe)

    Args:
        pair_df (pd.DataFrame): DataFrame containing the pairs of assets (cols asset_1, asset_2) which are used to calculate the log return

    Returns:
        list: list with unique assets
    """

    for key in list(target_pairs_prep.keys()):

        ls_assets = []

        ls_tmp = list(target_pairs_prep[key]["asset_1"]) + list(target_pairs_prep[key]["asset_2"])
        ls_assets.extend(ls_tmp)


    return list(set(ls_assets))

def calculate_log_return(df, asset_ls, lag) -> pd.DataFrame:
    """_summary_

    Args:
        df (_type_): _description_
        asset (_type_): _description_
        lag (_type_): _description_

    Returns:
        pd.DataFrame: _description_
    """

    asset_ls = [element.strip() for element in asset_ls]

    if len(asset_ls)==1: 
        df_tmp = df[["date_id"] + asset_ls].copy()
        df_tmp[f"log_return_lag_{lag}"] = np.log(df_tmp[asset_ls] / df_tmp[asset_ls].shift(lag))
    else:
        df_tmp = df[["date_id"] + asset_ls].copy()
        df_tmp[f"log_return_lag_{lag}"] = np.log(
                                            (df_tmp[asset_ls[0]] / df_tmp[asset_ls[0]].shift(lag)) /
                                            (df_tmp[asset_ls[1]] / df_tmp[asset_ls[1]].shift(lag))
                                        )       
        

    return df_tmp[["date_id", f"log_return_lag_{lag}"]]