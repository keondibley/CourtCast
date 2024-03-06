import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
from sklearn.datasets import load_iris
from sklearn.feature_selection import RFE
from sklearn.linear_model import LogisticRegression # feature selection
import statsmodels.api as sm
from sklearn import metrics
from sklearn.model_selection import train_test_split
from sklearn.metrics import confusion_matrix
from sklearn.metrics import classification_report

games = pd.read_csv("/Users/arman/Desktop/archive (9)/games.csv")
ranking = pd.read_csv('/Users/arman/Desktop/archive (9)/ranking.csv')
teams = pd.read_csv('/Users/arman/Desktop/archive (9)/teams.csv')
players = pd.read_csv('/Users/arman/Desktop/archive (9)/players.csv')

#help this is breaking everything: "DtypeWarning: Columns (6) have mixed types. Specify dtype option on import or set low_memory=False"
#details = pd.read_csv("/Users/arman/Desktop/archive (9)/games_details.csv")  

games = games.loc[games.SEASON >= 2011]
# games = games.sort_values(by = ["GAME_DATE_EST"])  #does this sort ascending or descending
# print(games)
games = games.reset_index()

ranking['SEASON_ID'].apply(lambda x: x - 20000)

#games_headers = list(games.columns)
#ranking_headers = list(ranking.columns)


#print(games.head())

def dsti(date_string): #date_string_to_int
    #helper function to turn strings into ints
    #so they can be compared
    x = date_string.split('-')  #ex. '2022-12-22' turns into ['2022', '12', '22']
    y = ''
    for val in x:
        y += val        # '20221222'
    return int(y)       # 20221222


def hwpct(hteam, game_date): #home win percentage for that season PRIOR TO THAT GAME
    #expects both parameters to be strings      (game_date takes "GAME_DATE_EST")
    game_date = dsti(game_date)
    for ind in range(len(ranking)):
        date = dsti(ranking["STANDINGSDATE"][ind])
        team = ranking["TEAM"][ind] 
        hrecord = ranking["HOME_RECORD"][ind]
        
        if date < game_date and hteam == team: # eg. '10-3'
            x = hrecord.split("-") # goes from '10-3' to ['10', '3']
            total_home_wins = int(x[0]) # turns from '10' into 10
            total_home_games = int(x[0]) + int(x[1]) #13
            hwpct = total_home_wins / total_home_games
            return hwpct #return so you only take the first record prior to the current game

#testing: passed         
# print(hwpct('Denver', '2022-12-22')) #expects 0.769
# print(hwpct('Denver', '2022-12-20')) #expects 0.75
# print(hwpct('Houston', '2022-12-16')) #expects 0.5

def rwpct(rteam, game_date): #away win percentage for that season PRIOR TO THAT GAME
    #exp parameters as strings
    game_date = dsti(game_date)
    for ind in range(len(ranking)):
        date = dsti(ranking["STANDINGSDATE"][ind])
        team = ranking["TEAM"][ind] 
        road_record = ranking["ROAD_RECORD"][ind]
        
        if date < game_date and rteam == team:
            x = road_record.split('-')
            total_road_wins = int(x[0])
            total_road_games = int(x[0]) + int(x[1])
            rwpct = total_road_wins / total_road_games
            return rwpct

        
#testing
# print(rwpct('Denver', '2022-12-22')) #expects 0.529411
# print(rwpct('Denver', '2022-12-20')) #expects 0.529411
# print(rwpct('Sacramento', "2022-12-16")) #expects 0.46666

def prev_game_fg3(team_ID, GAME_ID): # what was the fg3 pct in the team's last game? (works for both home and away team)
   
    for ind in range(len(games)):
        game_ID = games['GAME_ID'][ind]
        # print(game_ID)
        # print(GAME_ID)
        hteam = games['HOME_TEAM_ID'][ind]
        rteam = games['VISITOR_TEAM_ID'][ind]
        # print(game_ID < GAME_ID)
        if game_ID < GAME_ID:
            if hteam == team_ID:
                #print('played at home')
                return games["FG3_PCT_home"][ind]
            elif rteam == team_ID:
                #print('played away')
                return games["FG3_PCT_away"][ind]

#testing:
#if the team went from home to home
# print(type(games['GAME_ID'][0]))
# print(prev_game_fg3(1610612740, 22200477))

# #away , played home previously
#print(prev_game_fg3(1610612749, 22200457))

#home , played away prev: 
#i'll write more cases later


games = games.sort_values(by = ["GAME_DATE_EST"])  #does this sort ascending or descending

def fg3_pct_season(team_ID, GAME_ID, Season): # all parameters int type
    pcts = []
    count = 0
    #games = games.loc[games.SEASON == Season] this doesn't work
    for ind in range(len(games)):
        hteam = games['HOME_TEAM_ID'][ind]
        rteam = games['VISITOR_TEAM_ID'][ind]
        game_id = games['GAME_ID'][ind]
        season = games['SEASON'][ind]
        if game_id < GAME_ID:
            if season == Season:
                #print(season)
                if hteam == team_ID:
                    pcts.append(games["FG3_PCT_home"][ind])
                    #print(games["FG3_PCT_home"][ind])
                    count += 1
                elif rteam == team_ID:
                    pcts.append(games["FG3_PCT_away"][ind])
                    #print(games["FG3_PCT_away"][ind])
                    count += 1
    
    tpcts = 0 
    # print(count)
    # print(pcts)
    for val in pcts:
        tpcts += val #could be an issue if there's a misinput in the ds like '1.20' instead of .20
        if (val > 1) or (val < 0):
            pass
            #print(val)
            #if nothing prints here then the numbers are ok
    return tpcts / count

#all tests are of the 2021 - 2022 season (stats from ESPN)
# print(fg3_pct_season(1610612737, 22100452, 2021)) # hawks 0.373 (gives 0.37339)
# print(fg3_pct_season(1610612751, 22101148, 2021)) # nets 0.361 (gives 0.358712)
# print(fg3_pct_season(1610612741, 22101149, 2021)) # bulls 0.369 (gives 0.36599)
# print(fg3_pct_season(1610612765, 22101147, 2021)) # pistons 0.326 (gives 0.32565)





#Questions:
#whenever we have a function that calls a team name should we use the team name or the Team_ID
# how to merge dfs together so for plus minus specifically



# #X = games[] #this is where the features will go
# #y = games['HOME_TEAM_WINS'] #dependent variable we are trying to predict



# # Recommended Features:

    # PLUS_MINUS:  idk 
            # gmaes_detail
            # one for every player
            
    
    # STL: steals
            # details
            # sum the STL for each team 
            
    
    # FG3-PCT: 3-pinter %        (was it just home or diff of home and away)
            # FG_PCT_Home
            
    
    # FG-PCT:  free-throw %
            # FG3_PCT_HOME




# New Feature Ideas: 

    # AVG_Scoring_Difference (avg_home_team_score - avg_away_team_score):

    
    # Home team home win %  vs.  Away team away win % 
            # ranking csv
            # Home_Record:
                #match 
                #match TEAM_ID
            
    
    # Home team win % vs Away team win %
            # ranking
            # W_PCT header
    
    


#model_lasso = linear_model.Lasso(alpha = 0.1)

