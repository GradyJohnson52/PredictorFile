from flask import Flask, request, jsonify, render_template
from flask_cors import CORS
import pandas as pd
import joblib
import os

app = Flask(__name__)
CORS(app)

BASE_DIR = os.path.dirname(os.path.abspath(__file__))

model = joblib.load('../trained_model.pkl')
scaler = joblib.load('../scaler.pkl')

# model_path = os.path.join(BASE_DIR, 'trained_model.pkl')
# with open(model_path, 'rb') as f:
#     model = joblib.load(f)

# scaler_path = os.path.join(BASE_DIR, 'scaler.pkl')
# with open(scaler_path, 'rb') as f:
#     scaler = joblib.load(f)

csv_path = os.path.join(BASE_DIR, 'stats.csv')
matchup_df = pd.read_csv(csv_path)

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
    team1 = data['team1']
    team2 = data['team2']
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

