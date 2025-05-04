import pandas as pd


dataFrame = pd.read_csv(r"C:\Users\molle\Downloads\NBA-playerlist.csv")

print("our DataFrame....", dataFrame)
player1 =dataFrame.loc[0, :]
years = dataFrame.loc[:, 'TO_YEAR']
print(player1)
print(years)

