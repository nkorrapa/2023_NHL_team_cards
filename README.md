# 2023 NHL Team Cards
## Streamlit
[![Open in Streamlit](https://static.streamlit.io/badges/streamlit_badge_black_white.svg)](https://2023nhlcards.streamlit.app/)

## Introduction

This app provides basic information on a NHL team's scoring for the 2022-2023 NHL season.

Metrics shown
- Goals
- Assists
- Team Shooting %
- Scoring Flow

The scoring metrics are shown for the top 10 players at each strength state.


## The Data

The play by play data was pulled from the NHL's play by play API, and the overall NHL team data was pulled from the NHL website statistics page. The play by play data was then modified to remove uneccesary columns, in order to reduce the size of the file.

## Future Work

Some future work that can be done is updating the app so that it pulls live NHL data from the API, instead of stored data.