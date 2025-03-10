import os
import subprocess

import pandas as pd
import pytest

TEST_DATA_DIR = 'tests/data'
INPUT_TESTE_FILE = os.path.join(TEST_DATA_DIR, 'test_input.csv')


@pytest.fixture(scope='module')
def sample_test_data():
    """Creates a temporary test dataset for integration testing."""
    os.makedirs(TEST_DATA_DIR, exist_ok=True)
    test_file = INPUT_TESTE_FILE

    data = {
        'match_id': [1, 1, 2, 2, 3, 3, 4, 4],
        'match_name': [
            'Match A',
            'Match A',
            'Match B',
            'Match B',
            'Match C',
            'Match C',
            'Match D',
            'Match D',
        ],
        'team_id': [100, 200, 100, 200, 300, 400, 500, 600],
        'team_name': [
            'Team X',
            'Team Y',
            'Team X',
            'Team Y',
            'Team Z',
            'Team W',
            'Team P',
            'Team Q',
        ],
        'is_home': [True, False, True, False, True, False, True, False],
        'player_id': [1, 2, 3, 4, 5, 6, 7, 8],
        'player_name': [
            'Alice',
            'Bob',
            'Charlie',
            'David',
            'Eve',
            'Frank',
            'George',
            'Gerard',
        ],
        'goals_scored': [2, 1, 0, 3, 2, 2, 5, 1],
        'minutes_played': [90, 45, 60, 90, 90, 90, 78, 35],
    }

    df = pd.DataFrame(data)
    df.to_csv(test_file, index=False)
    return test_file


def test_full_dataset_processing(sample_test_data):
    """Tests the full dataset processing from CSV to JSONL."""

    command = ['python', 'main.py', sample_test_data]
    subprocess.run(command, check=True)

    for file in ['matches.jsonl', 'teams.jsonl', 'players.jsonl', 'statistics.jsonl']:
        assert os.path.exists(f'output/{file}'), f'Output {file} missing!'

    matches_df = pd.read_json('output/matches.jsonl', lines=True)
    assert len(matches_df) == 4
