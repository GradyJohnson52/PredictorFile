import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse
import statistics
import math

RDFile = 'RD_Table.csv'
PDFile = 'PD_Table.csv'
ROFile = 'RO_Table.csv'
POFile = 'PO_Table.csv'
SDFile = 'SD_Table.csv'
SOFile = 'SO_Table.csv'
TDFile = 'TD_Table.csv'
TOFile = 'TO_Table.csv'
TRFile = 'TR_Table.csv'
Model_Results = 'summary.csv'
Best_Model = 'Best_Model.csv'
RD_Table = pd.read_csv(RDFile)
PD_Table = pd.read_csv(PDFile)
RO_Table = pd.read_csv(ROFile)
PO_Table = pd.read_csv(POFile)
SD_Table = pd.read_csv(SDFile)
SO_Table = pd.read_csv(SOFile)
TD_Table = pd.read_csv(TDFile)
TO_Table = pd.read_csv(TOFile)
TR_Table = pd.read_csv(TRFile)
Models = pd.read_csv(Model_Results)
Best_Model = pd.read_csv

RD_Table = RD_Table.to_dict()
RushD = {}
for i in range(len(RD_Table['1'])):
    team = RD_Table['1'][i]
    yardage = RD_Table['2'][i]
    RushD[team] = yardage


PD_Table = PD_Table.to_dict()
PassD = {}
for i in range(len(PD_Table['1'])):
    team = PD_Table['1'][i]
    yardage = PD_Table['2'][i]
    PassD[team] = yardage


RO_Table = RO_Table.to_dict()
RushO = {}
for i in range(len(RO_Table['1'])):
    team = RO_Table['1'][i]
    yardage = RO_Table['2'][i]
    RushO[team] = yardage


PO_Table = PO_Table.to_dict()
PassO = {}
for i in range(len(PO_Table['1'])):
    team = PO_Table['1'][i]
    yardage = PO_Table['2'][i]
    PassO[team] = yardage


SD_Table = SD_Table.to_dict()
ScoreD = {}
for i in range(len(SD_Table['1'])):
    team = SD_Table['1'][i]
    points = SD_Table['2'][i]
    ScoreD[team] = points


SO_Table = SO_Table.to_dict()
ScoreO = {}
for i in range(len(SO_Table['1'])):
    team = SO_Table['1'][i]
    points = SO_Table['2'][i]
    ScoreO[team] = points


TD_Table = TD_Table.to_dict()
TurnD = {}
for i in range(len(TD_Table['1'])):
    team = TD_Table['1'][i]
    takeaway = TD_Table['2'][i]
    TurnD[team] = takeaway


TO_Table = TO_Table.to_dict()
TurnO = {}
for i in range(len(TO_Table['1'])):
    team = TO_Table['1'][i]
    turnover = TO_Table['2'][i]
    TurnO[team] = turnover


TR_Table = TR_Table.to_dict()
Rank = {}
for i in range(len(TR_Table['2'])):
    team = TR_Table['0'][i]
    ranking = TR_Table['2'][i]
    Rank[team] = ranking

combined_dicts = [RushD, PassD, RushO, PassO, ScoreD, ScoreO, TurnD, TurnO, Rank]

fbs_teams = sorted([key for key in RushD])

def Team_Dict(dicts, key):
    collected = []
    for d in dicts:
        if key in d:
            collected.append(d[key])
    return collected 

team_values = {team: Team_Dict(combined_dicts, team) for team in fbs_teams}

'''for team, values in team_values.items():
    print(f"{team}: {values}")'''




class Predictor:


    def __init__(self, name, RushD, PassD, RushO, PassO, ScoreD, ScoreO, TurnD, TurnO, WinPct):
        self.name = name
        self.RushD = RushD
        self.PassD = PassD
        self.RushO = RushO
        self.PassO = PassO
        self.ScoreD = ScoreD
        self.ScoreO = ScoreO
        self.TurnD = TurnD
        self.TurnO = TurnO
        self.WinPct = WinPct

    def LinearModel(team, slope, intercept, Rsq):
        model = (team * slope) + intercept
        result = model * Rsq
        return result

    def Poly2Model(team, coeffs, intercept, Rsq):
        # coeffs[0] = a, coeffs[1] = b, intercept = c
        model = (coeffs[0] * team**2) + (coeffs[1] * team) + intercept
        result = model * Rsq
        return result

    def Poly3Model(team, coeffs, intercept, Rsq):
        # coeffs[0] = a, coeffs[1] = b, coeffs[2] = c, intercept = d
        model = (coeffs[0] * team**3) + (coeffs[1] * team**2) + (coeffs[2] * team) + intercept
        result = model * Rsq
        return result

    def ExpModel(team, slope, intercept, Rsq):
        model = intercept * math.exp(slope * team)
        result = model * Rsq
        return result
    
    # RushDF: Polynomial (degree 2) best fit
    def RushDF(team):
        coeffs = [0, 0.19809488, -0.00067264]  # a, b
        intercept = 38.59671829151987
        Rsq = 0.004898750977543109
        return Poly2Model(team, coeffs, intercept, Rsq)

    # PassDF: Linear best fit
    def PassDF(team):
        slope = -0.04205829675775535
        intercept = 61.622817198466244
        Rsq = 0.004524979991828659
        return LinearModel(team, slope, intercept, Rsq)

    # RushOF: Linear best fit
    def RushOF(team):
        slope = 0.0217090641665092
        intercept = 48.81552902904929
        Rsq = 0.0020420557290231622
        return LinearModel(team, slope, intercept, Rsq)

    # PassOF: Polynomial (degree 3) best fit
    def PassOF(team):
        coeffs = [0, -2.14236955, 9.77189288e-03]  # a, b, c
        intercept = 200.66886466297947
        Rsq = 0.05243069283909363
        return Poly3Model(team, coeffs, intercept, Rsq)

    # ScoreDF: Linear best fit
    def ScoreDF(team):
        slope = -0.3359265129190195
        intercept = 61.312288760542515
        Rsq = 0.011210109580383154
        return LinearModel(team, slope, intercept, Rsq)

    # ScoreOF: Polynomial (degree 3) best fit
    def ScoreOF(team):
        coeffs = [0, 7.98311938, -2.87605931e-01]  # a, b, c
        intercept = -14.752919660040398
        Rsq = 0.01975603633252765
        return Poly3Model(team, coeffs, intercept, Rsq)

    # TurnDF: Polynomial (degree 2) best fit
    def TurnDF(team):
        coeffs = [0, -37.08259418, 14.79610023]  # a, b
        intercept = 72.79938598651026
        Rsq = 0.02988826659272914
        return Poly2Model(team, coeffs, intercept, Rsq)

    # TurnOF: Linear best fit
    def TurnOF(team):
        slope = -3.799167236470145
        intercept = 57.535542469919484
        Rsq = 0.005619925961779737
        return LinearModel(team, slope, intercept, Rsq)

    '''def compare_rush_off(self, opponent):
        team = self.RushO 
        opponent = opponent.RushO
        resTeam = RushOF(team)
        resOpp = RushOF(Opponent)
        return resTeam - resOpp'''

    @staticmethod
    def compare_rush_off(team1, team2):
        resTeam1 =  Predictor.RushOF(team_values[team1][2])   
        resTeam2 =  Predictor.RushOF(team_values[team2][2])   
        return resTeam1 - resTeam2

    @staticmethod
    def compare_pass_off(team1, team2):
        resTeam1 =  Predictor.PassOF(team_values[team1][3])   
        resTeam2 =  Predictor.PassOF(team_values[team2][3])   
        return resTeam1 - resTeam2

    @staticmethod
    def compare_rush_def(team1, team2):
        resTeam1 =  Predictor.RushDF(team_values[team1][0])   
        resTeam2 =  Predictor.RushDF(team_values[team2][0])   
        return resTeam1 - resTeam2

    @staticmethod
    def compare_pass_def(team1, team2):
        resTeam1 =  Predictor.PassDF(team_values[team1][1])   
        resTeam2 =  Predictor.PassDF(team_values[team2][1])   
        return resTeam1 - resTeam2
    
    @staticmethod
    def compare_score_off(team1, team2):
        resTeam1 =  Predictor.ScoreOF(team_values[team1][5])   
        resTeam2 =  Predictor.ScoreOF(team_values[team2][5])   
        return resTeam1 - resTeam2
    
    @staticmethod
    def compare_score_def(team1, team2):
        resTeam1 =  Predictor.ScoreDF(team_values[team1][4])   
        resTeam2 =  Predictor.ScoreDF(team_values[team2][4])   
        return resTeam1 - resTeam2
    
    @staticmethod
    def compare_turn_off(team1, team2):
        resTeam1 =  Predictor.TurnOF(team_values[team1][7])   
        resTeam2 =  Predictor.TurnOF(team_values[team2][7])   
        return resTeam1 - resTeam2

    @staticmethod
    def compare_turn_def(team1, team2):
        resTeam1 =  Predictor.TurnDF(team_values[team1][6])   
        resTeam2 =  Predictor.TurnDF(team_values[team2][6])   
        return resTeam1 - resTeam2
    
    @staticmethod
    def predict_winner():
        """Predict the winner based on team advantages"""
        # Ask the user to input team names
        team1 = input(f"Enter the name of the first team from the list:  ")
        team2 = input(f"Enter the name of the second team from the list: {', '.join(fbs_teams)}: ")

        # Get the team objects based on user input
        if team1 not in fbs_teams or team2 not in fbs_teams:
            print("One or both of the entered team names are invalid. Please try again.")
            return

        # Factor comparison
        rushO_adv = Predictor.compare_rush_off(team1, team2)
        rushD_adv = compare_rush_def(team1, team2)
        passO_adv = team1.compare_pass_off(team2)
        PassD_adv = team1.compare_pass_def(team2)
        scoreO_adv = team1.compare_score_off(team2)
        scoreD_adv = team1.compare_score_def(team2)
        turnO_adv = team1.compare_turn_off(team2)
        turnD_adv = team1.compare_turn_def(team2)
        
        # Calculate total advantage for team1 and team2
        advantage_team1 = rushO_adv + rushD_adv + passO_adv + passD_adv + scoreO_adv + scoreD_adv + turnO_adv + turnD_adv
        tot_adv1 = team1.WinPct + advantage_team1 
        advantage_team2 = -advantage_team1   
        tot_adv2 = team2.WinPct + advantage_team2


        # Determine the winner based on the total advantages
        if tot_adv1 > 0:
            print(f"The predicted winner is: {team1}")
            return team1
        elif tot_adv2 > 0:
            print(f"The predicted winner is: {team2}")
            return team2
        else:
            print("The match is predicted to be a tie.")
            return "Tie"

    
Predictor.predict_winner()