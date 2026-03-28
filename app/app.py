import streamlit as st
import joblib
import pandas as pd

teams = [
    'Sunrisers Hyderabad', 
    'Royal Challengers Bangalore',
    'Kolkata Knight Riders',
    'Kings XI Punjab',
    'Delhi Capitals',              
    'Mumbai Indians',
    'Chennai Super Kings',
    'Rajasthan Royals',
    'Gujarat Titans', 
    'Lucknow Super Giants'
]

cities = [
    'Hyderabad','Bangalore','Mumbai','Indore','Kolkata','Delhi',
    'Chandigarh','Jaipur','Chennai','Cape Town','Port Elizabeth',
    'Durban','Centurion','East London','Johannesburg','Kimberley',
    'Bloemfontein','Ahmedabad','Cuttack','Nagpur','Dharamsala',
    'Visakhapatnam','Pune','Raipur','Ranchi','Abu Dhabi',
    'Sharjah','Mohali','Bengaluru'
]

pipe = joblib.load('model/model.pkl')

st.title("🏏 IPL Win Predictor")

col1, col2 = st.columns(2)

with col1:
    batting_team = st.selectbox("Select Batting Team", sorted(teams))

with col2:
    bowling_team = st.selectbox("Select Bowling Team", sorted(teams))

selected_city = st.selectbox("Select Host City", sorted(cities))

target = st.number_input("Target", min_value=0)

col3, col4, col5 = st.columns(3)

with col3:
    score = st.number_input("Score", min_value=0)


with col4:
    overs_completed = st.number_input("Overs", min_value=0, max_value=20, step=1)

with col5:
    balls_in_over = st.number_input("Balls (0-5)", min_value=0, max_value=5, step=1)

wickets = st.number_input("Wickets Out", min_value=0, max_value=10)


if st.button("Predict Probability"):

    # Total balls bowled
    total_balls_bowled = overs_completed * 6 + balls_in_over

    if total_balls_bowled == 0:
        st.error("Overs must be greater than 0!")
        st.stop()

    # Remaining calculations
    runs_left = target - score
    ball_left = 120 - total_balls_bowled
    wickets_left = 10 - wickets

    if ball_left <= 0:
        st.error("Match already completed!")
        st.stop()

    # Run rates
    crr = (score * 6) / total_balls_bowled
    rrr = (runs_left * 6) / ball_left

    input_df = pd.DataFrame({
        "batting_team": [batting_team],
        "bowling_team": [bowling_team],
        "city": [selected_city],
        "runs_left": [runs_left],
        "ball_left": [ball_left],
        "wickets_left": [wickets_left],
        "crr": [crr],
        "rrr": [rrr],
        "total_runs_x": [target]
    })

    # Prediction
    result = pipe.predict_proba(input_df)
    loss = result[0][0]
    win = result[0][1]

    
    st.subheader("📊 Win Probability")

    st.success(f"{batting_team}: {round(win * 100)}%")
    st.error(f"{bowling_team}: {round(loss * 100)}%")

    st.info(f"""
    🏏 Match Situation:
    - Runs Left: {runs_left}
    - Balls Left: {ball_left}
    - Current Run Rate: {round(crr, 2)}
    - Required Run Rate: {round(rrr, 2)}
    """)