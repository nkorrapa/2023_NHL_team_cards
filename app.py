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

pbp= load_file("2023pbp.csv")

teams = load_file("teams.csv")

st.header("NHL Team Cards")

team_name = st.selectbox("Pick a NHL Team", teams['event_team'].tolist())

team_df = pbp[pbp.event_team == team_name]

# goals pie chart

goals = team_df[team_df.event_type == 'GOAL']

goals = goals.groupby('event_player_1_name', as_index=False).count()
goals = pd.DataFrame(goals)
goals = goals[['event_player_1_name','event']]

#pie = plt.pie(goals.event , labels = goals.event_player_1_name)

st.write("Goals")
#st.write(goals)

#st.pyplot(pie.get_figure())

chart = alt.Chart(goals).mark_arc().encode(
    theta="event",
    color="event_player_1_name"
)
st.altair_chart(chart)

#st.write("Pick a '{{ team }}' player")

