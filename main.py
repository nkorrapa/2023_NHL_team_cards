import streamlit as st
import time
import pandas as pd
import plotly.graph_objects as go
import plotly.express as px
# use container width = true
## functions
st.set_page_config(page_title="2023 Team Scorecard", layout="wide")
@st.cache_data()
def load_file(file):
    time.sleep(3)
    if file is not None:
        df = pd.read_csv(file)
    else:
        df = pd.read_csv(file)
    return(df)

def get_roster(df):
    #goals
    team_goals = df[df['event_type']== 'GOAL']
    team_goals = team_goals.groupby('event_player_1_name', as_index=False).count()
    team_goals = team_goals[['event_player_1_name','event']]
    team_goals.columns = ['Player', 'Goals']
    #assists
    team_assists_1 = df[(df['event_type'].values == 'GOAL') & (df['event_player_2_type'].values == 'Assist')]
    team_assists_2 = df[(df['event_type'].values == 'GOAL') & (df['event_player_3_type'].values == 'Assist')]
    team_assists_1 = team_assists_1.groupby('event_player_2_name', as_index=False).count()
    team_assists_2 = team_assists_2.groupby('event_player_3_name', as_index=False).count()
    team_assists_1 = team_assists_1[['event_player_2_name','event']]
    team_assists_2 = team_assists_2[['event_player_3_name','event']]
    team_assists_1.columns = ['Player', 'Assists']
    team_assists_2.columns = ['Player', 'Assists']
    #combine
    roster = team_goals.merge(team_assists_1, on = 'Player', how='outer')
    roster = roster.merge(team_assists_2, on='Player', how='outer')
    roster = roster.fillna(0)
    roster['Assists'] = roster['Assists_x'] + roster['Assists_y']
    roster = roster.drop(columns=['Assists_x', 'Assists_y'])
    return(roster)

## Load data
teams = load_file("data/teams.csv")
pbp = load_file("data/2023pbpfull.csv")


st.title("2023 NHL Team Cards")

team = st.sidebar.selectbox("Pick a NHL Team", teams['event_team'].tolist())

team_teams = teams[teams['event_team']== team]
team_pbp = pbp[pbp.event_team == team]
arena = "Home Arena: " + team_teams['home_arena'].values[0]

record = str(team_teams['W'].values[0]) + "-" + str(team_teams['L'].values[0]) + "-" + str(team_teams['OT'].values[0])

team_pbp_ev = pbp[(pbp['event_team'] == team) & (pbp['strength_code'] == 'EV')]
team_pbp_pp = pbp[(pbp['event_team'] == team) & (pbp['strength_code'] == 'PP')]
team_pbp_pk = pbp[(pbp['event_team'] == team) & (pbp['strength_code'] == 'SH')]
### DATA MANIP
## ALL
team_roster = get_roster(team_pbp)

goals_10 = team_roster.sort_values(by = ['Goals'], ascending=False).head(10)

goals_10_bar= px.bar(goals_10, x='Player', y='Goals', title= "Goals")

assists_10 = team_roster.sort_values(by = ['Assists'], ascending=False).head(10)

assists_10_bar = px.bar(assists_10, x = 'Player', y = 'Assists', title = "Assists")

# sankey

## EV
team_roster_ev = get_roster(team_pbp_ev)

goals_10_ev = team_roster_ev.sort_values(by = ['Goals'], ascending=False).head(10)

goals_10_ev_bar= px.bar(goals_10_ev, x='Player', y='Goals', title= "Goals")

assists_10_ev = team_roster_ev.sort_values(by = ['Assists'], ascending=False).head(10)

assists_10_ev_bar = px.bar(assists_10_ev, x = 'Player', y = 'Assists', title = "Assists")

# Sankey

## PP

team_roster_pp = get_roster(team_pbp_pp)

goals_10_pp = team_roster_pp.sort_values(by = ['Goals'], ascending=False).head(10)

goals_10_pp_bar= px.bar(goals_10_pp, x='Player', y='Goals', title= "Goals")

assists_10_pp = team_roster_pp.sort_values(by = ['Assists'], ascending=False).head(10)

assists_10_pp_bar = px.bar(assists_10_pp, x = 'Player', y = 'Assists', title = "Assists")

# Sankey

## PK

team_roster_pk = get_roster(team_pbp_pk)

goals_10_pk = team_roster_pk.sort_values(by = ['Goals'], ascending=False).head(10)

goals_10_pk_bar= px.bar(goals_10_pk, x='Player', y='Goals', title= "Goals")

assists_10_pk = team_roster_pk.sort_values(by = ['Assists'], ascending=False).head(10)

assists_10_pk_bar = px.bar(assists_10_pk, x = 'Player', y = 'Assists', title = "Assists")

# SANKEY


### BODY
st.write('## ' + 'Team: ', team)
st.write('#### ' + arena)
st.write('Conference: ', team_teams['conference'].values[0])
st.write('Division: ', team_teams['division'].values[0])

st.divider()

with st.container():
    col1, col2 = st.columns(2)
    with col1:
        st.write("Record: ", record)
        st.write("Total Points: ", str(team_teams['Points'].values[0]))
        st.write("PP%:  ", str(team_teams['PP%'].values[0]), "%")
        st.write("PK%:  ", str(team_teams['PK%'].values[0]), "%")
    
    with col2: 
        st.write("Rank")
        st.write("League: ", str(team_teams['league_rank'].values[0]))
        st.write("Conference: ", str(team_teams['conference_rank'].values[0]))
        st.write("Division: ", str(team_teams['division_rank'].values[0]))

st.divider()
with st.container():
    col1, col2 = st.columns(2)
    with col1:
      st.subheader("Roster Points")
    with st.container():
       st.dataframe(team_roster, hide_index=True, width=400)
    with col2:
        st.write("Team shooting % (INSERT PIE CHART HERE)") # TODO: add pie chart
st.divider()

st.subheader("Top 10 Overall Scoring")
with st.container():
    tab1, tab2 = st.tabs(["Goals", "Assists"])
    with tab1:
      st.plotly_chart(goals_10_bar, use_container_width=True)
    with tab2: 
        st.plotly_chart(assists_10_bar, use_container_width=True)
    st.divider()
    st.subheader("Scoring Flow")
    st.write("Add Sankey here") # TODO: Add sankey chart
st.divider()

st.subheader("Scoring - by Strength State")
with st.container(): 
    tab1, tab2, tab3 = st.tabs(["Even Strength", "Power Play", "Shorthanded"])
    with tab1:
      with st.container():
        col1, col2 = st.columns(2)
        with col1: 
          st.plotly_chart(goals_10_ev_bar, use_container_width=True)
        with col2:
          st.plotly_chart(assists_10_ev_bar, use_container_width=True)      
      st.write("Add Sankey here")
    with tab2:
      with st.container():
        col1, col2 = st.columns(2)
        with col1: 
          st.plotly_chart(goals_10_pp_bar, use_container_width=True)
        with col2:
          st.plotly_chart(assists_10_pp_bar, use_container_width=True)
      st.write("Add Sankey here")        
    with tab3:
      with st.container(): 
        col1, col2 = st.columns(2)
        with col1: 
          st.plotly_chart(goals_10_pk_bar, use_container_width=True)
        with col2:
          st.plotly_chart(assists_10_pk_bar, use_container_width=True)  
      st.write("Add sankey here")     

