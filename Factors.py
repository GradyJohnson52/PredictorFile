import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse
import statistics as stats
import numpy as np
import matplotlib.pyplot as plt
from sklearn.metrics import r2_score

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



#Rush Defense Factor
RushD_values = []
WinPCT_values = []

RushD_X = 0  
WinPCT_Y = 8  

for key, values in team_values.items():
    if len(values) > max(RushD_X, WinPCT_Y):
        RushD_values.append(values[RushD_X])
        WinPCT_values.append(values[WinPCT_Y])

RushD_values = np.array(RushD_values) 
WinPCT_values = np.array(WinPCT_values)

x_meanRD = stats.mean(RushD_values)
y_meanRD = stats.mean(WinPCT_values)

numeratorRD = sum((x - x_meanRD) * (y - y_meanRD) for x, y in zip(RushD_values, WinPCT_values))
denominatorRD = sum((x - x_meanRD) ** 2 for x in RushD_values)
slopeRD = numeratorRD / denominatorRD
intRD = y_meanRD - slopeRD * x_meanRD

predicted_yRD = slopeRD * RushD_values + intRD
ss_RD = sum((y - y_meanRD) ** 2 for y in WinPCT_values)
ss_resRD = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yRD))
r_sqRD = 1 - (ss_resRD / ss_RD)

#Pass Defense Factor
PassD_values = []
WinPCT_values = []

PassD_X = 1  
WinPCT_Y = 8


for key, values in team_values.items():
    if len(values) > max(PassD_X, WinPCT_Y):
        PassD_values.append(values[PassD_X])
        WinPCT_values.append(values[WinPCT_Y])

PassD_values = np.array(PassD_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanPD = stats.mean(PassD_values)
y_meanPD = stats.mean(WinPCT_values)

numeratorPD = sum((x - x_meanPD) * (y - y_meanPD) for x, y in zip(PassD_values, WinPCT_Y))
denominatorPD = sum((x - x_meanPD) ** 2 for x in PassD_values)
slopePD = numeratorPD / denominatorPD
intPD = y_meanPD - slopePD * x_meanPD

predicted_yPD = slopePD * PassD_values + intPD
ss_PD = sum((y - y_meanPD) ** 2 for y in WinPCT_values)
ss_resPD = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yPD))
r_sqPD = 1 - (ss_resPD / ss_PD)

#Rush Offense Factor
RushO_values = []
WinPCT_values = []

RushO_X = 2  
WinPCT_Y = 8


for key, values in team_values.items():
    if len(values) > max(RushO_X, WinPCT_Y):    
        RushO_values.append(values[RushO_X])
        WinPCT_values.append(values[WinPCT_Y])

RushO_values = np.array(RushO_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanRO = stats.mean(RushO_values)
y_meanRO = stats.mean(WinPCT_values)

numeratorRO = sum((x - x_meanRO) * (y - y_meanRO) for x, y in zip(RushO_values, WinPCT_Y))
denominatorRO = sum((x - x_meanRO) ** 2 for x in RushO_values)
slopeRO = numeratorRO / denominatorRO
intRO = y_meanRO - slopeRO * x_meanRO

predicted_yRO = slopeRO * RushO_values + intRO
ss_RO = sum((y - y_meanRO) ** 2 for y in WinPCT_values)
ss_resRO = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yRO))
r_sqRO = 1 - (ss_resRO / ss_RO)

#Pass Offense Factor
PassO_X = 3  
WinPCT_Y = 8

PassO_values = []
WinPCT_values = []

for key, values in team_values.items():
    if len(values) > max(PassO_X, WinPCT_Y):
        PassO_values.append(values[PassO_X])
        WinPCT_values.append(values[WinPCT_Y])

PassO_values = np.array(PassO_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanPO = stats.mean(PassO_values)
y_meanPO = stats.mean(WinPCT_values)

numeratorPO = sum((x - x_meanPO) * (y - y_meanPO) for x, y in zip(PassO_values, WinPCT_Y))
denominatorPO = sum((x - x_meanPO) ** 2 for x in PassO_values)
slopePO = numeratorPO / denominatorPO
intPO = y_meanPO - slopePO * x_meanPO

predicted_yPO = slopePO * PassO_values + intPO
ss_PO = sum((y - y_meanPO) ** 2 for y in WinPCT_values)
ss_resPO = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yPO))
r_sqPO = 1 - (ss_resPO / ss_PO)

#Score Defense Factor
ScoreD_X = 4  
WinPCT_Y = 8

ScoreD_values = []
WinPCT_values = []

for key, values in team_values.items():
    if len(values) > max(ScoreD_X, WinPCT_Y):
        ScoreD_values.append(values[ScoreD_X])
        WinPCT_values.append(values[WinPCT_Y])

ScoreD_values = np.array(ScoreD_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanSD = stats.mean(PassD_values)
y_meanSD = stats.mean(WinPCT_values)

numeratorSD = sum((x - x_meanSD) * (y - y_meanSD) for x, y in zip(ScoreD_values, WinPCT_Y))
denominatorSD = sum((x - x_meanSD) ** 2 for x in ScoreD_values)
slopeSD = numeratorSD / denominatorSD
intSD = y_meanSD - slopeSD * x_meanSD

predicted_ySD = slopeSD * ScoreD_values + intSD
ss_SD = sum((y - y_meanSD) ** 2 for y in WinPCT_values)
ss_resSD = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_ySD))
r_sqSD = 1 - (ss_resSD / ss_SD)

#Score Offense Factor
ScoreO_X = 5  
WinPCT_Y = 8

ScoreO_values = []
WinPCT_values = []

for key, values in team_values.items():
    if len(values) > max(ScoreO_X, WinPCT_Y):
        ScoreO_values.append(values[ScoreO_X])
        WinPCT_values.append(values[WinPCT_Y])

ScoreO_values = np.array(ScoreO_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanSO = stats.mean(ScoreO_values)
y_meanSO = stats.mean(WinPCT_values)

numeratorSO = sum((x - x_meanSO) * (y - y_meanSO) for x, y in zip(ScoreO_values, WinPCT_Y))
denominatorSO = sum((x - x_meanSO) ** 2 for x in ScoreO_values)
slopeSO = numeratorSO / denominatorSO
intSO = y_meanSO - slopeSO * x_meanSO

predicted_ySO = slopeSO * ScoreO_values + intSO
ss_SO = sum((y - y_meanSO) ** 2 for y in WinPCT_values)
ss_resSO = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_ySO))
r_sqSO = 1 - (ss_resSO / ss_SO)

#Takeaway Factor
TurnD_X = 6  
WinPCT_Y = 8

TurnD_values = []
WinPCT_values = []

for key, values in team_values.items():
    if len(values) > max(TurnD_X, WinPCT_Y):
        TurnD_values.append(values[TurnD_X])
        WinPCT_values.append(values[WinPCT_Y])

TurnD_values = np.array(TurnD_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanTD = stats.mean(TurnD_values)
y_meanTD = stats.mean(WinPCT_values)

numeratorTD = sum((x - x_meanTD) * (y - y_meanTD) for x, y in zip(TurnD_values, WinPCT_Y))
denominatorTD = sum((x - x_meanTD) ** 2 for x in TurnD_values)
slopeTD = numeratorTD / denominatorTD
intTD = y_meanTD - slopeTD * x_meanTD

predicted_yTD = slopeTD * TurnD_values + intTD
ss_TD = sum((y - y_meanTD) ** 2 for y in WinPCT_values)
ss_resTD = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yTD))
r_sqTD = 1 - (ss_resTD / ss_TD)

#Turnover Factor
TurnO_X = 7  
WinPCT_Y = 8

TurnO_values = []
WinPCT_values = []

for key, values in team_values.items():
    if len(values) > max(TurnO_X, WinPCT_Y):
        TurnO_values.append(values[TurnO_X])
        WinPCT_values.append(values[WinPCT_Y])

TurnO_values = np.array(TurnO_values) 
WinPCT_Y = np.array(WinPCT_values)

x_meanTO = stats.mean(TurnO_values)
y_meanTO = stats.mean(WinPCT_values)

numeratorTO = sum((x - x_meanTO) * (y - y_meanTO) for x, y in zip(TurnO_values, WinPCT_Y))
denominatorTO = sum((x - x_meanTO) ** 2 for x in TurnO_values)
slopeTO = numeratorTO / denominatorTO
intTO = y_meanTO - slopeTO * x_meanTO

predicted_yTO = slopeTD * TurnO_values + intTO
ss_TO = sum((y - y_meanTO) ** 2 for y in WinPCT_values)
ss_resTO = sum((y - pred) ** 2 for y, pred in zip(WinPCT_values, predicted_yTO))
r_sqTO = 1 - (ss_resTO / ss_TO)



print(slopePD, slopePO, slopeRD, slopeRO, slopeSD, slopeSO, slopeTD, slopeTO)