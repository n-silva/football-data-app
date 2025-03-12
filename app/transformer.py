import pandas as pd

from app.models import Match, Player, Statistic, Team


def extract_matches(df: pd.DataFrame) -> list[Match]:
    """
    Extracts and normalizes the matches dataset.

    **Processing:**
    - Groups by `Match Id` to get unique matches.
    - Identifies home and away teams.
    - Computes total goals for each team.

    Args:
        df (pd.DataFrame): Cleaned match data.

    Returns:
        list[Match]: List of `Match` model instances.
    """

    matches = (
        df.groupby('match_id')
        .agg(
            match_name=('match_name', 'first'),
            home_team_id=('team_id', lambda x: x[df.loc[x.index, 'is_home']].iloc[0]),
            away_team_id=('team_id', lambda x: x[~df.loc[x.index, 'is_home']].iloc[0]),
            home_goals=('goals_scored', lambda x: x[df.loc[x.index, 'is_home']].sum()),
            away_goals=('goals_scored', lambda x: x[~df.loc[x.index, 'is_home']].sum()),
        )
        .reset_index()
    )

    return [Match(**row) for row in matches.to_dict(orient='records')]


def extract_teams(df: pd.DataFrame) -> list[Team]:
    """
    Extracts and normalizes team data.

    Args:
        df (pd.DataFrame): Cleaned dataset.

    Returns:
        list[Team]: List of unique teams.
    """
    teams = df[['team_id', 'team_name']].drop_duplicates()
    return [Team(**row) for row in teams.to_dict(orient='records')]


def extract_players(df: pd.DataFrame) -> list[Player]:
    """
    Extracts unique players from the dataset.

    Args:
        df (pd.DataFrame): Cleaned dataset.

    Returns:
        list[Player]: List of unique players with team associations.
    """
    players = df[['player_id', 'player_name', 'team_id']].drop_duplicates()
    return [Player(**row) for row in players.to_dict(orient='records')]


def extract_statistics(df: pd.DataFrame) -> list[Statistic]:
    """
    Extracts player statistics.

    **Calculations:**
    - `fraction_of_total_minutes_played = minutes_played / 90`
    - `fraction_of_total_goals_scored = goals_scored / total_goals_in_match`
    - Generates unique `stat_id` based on `match_id + team_id + player_id`.

    Args:
        df (pd.DataFrame): Cleaned dataset.

    Returns:
        list[Statistic]: List of statistics for each player.
    """
    df['fraction_of_total_minutes_played'] = df['minutes_played'] / 90
    sum_goals_sored = df.groupby('match_id')['goals_scored'].transform('sum')
    # avoid Nan when division by zero
    df['fraction_of_total_goals_scored'] = df['goals_scored'] / sum_goals_sored.where(sum_goals_sored != 0, 1)

    df['stat_id']: int = df['match_id'].astype(str) + df['player_id'].astype(str)

    stats = df[
        [
            'stat_id',
            'player_id',
            'match_id',
            'goals_scored',
            'minutes_played',
            'fraction_of_total_minutes_played',
            'fraction_of_total_goals_scored',
        ]
    ]

    return [Statistic(**row) for row in stats.to_dict(orient='records')]
