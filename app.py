import time
import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt
import altair as alt

# read in pbp.csv

@st.cache_data()
def load_file(file):
    time.sleep(3)
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(file)
    return(df)

pbp= load_file("data/2023pbp.csv")

teams = load_file("data/teams.csv")

st.header("NHL Team Cards")

team_name = st.selectbox("Pick a NHL Team", teams['event_team'].tolist())

team_df = pbp[pbp.event_team == team_name]

# Place in league, division, conference

# points, pp%, pk%, record

# Top 5 in goals, assists, points -> PP, EV, PK

goals = team_df[team_df.event_type == 'GOAL']

goals = goals.groupby('event_player_1_name', as_index=False).count()
goals = pd.DataFrame(goals)
goals = goals[['event_player_1_name','event']]

# top 2 PP units
# top 2 PK units
