import aiohttp
import asyncio
import sqlite3
from bs4 import BeautifulSoup

# SQLite database setup to store team data
db_conn = sqlite3.connect('team_stats.db')
db_cursor = db_conn.cursor()

# Create table if it doesn't exist
db_cursor.execute('''CREATE TABLE IF NOT EXISTS team_stats (
                        team TEXT PRIMARY KEY,
                        rush_off REAL,
                        rush_def REAL,
                        pass_off REAL,
                        pass_def REAL,
                        score_off REAL,
                        score_def REAL,
                        win_pct REAL)''')
db_conn.commit()

# Function to scrape data asynchronously
async def fetch_data(url, stat_name, session):
    async with session.get(url) as response:
        html_content = await response.text()
        soup = BeautifulSoup(html_content, 'html.parser')

        # Find the right table, assuming it has the class 'datatable'
        table = soup.find('table', {'class': 'datatable'})
        if table is None:
            print(f"Warning: No table found at {url}")
            return {stat_name: []}  # Return an empty result for this stat

        rows = table.find_all('tr')[1:]  # Skip header row
        team_data = []
        for row in rows:
            columns = row.find_all('td')
            team_name = columns[0].text.strip()  # Keep team name as a string

            # Attempt to convert the stat value to a float, skip if not possible
            try:
                stat_value = float(columns[1].text.strip().replace(',', ''))  # Handle commas in numbers
            except ValueError:
                print(f"Skipping invalid stat value for team: {team_name}")
                continue

            team_data.append((team_name, stat_value))

        return {stat_name: team_data}

# Function to store scraped data into SQLite database
def store_team_data(data_dict):
    for stat_name, data in data_dict.items():
        for team_name, value in data:
            db_cursor.execute(f"INSERT OR IGNORE INTO team_stats (team) VALUES (?)", (team_name,))
            db_cursor.execute(f"UPDATE team_stats SET {stat_name} = ? WHERE team = ?", (value, team_name))
    db_conn.commit()

# Main asynchronous function to scrape all URLs
async def scrape_all_data():
    urls = {
        'rush_off': "https://www.teamrankings.com/college-football/stat/rushing-yards-per-game",
        'rush_def': "https://www.teamrankings.com/college-football/stat/opponent-rushing-yards-per-game",
        'pass_off': "https://www.teamrankings.com/college-football/stat/passing-yards-per-game",
        'pass_def': "https://www.teamrankings.com/college-football/stat/opponent-passing-yards-per-game",
        'score_off': "https://www.teamrankings.com/college-football/stat/points-per-game",
        'score_def': "https://www.teamrankings.com/college-football/stat/opponent-points-per-game",
        'win_pct': "https://www.teamrankings.com/college-football/stat/win-percentage"
    }

    async with aiohttp.ClientSession() as session:
        tasks = []
        for stat_name, url in urls.items():
            tasks.append(fetch_data(url, stat_name, session))

        results = await asyncio.gather(*tasks)

        # Flatten the results and store them in the database
        data_dict = {key: value for result in results for key, value in result.items()}
        store_team_data(data_dict)

# Running the async scraper
if __name__ == "__main__":
    loop = asyncio.get_event_loop()
    loop.run_until_complete(scrape_all_data())
    print("Data scraping completed and stored in team_stats.db")




def view_db_data(db_file):
    conn = sqlite3.connect(db_file)
    cursor = conn.cursor()

    # Get the list of all tables
    cursor.execute("SELECT name FROM sqlite_master WHERE type='table';")
    tables = cursor.fetchall()

    if len(tables) == 0:
        print("No tables found in the database.")
        return

    for table in tables:
        table_name = table[0]
        print(f"\nData from table: {table_name}")
        
        # Fetch column names to better understand the structure
        cursor.execute(f"PRAGMA table_info({table_name});")
        columns = cursor.fetchall()
        column_names = [col[1] for col in columns]  # Extracting column names
        print(f"Columns: {column_names}")
        
        # Query all rows from the table
        cursor.execute(f"SELECT * FROM {table_name};")
        rows = cursor.fetchall()

        if len(rows) == 0:
            print(f"No data found in table: {table_name}")
        else:
            # Print each row in the table
            for row in rows:
                print(row)

    conn.close()

# Path to your database file
db_file = 'team_stats.db'  # Replace with the correct path
view_db_data(db_file)