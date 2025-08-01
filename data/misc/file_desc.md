- train.csv
    - Desc: 
        - Historic finance data related to commodities such as closing prices, 
        trading volumes, foreign exchange rates, and so on.
    - cols:
        - date_id: 
                - A single UTC date. Due to time zone and holiday differences, some entire 
                exchanges may not have traded on a given date
        - time_series_identifier: 
                - Each security includes a two or three letter prefix that denotes the origin of the trading activity: LME (London Mercantile Exchange), JPX (Japanese Securities Exchange), US (various US stock exchanges), and FX (foreign exchange).

- test.csv
    - Desc:
        - A mock test set representing the structure of the unseen test set. The test set used for the public leaderboard set is a copy of the last 90 dates in the train set. As a result, the public leaderboard scores are not meaningful. The unseen copy of this file served by the evaluation API may be updated during the model training phase.
    - cols:
        - date_id:
                - see above
        - time_series_identifier:
                - see above
        - is_scored:
                - Whether this row is included in the evaluation metric calculation. During the model training phase this will be true for the first 90 rows only. Test set only.
    
- train_labels.csv
    - Desc: 
        - The targets consist of log returns of one financial instrument or the differences between a pair of financial instruments. See target_pairs.csv for the details of each target column.
    - cols:
        - date_id:
                - see above
        - target_[0-423]:
                - tbd

- lagged_test_labels/test_labels_lag_[1-4].csv
    - Desc:
        - The same content as train_labels.csv, but split into separate files for each lag. This will be served by the evaluation API.
    - cols:
        - date_id:
                - In this file, indicates the date the labels are released by the evaluation API.
        - label_date_id
                - The date id when this label would have been predicted for a perfect submission.
      
- target_pairs.csv
    - Desc:
        - Details of the inputs for each target calculation. See this notebook for an illustration of how to use this information to go from price data to targets.
    - cols:
        - target:
            The name of the matching target column.
        - lag:
            The number of days of lag
        - pair:
            The security or securities