import argparse
import logging

import pandas as pd

from app.transformer import (
    extract_matches,
    extract_players,
    extract_statistics,
    extract_teams,
)
from app.validator import validate_and_clean_dataframe

logger = logging.getLogger(__name__)


def main(file_path, csv_split=','):
    """Reads CSV, validates structure, extracts normalized data."""
    try:
        logging.info(f'Loading data from {args.file_path}')
        df = pd.read_csv(file_path, delimiter=csv_split)

        # Step 1: Validate CSV structure with Pandas
        df = validate_and_clean_dataframe(df)

        # Step 2: Extract normalized data
        matches = extract_matches(df)
        teams = extract_teams(df)
        players = extract_players(df)
        statistics = extract_statistics(df)

        # Step 3: Save Outputs
        pd.DataFrame([m.model_dump() for m in matches]).to_json(
            'output/matches.jsonl', orient='records', lines=True
        )
        pd.DataFrame([t.model_dump() for t in teams]).to_json(
            'output/teams.jsonl', orient='records', lines=True
        )
        pd.DataFrame([p.model_dump() for p in players]).to_json(
            'output/players.jsonl', orient='records', lines=True
        )
        pd.DataFrame([s.model_dump() for s in statistics]).to_json(
            'output/statistics.jsonl', orient='records', lines=True
        )

        logger.info('Data processing completed successfully.')
    except Exception as e:
        logging.error(f'Error processing file: {str(e)}')


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description='Process football match data from CSV.')
    parser.add_argument('file_path', type=str, help='Path to the input CSV file.')
    parser.add_argument('--csv_split', type=str, help='Optional delimiter to split lines from CSV files')

    args = parser.parse_args()

    csv_split = ','
    if args.csv_split:
        csv_split = args.csv_split

    main(args.file_path, csv_split=',')
