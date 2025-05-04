import pandas as pd
import joblib

from sklearn.metrics import accuracy_score

# Load the processed matchup data
matchup_df = pd.read_csv('advanced_matchup_data.csv')

# Load the trained model
best_model = joblib.load('trained_model.pkl')
scaler = joblib.load('scaler.pkl')

# Prediction function
def predict_winner(team1_name, team2_name, week):
    matchup = matchup_df[
        ((matchup_df['team1'] == team1_name) & (matchup_df['team2'] == team2_name) & (matchup_df['week'] == week)) |
        ((matchup_df['team1'] == team2_name) & (matchup_df['team2'] == team1_name) & (matchup_df['week'] == week))
    ]
    
    if matchup.empty:
        print(f"No matchup data found for {team1_name} and {team2_name} for week {week}.")
        return

    if len(matchup) > 1:
        print("Multiple matchups found for these teams. Please check the dataset.")
        return

    matchup = matchup.iloc[0]
    print(matchup)
    feature_cols = [
        'rush_adv_team1', 'rush_adv_team2', 'pass_adv_team1', 'pass_adv_team2',
        'score_adv_team1', 'score_adv_team2', 'turnover_adv_team1', 'turnover_adv_team2',
        'pred_rank_team1', 'pred_rank_team2', 'sos_team1', 'sos_team2', 'week'
        ]

    features = matchup.drop(columns=['team1', 'team2'])

    feature_vector = matchup[feature_cols].values.reshape(1, -1)
    scaled_vector = scaler.transform(feature_vector)
    prediction = best_model.predict(scaled_vector)[0]
    proba = best_model.predict_proba(scaled_vector)[0]

    predicted_winner = team1_name if prediction == 1 else team2_name
    confidence = proba[prediction]

    print(f"Predicted winner: {predicted_winner} (Confidence: {confidence:.2%})")

# Take user input
team1_name = input("Enter the name of the first team: ")
team2_name = input("Enter the name of the second team: ")
week = int(input("Enter the week number: "))

# Predict
predict_winner(team1_name, team2_name, week)
