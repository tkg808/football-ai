from pydantic import BaseModel, validator

class Team(BaseModel):
    name: str
    run_offense: int
    pass_offense: int
    run_defense: int
    pass_defense: int
    special_teams: int

    @validator('run_offense', 'pass_offense', 'run_defense', 'pass_defense', 'special_teams')
    def validate_integer_range(cls, value):
        if not 1 <= value <= 99:
            raise ValueError('must be between 1 and 99 (inclusive)')
        return value