from typing import ClassVar, Dict

from pydantic import BaseModel, field_validator


class Match(BaseModel):
    match_id: int
    match_name: str
    home_team_id: int
    away_team_id: int
    home_goals: int
    away_goals: int

    @field_validator('home_goals', 'away_goals')
    def validate_goals(cls, value):
        if value < 0:
            raise ValueError('Goals cannot be negative')
        return value


class Team(BaseModel):
    team_id: int
    team_name: str


class Player(BaseModel):
    player_id: int
    player_name: str
    team_id: int

    _player_team_mapping: ClassVar[Dict[int, int]] = {}

    @field_validator('team_id', mode='before')
    @classmethod
    def validate_unique_team(cls, value, info):
        player_id = info.data.get('player_id')

        if player_id is None:
            raise ValueError('Player ID is required to validate team assignment.')

        if player_id in cls._player_team_mapping and cls._player_team_mapping[player_id] != value:
            raise ValueError(
                f'Player {player_id} is already assigned to team {cls._player_team_mapping[player_id]}.'
            )

        cls._player_team_mapping[player_id] = value
        return value


class Statistic(BaseModel):
    stat_id: int
    player_id: int
    match_id: int
    goals_scored: int
    minutes_played: int
    fraction_of_total_minutes_played: float
    fraction_of_total_goals_scored: float

    @field_validator('fraction_of_total_minutes_played', 'fraction_of_total_goals_scored')
    def validate_fractions(cls, value):
        if not 0 <= value <= 1:
            raise ValueError('Fractions must be between 0 and 1')
        return value
