import pandas as pd
import requests
from bs4 import BeautifulSoup as bs
import argparse

pd.set_option('display.max_rows', None)
pd.set_option('display.max_columns', None)

parser = argparse.ArgumentParser()
parser.add_argument("-q", help="for search term")
args = parser.parse_args()

# Define all the URLs
urls = {
    "RD": "https://www.teamrankings.com/college-football/stat/opponent-rushing-yards-per-game",
    "PD": "https://www.teamrankings.com/college-football/stat/opponent-passing-yards-per-game",
    "RO": "https://www.teamrankings.com/college-football/stat/rushing-yards-per-game",
    "PO": "https://www.teamrankings.com/college-football/stat/passing-yards-per-game",
    "SD": "https://www.teamrankings.com/college-football/stat/opponent-points-per-game",
    "SO": "https://www.teamrankings.com/college-football/stat/points-per-game",
    "TD": "https://www.teamrankings.com/college-football/stat/takeaways-per-game",
    "TO": "https://www.teamrankings.com/college-football/stat/giveaways-per-game",
    "ROF": "https://www.teamrankings.com/college-football/stat/rushing-yards-per-game?date=2024-01-09",
    "wp23": "https://www.teamrankings.com/ncf/trends/win_trends/?range=yearly_2023",
    "POF": "https://www.teamrankings.com/college-football/stat/passing-yards-per-game?date=2024-01-09",
    "RDF": "https://www.teamrankings.com/college-football/stat/opponent-rushing-yards-per-game?date=2024-01-09",
    "PDF": "https://www.teamrankings.com/college-football/stat/opponent-passing-yards-per-game?date=2024-01-09",
    "TOF": "https://www.teamrankings.com/college-football/stat/giveaways-per-game?date=2024-01-09",
    "TDF": "https://www.teamrankings.com/college-football/stat/takeaways-per-game?date=2024-01-09",
    "SOF": "https://www.teamrankings.com/college-football/stat/points-per-game?date=2024-01-09",
    "SDF": "https://www.teamrankings.com/college-football/stat/opponent-points-per-game?date=2024-01-09"
}


# Function to scrape data and clean it
def scrape_and_clean_data(url, file_name):
    response = requests.get(url)
    soup = bs(response.text, "html.parser")
    
    # Find the table and extract rows
    table = soup.find("table", {'class': 'tr-table'})
    rows = table.find_all('tr')
    
    data = []
    for row in rows:
        cells = row.find_all('td')
        if len(cells) > 0:  # Only include rows with data
            data.append([cell.text.strip() for cell in cells])
    
    # Create DataFrame, drop unwanted rows, and save to CSV
    df = pd.DataFrame(data)
    if df.shape[1] > 0:  # Assume first two columns are always the relevant ones
        df = df.iloc[:, [1, 2]]

    df.dropna(inplace=True)  # Drop any rows with missing values
    df = df.iloc[1:]  # Skip the first row if it's a duplicate header
    
    if file_name == "wp23":
        df = df.iloc[:, [0, 2]]

    df.to_csv(f"{file_name}.csv", index=False)
    return df

# Iterate over each URL, scrape data, clean it, and save to CSV
dfs = {}
for key, url in urls.items():
    dfs[key] = scrape_and_clean_data(url, f"{key}_Table")

# Ensure all DataFrames have the same number of rows by reindexing them
max_rows = max(df.shape[0] for df in dfs.values())  # Find the max row count

for key in dfs:
    dfs[key] = dfs[key].reindex(range(max_rows)).fillna("")

# Save the standardized CSVs
for key, df in dfs.items():
    df.to_csv(f"{key}_Table.csv", index=False)
