import streamlit as st
import time
import pandas as pd

## functions
@st.cache_data()
def load_file(file):
    time.sleep(3)
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(file)
    return(df)

## Load data
teams = load_file("data/teams.csv")

st.title("NHL Team Cards")

team = st.sidebar.selectbox("Pick a NHL Team", teams['event_team'].tolist())

team_teams = teams[teams['event_team']== team]

arena = "Home Arena: " + team_teams['home_arena'].values[0]

st.write('## ' + team)
st.write('#### ' + arena)

st.divider()

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.write("Record: TODO")
        st.write("PP%: TODO")
        st.write("PK%: TODO")
    
    with col2: 
        st.write("Rank")
        st.write("League: TODO ")
        st.write("Conference: TODO ")
        st.write("Division: TODO ")

st.divider()

st.subheader("Scoring")
with st.container():
    tab1, tab2, tab3 = st.tabs(["Even Strength", "Power Play", "Shorthanded"])
    with tab1:
        st.text("top 5 goals")
    with tab2:
        st.text("top 5 goals")
    with tab3:
        st.text("top 5 goals")