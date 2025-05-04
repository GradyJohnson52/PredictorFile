from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib
import os

BASE_DIR = os.path.dirname(os.path.abspath(__file__))
ROOT_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", ".."))
FRONTEND_DIR = os.path.abspath(os.path.join(BASE_DIR, "..", "frontend"))

app = Flask(__name__, static_folder=os.path.join(FRONTEND_DIR, "static"), template_folder=FRONTEND_DIR)
CORS(app)

MODEL_PATH = os.path.join(ROOT_DIR, "trained_model.pkl")
SCALER_PATH = os.path.join(ROOT_DIR, "scaler.pkl")
CSV_PATH = os.path.join(ROOT_DIR, "advanced_matchup_data.csv")

with open(MODEL_PATH, "rb") as f:
    model = joblib.load(f)

with open(SCALER_PATH, 'rb') as f:
    scaler = joblib.load(f)

matchup_df = pd.read_csv(CSV_PATH)

team_mapping = {
    'Florida Intl': 'FIU',
    'Ohio St': 'Ohio State',
    'Iowa St': 'Iowa State',
    'Notre Dame': 'Notre Dame',
    'N Illinois': 'Northern Illinois',
    'Washington': 'Washington',
    'Texas': 'Texas',
    'LA Tech': 'Louisiana Tech',
    'Sam Hous St': 'Sam Houston State',
    'UL Monroe': 'Louisiana-Monroe',
    'Minnesota': 'Minnesota',
    'Indiana': 'Indiana',
    'Bowling Grn': 'Bowling Green',
    'Wisconsin': 'Wisconsin',
    'W Kentucky': 'Western Kentucky',
    'Tulane': 'Tulane',
    'Kentucky': 'Kentucky',
    'Rice': 'Rice',
    'Alabama': 'Alabama',
    'Oregon': 'Oregon',
    'BYU': 'Brigham Young',
    'Houston': 'Houston',
    'U Mass': 'Massachusetts',
    'UAB': 'Alabama-Birmingham',
    'Army': 'Army',
    'Temple': 'Temple',
    'Tennessee': 'Tennessee',
    'Penn St': 'Penn State',
    'Colorado': 'Colorado',
    'Miami (OH)': 'Miami (OH)',
    'Missouri': 'Missouri',
    'TX Christian': 'Texas Christian',
    'Louisiana': 'Louisiana',
    'Liberty': 'Liberty',
    'Air Force': 'Air Force',
    'Florida St': 'Florida State',
    'Nevada': 'Nevada',
    'Marshall': 'Marshall',
    'S Carolina': 'South Carolina',
    'Central Mich': 'Central Michigan',
    'Fresno St': 'Fresno State',
    'Georgia St': 'Georgia State',
    'Oklahoma': 'Oklahoma',
    'Iowa': 'Iowa',
    'James Mad': 'James Madison',
    'Toledo': 'Toledo',
    'Utah': 'Utah',
    'Charlotte': 'Charlotte',
    'Oregon St': 'Oregon State',
    'Texas St': 'Texas State',
    'Navy': 'Navy',
    'Auburn': 'Auburn',
    'Georgia': 'Georgia',
    'Michigan St': 'Michigan State',
    'Troy': 'Troy',
    'VA Tech': 'Virginia Tech',
    'Jksnville St': 'Jacksonville State',
    'Michigan': 'Michigan',
    'Ohio': 'Ohio',
    'Connecticut': 'Connecticut',
    'S Mississippi': 'Southern Mississippi',
    'Miami': 'Miami',
    'Cincinnati': 'Cincinnati',
    'Nebraska': 'Nebraska',
    'Duke': 'Duke',
    'Clemson': 'Clemson',
    'San Diego St': 'San Diego State',
    'App State': 'Appalachian State',
    'Hawaii': 'Hawaii',
    'Arizona St': 'Arizona State',
    'California': 'California',
    'Wyoming': 'Wyoming',
    'UCF': 'Central Florida',
    'Syracuse': 'Syracuse',
    'LSU': 'LSU',
    'E Michigan': 'Eastern Michigan',
    'Illinois': 'Illinois',
    'GA Tech': 'Georgia Tech',
    'W Michigan': 'Western Michigan',
    'Coastal Car': 'Coastal Carolina',
    'TX El Paso': 'Texas-El Paso (UTEP)',
    'NC State': 'North Carolina State',
    'S Methodist': 'Southern Methodist',
    'Florida': 'Florida',
    'Kansas St': 'Kansas State',
    'USC': 'Southern California',
    'UNLV': 'Nevada-Las Vegas',
    'San Jose St': 'San Jose State',
    'Northwestern': 'Northwestern',
    'N Carolina': 'North Carolina',
    'Mississippi': 'Mississippi',
    'Old Dominion': 'Old Dominion',
    'Colorado St': 'Colorado State',
    'Akron': 'Akron',
    'Rutgers': 'Rutgers',
    'Texas A&M': 'Texas A&M',
    'Fla Atlantic': 'Florida Atlantic',
    'UCLA': 'UCLA',
    'Miss State': 'Mississippi State',
    'Baylor': 'Baylor',
    'Kennesaw St': 'Kennesaw State',
    'N Mex State': 'New Mexico State',
    'E Carolina': 'East Carolina',
    'Maryland': 'Maryland',
    'Kansas': 'Kansas',
    'Louisville': 'Louisville',
    'Boise St': 'Boise State',
    'Middle Tenn': 'Middle Tennessee State',
    'Buffalo': 'Buffalo',
    'Arizona': 'Arizona',
    'Vanderbilt': 'Vanderbilt',
    'Arkansas St': 'Arkansas State',
    'S Alabama': 'South Alabama',
    'Kent St': 'Kent State',
    'Arkansas': 'Arkansas',
    'Utah St': 'Utah State',
    'Boston Col': 'Boston College',
    'GA Southern': 'Georgia Southern',
    'Pittsburgh': 'Pittsburgh',
    'W Virginia': 'West Virginia',
    'Memphis': 'Memphis',
    'Purdue': 'Purdue',
    'North Texas': 'North Texas',
    'Wash State': 'Washington State',
    'Virginia': 'Virginia',
    'UTSA': 'Texas-San Antonio (UTSA)',
    'Ball St': 'Ball State',
    'New Mexico': 'New Mexico',
    'Stanford': 'Stanford',
    'Oklahoma St': 'Oklahoma State',
    'Wake Forest': 'Wake Forest',
    'Texas Tech': 'Texas Tech',
    'S Florida': 'South Florida',
    'Tulsa': 'Tulsa'
}

def standardize_team_name(team_name):
    return team_mapping.get(team_name, team_name)

@app.route('/')
def home():
    try:
        # Your existing logic here, like rendering a template or loading data
        return render_template("index.html")  # or however your route works
    except Exception as e:
        import traceback
        print("ERROR:", e)
        traceback.print_exc()
        return f"Internal Server Error: {e}", 500

@app.route('/predict', methods=['POST'])
def predict():
    data = request.json
    team1 = standardize_team_name(data['team1'])
    team2 = standardize_team_name(data['team2'])
    week = int(data['week'])

    matchup = matchup_df[
        ((matchup_df['team1'] == team1) & (matchup_df['team2'] == team2) & (matchup_df['week'] == week)) |
        ((matchup_df['team1'] == team2) & (matchup_df['team2'] == team1) & (matchup_df['week'] == week))
    ]

    if matchup.empty:
        return jsonify({'error': 'Matchup not found'}), 404

    row = matchup.iloc[0]
    feature_cols = [
        'rush_adv_team1', 'rush_adv_team2', 'pass_adv_team1', 'pass_adv_team2',
        'score_adv_team1', 'score_adv_team2', 'turnover_adv_team1', 'turnover_adv_team2',
        'pred_rank_team1', 'pred_rank_team2', 'sos_team1', 'sos_team2', 'week'
    ]
    X = scaler.transform([row[feature_cols].values])
    prediction = model.predict(X)[0]
    proba = model.predict_proba(X)[0]
    winner = team1 if prediction == 1 else team2
    confidence = float(proba[prediction])

    return jsonify({'winner': winner, 'confidence': confidence})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.environ.get('PORT', 5000)))

