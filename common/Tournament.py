from common.Team import Team
import random
import math
import pandas as pd
import copy



'''
Tournament class
64 slots for teams
'''


class Tournament:
    def __init__(self):
        # Dictionaries for rounds
        self._current_round = 1
        self._bracket = self.init_bracket(32)
        # Base bracket to reset to without needing to assign teams again
        self._base_bracket = None
        
        
    # Initiate an empty dictionary to represent brackets
    def init_bracket(self, num_games):
        bracket = {}
        round_num = 1 
        while num_games >= 1:
            round_name = f'R{str(round_num).zfill(2)}'
            bracket[round_name] = {}
            for n in range(int(num_games)):
                bracket[round_name][f'G{str(n+1).zfill(2)}'] = {"T1": None, "T2": None,
                                                  "Winner": None, "Loser": None}
        
            num_games /= 2
            round_num += 1
        
        return bracket
    
    
    def get_bracket(self):
        return self._bracket
    
    # Set a single team in a bracket slot
    def set_team(self, round_name: str, game_name: str, team_name: str, team: Team):
        self._bracket[round_name][game_name][team_name] = team
        
        
    # Load in leads from a CSV file
    # Seed, Name, Weight
    def set_teams_from_csv(self, filename):
        
        teams = pd.read_csv(filename)
        for index, row in teams.iterrows():
            game_num = math.ceil(row['Seed'] / 2)
            t = Team(row['Name'], row['Weight'])
            
            if row['Seed'] % 2 == 0:
                team_num = 2
            else:
                team_num = 1

            self.set_team("R01", f"G{str(game_num).zfill(2)}", 
                          f"T{team_num}", t)
        
        # Set deep copy of bracket to base_bracket
        self._base_bracket = copy.deepcopy(self._bracket)
        
        
        
    
    # Simulate a single game
    def play_game(self, round_name: str, game_name: str):
        
        game = self._bracket[round_name][game_name]
        
        t1 = game['T1']
        t2 = game['T2']
        
        if t1 is None or t2 is None:
            raise ValueError("Teams not set. Please set teams and retry.")
                
        w1 = t1.weight()
        w2 = t2.weight()
        
        # Simulate game with weights
        if random.random() < w1 / (w1+w2):
            game['Winner'] = t1
            game['Loser'] = t2
        else:
            game['Winner'] = t2
            game['Loser'] = t1
            
        return game
    
    
    # Simulate all games in a given round
    def play_all_games_round(self, round_name: str):
        
        game_names = self._bracket[round_name].keys()
        
        for g in game_names:
            self.play_game(round_name, g)
            
        return self._bracket[round_name]
    
    
    
    # Advance all winners to next round
    def advance_winners_next_round(self, curr_round_name: str):
        
        next_round_num = int(curr_round_name[1:3]) + 1
        
        for g in self._bracket[curr_round_name].keys():
            
            winner = self._bracket[curr_round_name][g]['Winner']
            
            curr_game_num = int(g[1:3])
            next_game_num = math.ceil(curr_game_num/2)
            if curr_game_num / 2 < next_game_num:
                next_team_num = 1
            else:
                next_team_num = 2
                
               
            self.set_team(f"R{str(next_round_num).zfill(2)}", 
                          f"G{str(next_game_num).zfill(2)}",
                          f"T{str(next_team_num)}", winner)
            
            
            
    
    
    def play_all_games(self):
        curr_round = 1
        
        while curr_round <= 6:
            
            round_name = f"R{str(curr_round).zfill(2)}"
            self.play_all_games_round(round_name)
            
            if curr_round != 6:
                self.advance_winners_next_round(round_name)
            
            curr_round += 1
            
            
            
            
    def get_winner(self, round_name, game_name):
        
        return self._bracket[round_name][game_name]['Winner']
            
            
            
    # Reset bracket to base bracket.
    # Teams and weights set but no games simulated
    def reset(self):
        self._current_round = 1
        self._bracket = copy.deepcopy(self._base_bracket)
        
        
        
    ###### Bracket to CSV ######
    
    
    
    
    
    
    
    
        
        
        
    ##### Print Functions ######
     
    def print_round(self, round_name):
        bracket = self._bracket
        strr = f'===== ROUND {int(round_name[1:3])} =====\n'
        
        for g in bracket[round_name].keys():
                strr += f"{g}: {bracket[round_name][g]['T1']}\tvs\t{bracket[round_name][g]['T2']}\t\t"\
                        f"WINNER: {bracket[round_name][g]['Winner']}\n"
    
        print(strr)
    
    
    
    def print_bracket(self):
        print(self.__str__)

        
    
    def __str__(self):
        bracket = self._bracket
        strr = ''
        
        for rd in bracket.keys():
            strr += f"===== ROUND {rd[1:3]} =====\n"
            
            for g in bracket[rd].keys():
                strr += f"{g}: {bracket[rd][g]['T1']}\tvs\t{bracket[rd][g]['T2']}\t" \
                        f"WINNER: {bracket[rd][g]['Winner']}\n"
            
        return strr
            
        
            