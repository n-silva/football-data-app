import pandas as pd
import pytest

from app.transformer import (
    extract_matches,
    extract_players,
    extract_statistics,
    extract_teams,
)


@pytest.fixture
def cleaned_dataframe():
    """Returns a cleaned DataFrame after validation step."""
    data = {
        'match_id': [1, 1, 2, 2],
        'match_name': ['Match A', 'Match A', 'Match B', 'Match B'],
        'team_id': [100, 200, 100, 200],
        'team_name': ['Team X', 'Team Y', 'Team X', 'Team Y'],
        'is_home': [True, False, False, True],
        'player_id': [1, 2, 1, 2],
        'player_name': ['Alice', 'Bob', 'Alice', 'Bob'],
        'goals_scored': [2, 1, 0, 3],
        'minutes_played': [90, 45, 60, 90],
    }
    return pd.DataFrame(data)


def test_extract_matches(cleaned_dataframe):
    """Test match extraction & validation."""
    matches = extract_matches(cleaned_dataframe)
    assert len(matches) == 2  # Expecting 2 unique matches
    assert matches[0].home_goals == 2
    assert matches[1].away_goals == 0


def test_extract_teams(cleaned_dataframe):
    """Test team extraction."""
    teams = extract_teams(cleaned_dataframe)
    assert len(teams) == 2  # 2 unique teams


def test_extract_players(cleaned_dataframe):
    """Test player extraction & uniqueness."""
    players = extract_players(cleaned_dataframe)
    assert len(players) == 2  # 24 unique players


def test_extract_statistics(cleaned_dataframe):
    """Test statistics processing & unique stat ID generation."""
    statistics = extract_statistics(cleaned_dataframe)

    assert len(statistics) == 4  # Each player should have one statistic entry

    # Validate stat_id format (match_id + player_id)
    expected_stat_id = f'{cleaned_dataframe.iloc[0]["match_id"]}{cleaned_dataframe.iloc[0]["player_id"]}'
    assert statistics[0].stat_id == int(expected_stat_id)
