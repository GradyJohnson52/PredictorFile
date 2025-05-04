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


RDFFile = 'RDF_Table.csv'
PDFFile = 'PDF_Table.csv'
ROFFile = 'ROF_Table.csv'
POFFile = 'POF_Table.csv'
SDFFile = 'SDF_Table.csv'
SOFFile = 'SOF_Table.csv'
TDFFile = 'TDF_Table.csv'
TOFFile = 'TOF_Table.csv'
wp23File = 'wp23_Table.csv'
RDF_Table = pd.read_csv(RDFFile)
PDF_Table = pd.read_csv(PDFFile)
ROF_Table = pd.read_csv(ROFFile)
POF_Table = pd.read_csv(POFFile)
SDF_Table = pd.read_csv(SDFFile)
SOF_Table = pd.read_csv(SOFFile)
TDF_Table = pd.read_csv(TDFFile)
TOF_Table = pd.read_csv(TOFFile)
wp23_Table = pd.read_csv(wp23File)

RDF_Table = RDF_Table.to_dict()
RushDF = {}
for i in range(len(RDF_Table['1'])):
    team = RDF_Table['1'][i]
    yardage = RDF_Table['2'][i]
    RushDF[team] = yardage


PDF_Table = PDF_Table.to_dict()
PassDF = {}
for i in range(len(PDF_Table['1'])):
    team = PDF_Table['1'][i]
    yardage = PDF_Table['2'][i]
    PassDF[team] = yardage


ROF_Table = ROF_Table.to_dict()
RushOF = {}
for i in range(len(ROF_Table['1'])):
    team = ROF_Table['1'][i]
    yardage = ROF_Table['2'][i]
    RushOF[team] = yardage


POF_Table = POF_Table.to_dict()
PassOF = {}
for i in range(len(POF_Table['1'])):
    team = POF_Table['1'][i]
    yardage = POF_Table['2'][i]
    PassOF[team] = yardage


SDF_Table = SDF_Table.to_dict()
ScoreDF = {}
for i in range(len(SDF_Table['1'])):
    team = SDF_Table['1'][i]
    points = SDF_Table['2'][i]
    ScoreDF[team] = points


SOF_Table = SOF_Table.to_dict()
ScoreOF = {}
for i in range(len(SOF_Table['1'])):
    team = SOF_Table['1'][i]
    points = SOF_Table['2'][i]
    ScoreOF[team] = points


TDF_Table = TDF_Table.to_dict()
TurnDF = {}
for i in range(len(TDF_Table['1'])):
    team = TDF_Table['1'][i]
    takeaway = TDF_Table['2'][i]
    TurnDF[team] = takeaway


TOF_Table = TOF_Table.to_dict()
TurnOF = {}
for i in range(len(TOF_Table['1'])):
    team = TOF_Table['1'][i]
    turnover = TOF_Table['2'][i]
    TurnOF[team] = turnover


WP_Table = wp23_Table.to_dict()
WP = {}
for i in range(len(WP_Table['0'])):
    team = WP_Table['0'][i]
    WinPct = WP_Table['2'][i]
    WP[team] = WinPct

combined_dicts = [RushDF, PassDF, RushOF, PassOF, ScoreDF, ScoreOF, TurnDF, TurnOF, WP]

fbs_teams = sorted([key for key in RushDF])

def Team_Dict(dicts, key):
    collected = []
    for d in dicts:
        if key in d:
            collected.append(d[key])
    return collected 

team_values = {team: Team_Dict(combined_dicts, team) for team in fbs_teams}

class ExponentialRegression(BaseEstimator, RegressorMixin):
    def fit(self, X, y):
        self.params_, _ = curve_fit(lambda t, a, b: a * np.exp(b * t), X.ravel(), y, p0=(1, 0.1))
        return self

    def predict(self, X):
        a, b = self.params_
        return a * np.exp(b * X.ravel())

# Function to evaluate models
def evaluate_model(model, X, y):
    scores = cross_val_score(model, X, y, scoring='neg_mean_squared_error', cv=5)
    return np.mean(-scores)



# Main function to compare models on multiple datasets
def model_comparison(data_list):
    results = []
    for i, (name, filepath) in enumerate(data_list.items()):
        # Load dataset
        data = pd.read_csv(filepath)
        
        X = data.iloc[:, :-1].values
        y = 
        
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
        
        dataset_results = {'Dataset': name}
        
        # Evaluate each model
        for model_name, model in models.items():
            mse = evaluate_model(model, X, y)
            dataset_results[model_name] = mse
        
        # Identify the best model for this dataset
        best_model = min(dataset_results, key=lambda k: dataset_results[k] if k != 'Dataset' else float('inf'))
        dataset_results['Best Model'] = best_model
        
        results.append(dataset_results)
    
    results_df = pd.DataFrame(results)
    results_df.to_csv('results.csv', index=False)
    return results_df

# Run the comparison
results_df = model_comparison(data_list)
print(results_df)
