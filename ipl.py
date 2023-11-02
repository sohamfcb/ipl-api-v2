import numpy as np
import pandas as pd

matches=pd.read_csv('ipl-matches.csv')

def teamsAPI():
    teams=list(set(matches['Team1'].unique()))
    team_dict={
        'teams':teams
    }

    return team_dict

def teamVteamAPI(team1, team2):

    valid_team_names=list(set(matches['Team1'].unique()))

    if team1 in valid_team_names and team2 in valid_team_names:

        temp_df = matches[(matches['Team1'] == team1) & (matches['Team2'] == team2) | (matches['Team2'] == team1) & (
                    matches['Team1'] == team2)]
        total_matches = temp_df.shape[0]

        matches_won_team1 = temp_df['WinningTeam'].value_counts()[team1]
        matches_won_team2 = temp_df['WinningTeam'].value_counts()[team2]

        draws = total_matches - (matches_won_team1 + matches_won_team2)

        response = {
            'total_matches': str(total_matches),
            team1: str(matches_won_team1),
            team2: str(matches_won_team2),
            'draw/no_result': str(draws)
        }

        return response

    else:
        return {'message':'invalid team name'}