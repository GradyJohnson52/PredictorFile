import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse
import statistics as stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score
from sklearn.linear_model import LinearRegression
from sklearn.preprocessing import PolynomialFeatures


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

factors = {
    'RushD': 0,  
    'PassD': 1,  
    'RushO': 2,  
    'PassO': 3,  
    'ScoreD': 4,  
    'ScoreO': 5,  
    'TurnD': 6,  
    'TurnO': 7   }


def calc_linear(X_values, y_values):
    """Linear Regression"""
    X = np.array(X_values).reshape(-1, 1)  # Reshape for sklearn
    y = np.array(y_values)
    
    model = LinearRegression().fit(X, y)
    predicted_y = model.predict(X)
    r2 = r2_score(y, predicted_y)
    
    return model.coef_[0], model.intercept_, r2

def calc_polynomial(X_values, y_values, degree):
    """Polynomial Regression of degree 2 or 3"""
    X = np.array(X_values).reshape(-1, 1)  # Reshape for sklearn
    y = np.array(y_values)
    
    poly = PolynomialFeatures(degree=degree)
    X_poly = poly.fit_transform(X)  # Apply polynomial feature transformation
    
    model = LinearRegression().fit(X_poly, y)
    predicted_y = model.predict(X_poly)
    r2 = r2_score(y, predicted_y)
    
    return model.coef_, model.intercept_, r2


def calc_exponential(X_values, y_values):
    """Exponential Regression"""
    # Check for zero or negative values in y_values, as log transform can't handle them
    y_values = np.array(y_values)
    y_values = np.where(y_values <= 0, 1e-6, y_values)  # Replace zero or negative values with a small positive number
    
    X = np.array(X_values).reshape(-1, 1)
    y_log = np.log(y_values)  # Log transform the target variable (Win PCT)
    
    model = LinearRegression().fit(X, y_log)
    predicted_y_log = model.predict(X)
    predicted_y = np.exp(predicted_y_log)  # Re-transform the predictions using exp()
    
    r2 = r2_score(y_values, predicted_y)
    
    return model.coef_[0], model.intercept_, r2


def apply_models(factor_name, team_values, wp_dict):
    # Get X values (input data) from the team_values dictionary for the factor
    factor_index = factors[factor_name]  # Get the index for the current factor
    X_values = [values[factor_index] for values in team_values.values()]  # Extract X values for the factor
    y_values = list(wp_dict.values())  # Get the WinPct values as y_values
    
    # Apply models (linear, polynomial degree 2, polynomial degree 3, and exponential)
    linear_slope, linear_intercept, r2_linear = calc_linear(X_values, y_values)
    poly2_coef, poly2_intercept, r2_poly2 = calc_polynomial(X_values, y_values, degree=2)
    poly3_coef, poly3_intercept, r2_poly3 = calc_polynomial(X_values, y_values, degree=3)
    exp_slope, exp_intercept, r2_exp = calc_exponential(X_values, y_values)
    
    # Return the results in a dictionary
    return {
        "linear": (linear_slope, linear_intercept, r2_linear),
        "poly2": (poly2_coef, poly2_intercept, r2_poly2),
        "poly3": (poly3_coef, poly3_intercept, r2_poly3),
        "exponential": (exp_slope, exp_intercept, r2_exp)
    }

# Print the model results for a given factor
def print_model_results(factor_name, results):
    print(f"Results for {factor_name}:")
    print(f"Linear: Slope = {results['linear'][0]}, Intercept = {results['linear'][1]}, R² = {results['linear'][2]}")
    print(f"Polynomial (Degree 2): Coefficients = {results['poly2'][0]}, Intercept = {results['poly2'][1]}, R² = {results['poly2'][2]}")
    print(f"Polynomial (Degree 3): Coefficients = {results['poly3'][0]}, Intercept = {results['poly3'][1]}, R² = {results['poly3'][2]}")
    print(f"Exponential: Slope = {results['exponential'][0]}, Intercept = {results['exponential'][1]}, R² = {results['exponential'][2]}")
    print("")

# Now, apply models for each factor and print the results
for factor_name in factors:
    results = apply_models(factor_name, team_values, WP)
    print_model_results(factor_name, results)
# Now, you can apply this for each factor
RushD_results = apply_models('RushD', team_values, WP)
PassD_results = apply_models('PassD', team_values, WP)
RushO_results = apply_models('RushO', team_values, WP)
PassO_results = apply_models('PassO', team_values, WP)
ScoreD_results = apply_models('ScoreD', team_values, WP)
ScoreO_results = apply_models('ScoreO', team_values, WP)
TurnD_results = apply_models('TurnD', team_values, WP)
TurnO_results = apply_models('TurnO', team_values, WP)

# Print results for each factor
def print_model_results(factor_name, results):
    print(f"Results for {factor_name}:")
    print(f"Linear: Slope = {results['linear'][0]}, Intercept = {results['linear'][1]}, R² = {results['linear'][2]}")
    print(f"Polynomial (Degree 2): Coefficients = {results['poly2'][0]}, Intercept = {results['poly2'][1]}, R² = {results['poly2'][2]}")
    print(f"Polynomial (Degree 3): Coefficients = {results['poly3'][0]}, Intercept = {results['poly3'][1]}, R² = {results['poly3'][2]}")
    print(f"Exponential: Slope = {results['exponential'][0]}, Intercept = {results['exponential'][1]}, R² = {results['exponential'][2]}")
    print("")

print_model_results("Rush Defense", RushD_results)
print_model_results("Pass Defense", PassD_results)
print_model_results("Rush Offense", RushO_results)
print_model_results("Pass Offense", PassO_results)
print_model_results("Score Defense", ScoreD_results)
print_model_results("Score Offense", ScoreO_results)
print_model_results("Turnover Defense", TurnD_results)
print_model_results("Turnover Offense", TurnO_results)

import pandas as pd

def create_summary_table(factors, team_values, wp_dict):
    # List to store all rows of data for each factor
    rows = []

    # Apply models for each factor and collect results
    for factor_name in factors:
        results = apply_models(factor_name, team_values, wp_dict)
        
        # Create a dictionary for the factor, containing the results
        row = {
            "Factor": factor_name,
            "Linear Slope": results['linear'][0],
            "Linear Intercept": results['linear'][1],
            "Linear R²": results['linear'][2],
            "Poly2 Coefficients": results['poly2'][0],
            "Poly2 Intercept": results['poly2'][1],
            "Poly2 R²": results['poly2'][2],
            "Poly3 Coefficients": results['poly3'][0],
            "Poly3 Intercept": results['poly3'][1],
            "Poly3 R²": results['poly3'][2],
            "Exponential Slope": results['exponential'][0],
            "Exponential Intercept": results['exponential'][1],
            "Exponential R²": results['exponential'][2]
        }
        
        # Append the row to the list
        rows.append(row)

    # Convert the list of rows into a DataFrame
    summary_df = pd.DataFrame(rows)
    summary_df.to_csv('summary.csv', index=False)
    
    return summary_df

# Example usage
summary_table = create_summary_table(factors, team_values, WP)

# Display the table
print(summary_table)
