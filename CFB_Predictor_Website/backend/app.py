from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
app = Flask(__name__)

model = joblib.load('trained_model.pkl')
scaler = joblib.load('scaler.pkl')
matchup_df = pd.read_csv('advanced_matchup_data.csv')

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

