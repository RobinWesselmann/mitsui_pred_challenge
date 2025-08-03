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
        df_tmp_assets = df_tmp[asset_ls].copy()

        df_tmp[f"log_return"] = np.log(df_tmp_assets / df_tmp_assets.shift(lag))
    else:
        df_tmp = df[["date_id"] + asset_ls].copy()
        df_tmp_assets_1 = df_tmp[asset_ls[0]].copy()
        df_tmp_assets_2 = df_tmp[asset_ls[1]].copy()

        df_tmp[f"log_return"] = np.log(
                                            (df_tmp_assets_1 / df_tmp_assets_1.shift(lag)) /
                                            (df_tmp_assets_2 / df_tmp_assets_2.shift(lag))
                                        )       
        
    df_tmp[f"log_return"] = df_tmp[f"log_return"].shift(-lag - 1).copy()
    
    return df_tmp[["date_id", f"log_return"]].copy()

def prepare_target_data(target_pairs_df, train_df) -> dict:
    """Creates based on the target_pairs and the train df a dictionary containing over all 4 lags 
    target values.

    Args:
        target_pairs_df (pd.DataFrame): target_pairs df mapping the assets to the targets
        train_df (pd.DataFrame): provided train_df

    Returns:
        dict: dictionary containing for each lag the relevant target data
    """

    train_dict = {}

    for lag_ in range(1,5,1):

        target_pairs_df_tmp = prepare_target_pairs(target_pairs_df)[f"lag_{lag_}"]
        lag_train_df = train_df["date_id"].to_frame().copy()

        for i in range(0, target_pairs_df_tmp.shape[0], 1):

            ls = [target_pairs_df_tmp.iloc[i]["asset_1"], target_pairs_df_tmp.iloc[i]["asset_2"]]
            ls = [element.strip() for element in ls if pd.notna(element)]

            target_no = i + (lag_ - 1) * 106
            df_tmp = calculate_log_return(df = train_df, asset_ls = ls, lag = lag_)["log_return"].rename(f"target_{target_no}")
            
            lag_train_df = pd.concat([lag_train_df, df_tmp], axis = 1)

        train_dict[f"lag_{lag_}"] = lag_train_df        
    
    return train_dict