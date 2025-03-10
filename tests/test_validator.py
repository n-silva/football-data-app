import pandas as pd
import pytest

from app.validator import validate_and_clean_dataframe


@pytest.fixture
def raw_dataframe():
    """Returns a raw DataFrame with intentional data issues."""
    data = {
        'match_id': [1, 1, 1, 2, 2, 3, 3, 3],  # Match 1 has 3 teams (invalid)
        'match_name': ['Match A'] * 3 + ['Match B'] * 2 + ['Match C'] * 3,
        'team_id': [
            100,
            200,
            300,
            100,
            200,
            400,
            400,
            500,
        ],  # Match 3 has duplicate teams
        'team_name': [
            'Team X',
            'Team Y',
            'Team Z',
            'Team X',
            'Team Y',
            'Team W',
            'Team W',
            'Team Q',
        ],
        'is_home': [
            True,
            False,
            False,
            True,
            False,
            True,
            False,
            False,
        ],  # Extra away team in Match 3
        'player_id': [1, 2, 3, 4, 5, 6, 6, 7],  # Player 6 appears twice in Match 3
        'player_name': [
            'Alice',
            'Bob',
            'Charlie',
            'David',
            'Eve',
            'Frank',
            'Frank',
            'George',
        ],
        'goals_scored': [2, 1, 0, 3, 2, 1, 1, 2],
        'minutes_played': [90, 45, 60, 90, 75, 90, 60, 90],
    }
    return pd.DataFrame(data)


def test_validate_and_clean_dataframe(raw_dataframe):
    """Test cleaning of invalid matches & duplicate players."""
    cleaned_df = validate_and_clean_dataframe(raw_dataframe)

    # Ensure Match 1 (which had 3 teams) is removed
    assert 1 not in cleaned_df['match_id'].unique()

    # Ensure Match 3 still exists but has only two teams
    match_3_teams = cleaned_df[cleaned_df['match_id'] == 3]['team_id'].nunique()
    assert match_3_teams == 2

    # Ensure Player 6 is not duplicated in Match 3
    match_3_players = cleaned_df[(cleaned_df['match_id'] == 3) & (cleaned_df['player_id'] == 6)]
    assert len(match_3_players) == 1
