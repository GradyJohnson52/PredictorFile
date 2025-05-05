import pandas as pd
import numpy as np
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures
from sklearn.model_selection import train_test_split, cross_val_score
from sklearn.metrics import mean_squared_error
from sklearn.pipeline import Pipeline
from sklearn.base import BaseEstimator, RegressorMixin
from scipy.optimize import curve_fit

RDFile = 'RD_Table.csv'
PDFile = 'PD_Table.csv'
ROFile = 'RO_Table.csv'
POFile = 'PO_Table.csv'
SDFile = 'SD_Table.csv'
SOFile = 'SO_Table.csv'
TDFile = 'TD_Table.csv'
TOFile = 'TO_Table.csv'
TRFile = 'TR_Table.csv'
RD_Table = pd.read_csv(RDFile)
PD_Table = pd.read_csv(PDFile)
RO_Table = pd.read_csv(ROFile)
PO_Table = pd.read_csv(POFile)
SD_Table = pd.read_csv(SDFile)
SO_Table = pd.read_csv(SOFile)
TD_Table = pd.read_csv(TDFile)
TO_Table = pd.read_csv(TOFile)
TR_Table = pd.read_csv(TRFile)

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
WP = {}
for i in range(len(TR_Table['0'])):
    team = TR_Table['0'][i]
    WinPCT = TR_Table['2'][i]
    WP[team] = WinPCT

fbs_teams = sorted([key for key in RushD])

def Team_Dict(dicts, key):
    collected = []
    for d in dicts:
        if key in d:
            collected.append(d[key])
    return collected 


combined_dicts = [RushD, PassD, RushO, PassO, ScoreD, ScoreO, TurnD, TurnO, WP]

team_values = {team: Team_Dict(combined_dicts, team) for team in fbs_teams}

for team, values in team_values.items():
    print(f"{team}: {values}")


# Class for Exponential Regression
class ExponentialRegression(BaseEstimator, RegressorMixin):
    def fit(self, X, y):
        self.params_, _ = curve_fit(lambda t, a, b: a * np.exp(b * t), X.ravel(), y, p0=(1, 0.1))
        return self

    def predict(self, X):
        a, b = self.params_
        return a * np.exp(b * X.ravel())


# Function to evaluate models using cross-validation
def evaluate_model(model, X, y):
    scores = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=5)
    return np.mean(-scores)


# Main function to compare models on multiple datasets (variables)
def model_comparison(combined_dicts, target_dict):
    results = []
    
    # Iterate over each variable (RushDF, PassDF, etc.) and its corresponding values
    for i, (variable_name, variable_dict) in enumerate(zip(
            ['RushDF', 'PassDF', 'RushOF', 'PassOF', 'ScoreDF', 'ScoreOF', 'TurnDF', 'TurnOF'],
            combined_dicts)):
        
        # Prepare the data
        X = np.array([variable_dict[team] for team in fbs_teams]).reshape(-1, 1)  # Reshape for sklearn
        y = np.array([target_dict[team] for team in fbs_teams])  # Win percentage as y
        
        # Define models to test
        models = {
            'Linear': Pipeline([('linear', LinearRegression())]),
            'Polynomial (degree=2)': Pipeline([
                ('poly', PolynomialFeatures(degree=2)),
                ('linear', LinearRegression())
            ]),
            'Polynomial (degree=3)': Pipeline([
                ('poly', PolynomialFeatures(degree=3)),
                ('linear', LinearRegression())
            ]),
            'Exponential': ExponentialRegression()
        }
        
        dataset_results = {'Variable': variable_name}
        
        # Evaluate each model
        for model_name, model in models.items():
            mse = evaluate_model(model, X, y)
            dataset_results[model_name] = mse
        
        # Identify the best model for this variable
        best_model = min(dataset_results, key=lambda k: dataset_results[k] if k != 'Variable' else float('inf'))
        dataset_results['Best Model'] = best_model
        
        results.append(dataset_results)
    
    # Save results to a DataFrame and return it
    Best_Model_df = pd.DataFrame(results)
    Best_Model_df.to_csv('Best_Model.csv', index=False)
    return Best_Model_df



# Target dictionary (WinPct from wp23)
target_dict = WP

# Define the list of teams (preloaded)
fbs_teams = sorted([key for key in RushD])  # Assuming RushDF contains all FBS teams

# Run the comparison
Best_Model_df = model_comparison(combined_dicts, target_dict)
print(Best_Model_df)


