import pandas as pd
from tqdm import tqdm
import time

import matplotlib.pylab as plt 
import seaborn as sns

from common.Team import Team
from common.Tournament import Tournament




'''
Run monte carlo simulation for March Madness
num_sims: <int> number of simulations to run
teams_csv_filename: <str> name of file with team seeds, names, weights as columns
'''
def run_monte_carlo(num_sims, teams_csv_filename):
    
    print(f"Running Monte Carlo Simulations: {num_sims}")
    print(f"Teams CSV File: {teams_csv_filename}")
    
    time.sleep(0.3)
    
    # Create tournament with teams from CSV file
    tmn = Tournament(teams_csv = teams_csv_filename)
    
    teams = pd.read_csv(teams_csv_filename)
    
    # List to hold winner of each simulation
    winner_list = []
    
    # Run simulations and append winner to list
    for i in tqdm(range(num_sims)):
        tmn.reset()
        tmn.play_all_games()
        winner = tmn.get_final_winner()
        winner_list.append(winner.name())
    
    # Count wins
    winners = pd.DataFrame(pd.Series(winner_list).value_counts()).reset_index()
    winners.columns = ['Name', 'Wins']
    winners['Win%'] = round(winners['Wins'] / num_sims * 100, 3)
    
    time.sleep(0.3)
    

    # Merge with teams
    m = teams.merge(winners, on = 'Name')
    print(m.sort_values('Wins', ascending=False).head())
    
    # Return aggregate wins dataframe
    return m
    
    

# Plot Wins vs Weighting given a Monte Carlo results DataFrame
def mc_scatterplot(mc_df):
    
    #fig, ax = plt.subplots(figsize = (12, 12))
    p = sns.scatterplot(data = m, x='Weight', y = 'Wins').set_title("Monte Carlo Wins vs Weight")

    for index, row in m.iterrows():
        plt.text(row['Weight']+0.25, row['Wins']-0.25, row['Name'])
        
    return p



def mc_barplot(mc_df):
    
    p = sns.barplot(data = m, x = 'Wins', y = 'Name', orient = 'h', palette = 'flare')
    return p




if __name__ == '__main__':
    
    m = run_monte_carlo(1000, 'teams_64_kenpom_adjEM.csv')
    
    #p = mc_barplot(m)
    p = mc_scatterplot(m)
    
    plt.show()



