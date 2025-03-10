import logging

import pandas as pd

logger = logging.getLogger(__name__)

# Expected Data Types for Each Column
COLUMN_TYPES = {
    'match_id': 'Int64',
    'match_name': 'string',
    'team_id': 'Int64',
    'team_name': 'string',
    'is_home': 'boolean',
    'player_id': 'Int64',
    'player_name': 'string',
    'goals_scored': 'Int64',
    'minutes_played': 'Int64',
}


# Expected column names
REQUIRED_COLUMNS = [
    'match_id',
    'match_name',
    'team_id',
    'team_name',
    'is_home',
    'player_id',
    'player_name',
    'goals_scored',
    'minutes_played',
]


def validate_and_clean_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """
    Cleans and validates a Pandas DataFrame before processing.

    Steps:
    1. Ensure all columns are present.
    2. Convert data types to expected formats.
    3. Remove invalid duplicate match-team combinations.
    4. Ensure players appear only once per match & team.
    """

    missing_cols = [col for col in REQUIRED_COLUMNS if col not in df.columns]
    if missing_cols:
        raise ValueError(f'Missing required columns: {missing_cols}')

    df_clean = df.copy()

    for col, dtype in COLUMN_TYPES.items():
        try:
            df_clean[col] = df_clean[col].astype(dtype)
        except Exception as e:
            raise ValueError(f"Column '{col}' has incorrect data type: {e}") from e

    logger.info('Data types validated.')

    match_team_counts = df_clean.groupby('match_id')['team_id'].nunique()
    invalid_matches = match_team_counts[match_team_counts != 2].index
    if not invalid_matches.empty:
        logger.warning(f'Removing {len(invalid_matches)} matches with more than 2 teams.')
        df_clean = df_clean[~df_clean['match_id'].isin(invalid_matches)]
    logger.info('Matches validated.')

    df_clean = df_clean.copy()
    df_clean['player_key'] = (
        df_clean['match_id'].astype(str)
        + '_'
        + df_clean['team_id'].astype(str)
        + '_'
        + df_clean['player_id'].astype(str)
    )

    duplicated_players = df_clean[df_clean.duplicated('player_key', keep=False)]
    if not duplicated_players.empty:
        logger.warning(f'Removing {len(duplicated_players)} duplicate player entries.')
        df_clean = df_clean.drop_duplicates(subset='player_key', keep='first')
    df_clean.drop(columns=['player_key'], inplace=False)
    df_clean = df_clean.copy()

    logger.info('Data cleaning completed.')
    return df_clean
