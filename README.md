# Football Data Processing App

## Overview
This is a Python-based command-line application for processing football match event data from a CSV file. The application normalizes the data into structured models (matches, teams, players, and statistics) and allows output as JSON or separate CSV files.

## Features
- **Processes Football Match Data**: Extracts match details, teams, players, and statistics.
- **Handles Data Normalization**: Ensures data integrity and validation.
- **CLI-Based Execution**: Can be run from the terminal.
- **CSV Output Option**: Allows saving processed data as separate CSV files.
- **Logging**: Captures logs for debugging and monitoring.
- **Unit Testing**: Ensures correctness of data processing.

## Folder Structure
```
football_match/
│── app/
│   ├── models.py          # Defines data structures with Pydantic
│   ├── transformer.py     # Extracts matches, teams, players, statistics
│   ├── validator.py       # Cleans and validates raw CSV data
│   ├── utils.py           # Helper functions for column mapping
│
│── tests/
│   ├── test_validator.py  # Unit tests for data cleaning
│   ├── test_transformer.py # Unit tests for data extraction
│   ├── test_integration.py # Full pipeline tests
│
│── main.py                # CLI entry point
│── requirements.txt       # Dependencies
│── README.md              # Documentation
```

## Prerequisites
- **Python Version**: Python 3.8 or higher is required.
- **Dependencies**: Listed in `requirements.txt`.

## Setup Instructions

### 1. Clone the Repository
```sh
git clone https://github.com/n-silva/football-data-app.git
cd football-data-app
```

### 2. Create a Virtual Environment (Recommended)
```sh
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### 3. Install Dependencies
```sh
pip install -r requirements.txt
```

### 4. Setting Up Pre-Commit (Optional)

   Before do this, make sure you are in a git repository.

   Install pre-commit:
   ```
    pip install pre-commit
   ```
   Install hooks:
   ```
    pre-commit install
   ```
   Run pre-commit manually (optional):
   ```
    pre-commit run --all-files
   ```

## Usage

### Running the Application
```sh
python main.py data/yourfile.csv
```

### Using a different delimiter
```sh
python main.py data/input.csv --csv_split=';'
```
This generates the following files:
- `output/matches.csv`
- `output/teams.csv`
- `output/players.csv`
- `output/statistics.csv`

## Testing
Run unit tests using:
```sh
pytest tests/
```

## Contributing
Pull requests are welcome! Please ensure your code adheres to the project's coding style and passes all tests.

## License
MIT License
