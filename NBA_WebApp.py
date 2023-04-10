import streamlit as st
import pandas as pd
import io
import requests
from num2words import num2words
from PIL import Image

st.set_page_config(layout="wide")


# Import DFs
player_df = pd.read_csv(r"Player_stats.csv")
team_df = pd.read_csv(r"Team-stats.csv")
standings = pd.read_csv('Standings.csv')
advanced_df = pd.read_csv('advanced_stats.csv')


# Get Metrics
def get_metrics(team):
    record = standings.loc[standings['TEAM_NAME'] == team, 'Record'].values[0]
    home = standings.loc[standings['TEAM_NAME'] == team, 'HOME'].values[0]
    road = standings.loc[standings['TEAM_NAME'] == team, 'ROAD'].values[0]
    return record, home, road


def get_advanced_metrics1(team):
    ortg = advanced_df.loc[advanced_df['Team'] == team, 'ORtg'].values[0]
    ortg_rank = advanced_df.loc[advanced_df['Team'] == team, 'Orank'].values[0]

    drtg = advanced_df.loc[advanced_df['Team'] == team, 'DRtg'].values[0]
    drtg_rank = advanced_df.loc[advanced_df['Team'] == team, 'Drank'].values[0]
    nrtg = ortg - drtg
    if nrtg > 0:
        nrtg = "+" + str(round(nrtg, 2))
    elif nrtg == 0:
        nrtg = 0
    else:
        nrtg = str(round(nrtg, 2))

    nrtg_rank = advanced_df.loc[advanced_df['Team'] == team, 'Nrank'].values[0]
    return ortg, drtg, nrtg, ortg_rank, drtg_rank, nrtg_rank


def get_advanced_metrics2(team):
    pace = advanced_df.loc[advanced_df['Team'] == team, 'Pace'].values[0]
    pace_rank = advanced_df.loc[advanced_df['Team'] == team, 'PaceRank'].values[0]

    fg_pct = team_df.loc[team_df['TEAM_NAME'] == team, 'FG_PCT'].values[0]
    fg_pct = f'{fg_pct}%'
    fg_pct_rank = team_df.loc[team_df['TEAM_NAME'] == team, 'FG_PCT_RANK'].values[0]

    fg3_pct = team_df.loc[team_df['TEAM_NAME'] == team, 'FG3_PCT'].values[0]
    fg3_pct = f'{fg3_pct}%'
    fg3_pct_rank = team_df.loc[team_df['TEAM_NAME'] == team, 'FG3_PCT_RANK'].values[0]

    return pace, pace_rank, fg_pct, fg_pct_rank, fg3_pct, fg3_pct_rank



def team_leaders(team):
    t_id = standings.loc[standings['TEAM_NAME'] == team, 'TeamID'].values[0]
    by_team = player_df.loc[player_df['TEAM_ID'] == t_id]
    by_points = by_team.sort_values(by= 'PPG', ascending=False)
    points = by_points['PPG'].iloc[0]
    points_name = by_points['PLAYER_NAME'].iloc[0]
    by_assists = by_team.sort_values(by= 'APG', ascending=False)
    ast = by_assists['APG'].iloc[0]
    ast_name = by_assists['PLAYER_NAME'].iloc[0]
    by_rebounds = by_team.sort_values(by= 'RPG', ascending=False)
    reb = by_rebounds['RPG'].iloc[0]
    reb_name = by_rebounds['PLAYER_NAME'].iloc[0]

    return points_name, points, ast_name, ast, reb_name, reb


def get_player_pic(player):
    pid = player_df.loc[player_df['PLAYER_NAME'] == player, "PLAYER_ID"].values[0]
    r = requests.get(f'https://cdn.nba.com/headshots/nba/latest/1040x760/{pid}.png')
    img_file = io.BytesIO(r.content)
    image = Image.open(img_file)

    return image




### Title ###
st.markdown('<h1 style="text-align: center; color:red;"><u>NBA 2022-23 Season Team Analysis</u></h1>',
                unsafe_allow_html=True)


# User Input
st.sidebar.header("Team Selection")
input_team = st.sidebar.selectbox("Please select the team to analyze", team_df['TEAM_NAME'].tolist())


### Team Logo and Rank ###
with st.container():
    if st.sidebar.button('Search'):
        st.markdown(f'<h1 style="text-align: center;">{input_team}</h1>',
                    unsafe_allow_html=True)

        with st.container():
            c1, c2 = st.columns(2)
            with c1:
                col1, col2, col3 = st.columns(3)
                with col2:
                    img = Image.open(f"logos/{input_team}.png")
                    st.image(img, width=270)

            with c2:
                rank = standings.loc[standings['TEAM_NAME'] == input_team, "PlayoffRank"].values[0]
                rank_word = num2words(int(rank), to='ordinal_num')
                side = standings.loc[standings['TEAM_NAME'] == input_team, "Conference"].values[0]
                # Add empty rows to align with team logo
                st.write("")
                st.write("")

                if rank <= 6:
                    st.markdown(f'<h1 style="text-align: center; color:green;">{rank_word} in the {side}</h1>',
                                unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center; color:green;">In Playoff Contention</p>',
                                unsafe_allow_html=True)

                elif rank > 10:
                    st.markdown(f'<h1 style="text-align: center; color:red;">{rank_word} in the {side}</h1>',
                                unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center; color:red;">Out of the Playoffs</p>',
                                unsafe_allow_html=True)
                else:
                    st.markdown(f'<h1 style="text-align: center; color:blue;">{rank_word} in the {side}</h1>',
                                unsafe_allow_html=True)
                    st.markdown(f'<p style="text-align: center; color:blue;">In the Play-ins</p>',
                                unsafe_allow_html=True)



            ### Metrics ###
            c1, c2, c3 = get_metrics(input_team)
            offrtg, defrtg, netrtg, orank, drank, nrank = get_advanced_metrics1(input_team)
            pace, pace_rank, fg_p, fg_prank, fg3_p, fg_3prank = get_advanced_metrics2(input_team)
            col1, col2= st.columns(2)

            ### Team Stats ###
            with col1:
                col1a, col1b, col1c = st.columns(3)
                with col1a:
                    st.markdown('<h6 style="text-align: center;">Record</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{c1}</h4>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">Offensive Rating</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{offrtg}</h4>',
                                unsafe_allow_html=True)
                    orank = num2words(int(orank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{orank}</p>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">Pace</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{pace}</h4>',
                                unsafe_allow_html=True)
                    pace_rank = num2words(int(pace_rank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{pace_rank}</p>',
                                unsafe_allow_html=True)




                with col1b:
                    st.markdown('<h6 style="text-align: center;">At Home</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{c2}</h4>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">Defensive Rating</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{defrtg}</h4>',
                                unsafe_allow_html=True)
                    drank = num2words(int(drank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{drank}</p>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">FG %</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{fg_p}</h4>',
                                unsafe_allow_html=True)
                    fg_prank = num2words(int(fg_prank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{fg_prank}</p>',
                                unsafe_allow_html=True)



                with col1c:
                    st.markdown('<h6 style="text-align: center;">On the Road</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{c3}</h4>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">Net Rating</h6>',
                                unsafe_allow_html=True)
                    if "+" in netrtg:
                        st.markdown(f'<h4 style="text-align: center; color: green;">{netrtg}</h4>',
                                    unsafe_allow_html=True)
                    elif "-" in netrtg:
                        st.markdown(f'<h4 style="text-align: center; color: red;">{netrtg}</h4>',
                                    unsafe_allow_html=True)
                    else:
                        st.markdown(f'<h4 style="text-align: center;">{netrtg}</h4>',
                                    unsafe_allow_html=True)

                    nrank = num2words(int(nrank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{nrank}</p>',
                                unsafe_allow_html=True)
                    st.write("-" * 15)
                    st.markdown('<h6 style="text-align: center;">3pt FG %</h6>',
                                unsafe_allow_html=True)
                    st.markdown(f'<h4 style="text-align: center;">{fg3_p}</h4>',
                                unsafe_allow_html=True)
                    fg_3prank = num2words(int(fg_3prank), to='ordinal_num')
                    st.markdown(f'<p style="text-align: center;">{fg_3prank}</p>',
                                unsafe_allow_html=True)


                    ### Team Leaders ###
            with col2:
                with st.container():
                    st.markdown('<h2 style="text-align: center;"><u>Team Leaders</u></h2>',
                                unsafe_allow_html=True)
                    st.write("")
                    st.write("")
                    pname, ppg, aname, apg, rname, rpg = team_leaders(input_team)

                    col2a, col2b, col2c = st.columns(3)
                    with col2a:
                        st.markdown('<h3 style="text-align: center;">PPG</h3>',
                                        unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{pname}</h5>',
                                        unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{round(ppg,1)}</h5>',
                                        unsafe_allow_html=True)
                        img = get_player_pic(pname)
                        st.image(img, width=265)


                    with col2b:
                        st.markdown('<h3 style="text-align: center;">APG</h3>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{aname}</h5>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{round(apg, 1)}</h5>',
                                    unsafe_allow_html=True)
                        img = get_player_pic(aname)
                        st.image(img, width=265)


                    with col2c:
                        st.markdown('<h3 style="text-align: center;">RPG</h3>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{rname}</h5>',
                                    unsafe_allow_html=True)
                        st.markdown(f'<h5 style="text-align: center;">{round(rpg, 1)}</h5>',
                                    unsafe_allow_html=True)
                        img = get_player_pic(rname)
                        st.image(img, width=265)