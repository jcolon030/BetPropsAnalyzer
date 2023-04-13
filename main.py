from nba_api.stats.endpoints import playercareerstats
from nba_api.stats.endpoints import leaguegamefinder
from nba_api.stats.endpoints import playergamelog
from nba_api.stats.endpoints import playercompare
from nba_api.stats.library.parameters import SeasonAll
from nba_api.stats.static import players
import datetime
import pandas as pd
import json

PLAYERLIST = players.get_players()

class PlayerStats:
    def __init__(self, name):
        
        self.player = [player for player in PLAYERLIST if player["full_name"] == name][0] # Number filters data
        self.id = str(self.player["id"])
        
        self.full_stats = playercareerstats.PlayerCareerStats(player_id=self.id)
        
        # Per-Season Career Stats 
        self.career_stats = self.full_stats.get_data_frames()[0]
        self.career_stats = self.career_stats.to_json()

    def PlayersLast10Games(self, stat):
        gamelog = playergamelog.PlayerGameLog(player_id=self.id, season = SeasonAll.all)
        
        df_gamelog = gamelog.get_data_frames()[0] # Grab between [0:11] for last 10 games
        
        print(df_gamelog["MATCHUP"])
        
        against_log = [df_gamelog[stat][game] for game in range(len(df_gamelog)) if "TOR" == df_gamelog["MATCHUP"][game][-3:]]
        against_log = against_log[:10]
        
        per_game = [pts for pts in df_gamelog[stat][:10]]
        
        print(df_gamelog)
        
        print(per_game)
        
        print(against_log)
        
        av1 = sum(per_game)/len(per_game)
        av2 = sum(against_log)/len(against_log)
        
        return round((av1 + av2)/ 2, 2)
        
        
        
p1 = PlayerStats("Alex Caruso")

print(p1.career_stats)

#result = leaguegamefinder.LeagueGameFinder()
#print(result.get_data_frames()[0].tail())

print(p1.PlayersLast10Games("PTS"))
