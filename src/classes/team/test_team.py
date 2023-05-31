import pytest
from team import Team

def test_team_init_pos():
    test_data = {
        'name': 'Alabama',
        'run_offense': 95,
        'pass_offense': 91,
        'run_defense': 93,
        'pass_defense': 94,
        'special_teams': 91
    }
    result = Team(**test_data)
    
    assert result.name == 'Alabama'
    assert result.run_offense == 95
    assert result.pass_offense == 91
    assert result.run_defense == 93
    assert result.pass_defense == 94
    assert result.special_teams == 91

def test_team_init_int_name():
    with pytest.raises(TypeError):
        Team({
            'name': 99,
            'run_offense': 95,
            'pass_offense': 91,
            'run_defense': 93,
            'pass_defense': 94,
            'special_teams': 91
        })
        
def test_team_init_neg_rating():
    with pytest.raises(TypeError):
        Team({
            'name': 'Alabama',
            'run_offense': -1,
            'pass_offense': 91,
            'run_defense': 93,
            'pass_defense': 94,
            'special_teams': 91
        })
        
def test_team_init_zero_rating():
    with pytest.raises(TypeError):
        Team({
            'name': 'Alabama',
            'run_offense': 0,
            'pass_offense': 91,
            'run_defense': 93,
            'pass_defense': 94,
            'special_teams': 91
        })
        
def test_team_init_high_rating():
    with pytest.raises(TypeError):
        Team({
            'name': 'Alabama',
            'run_offense': 100,
            'pass_offense': 91,
            'run_defense': 93,
            'pass_defense': 94,
            'special_teams': 91
        })
        
def test_team_init_str_rating():
    with pytest.raises(TypeError):
        Team({
            'name': 'Alabama',
            'run_offense': '95',
            'pass_offense': 91,
            'run_defense': 93,
            'pass_defense': 94,
            'special_teams': 91
        })
        

    
