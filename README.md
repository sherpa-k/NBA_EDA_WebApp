# NBA 22-23 Season Analyzing Web App

## Description 
End to end data analysis/visualization on NBA team statistics for the 2022-23 season using streamlit. After selecting a team, the program displays a team's offensive, defensive and net ratings along with the top individual performers of the team and other performance metrics.

![okc](examples/thunder.png)

## Getting started
Check out the site here:

https://sherpa-k-nba-eda-webapp-nba-webapp-9pb95p.streamlit.app/

#### Locally
Cloning the repo through terminal:

```https://github.com/sherpa-k/NBA_EDA_WebApp.git```


Move into project directory

```cd NBA_EDA_WebApp/```


Install required dependencies:


```pip install -r requirements.txt```


Run the program:

```streamlit run ./NBA_WebApp.py```


## Data
We used swar's ```nba_api``` to call data for player and team stats as well as team standings. Using BeautifulSoup we html parsed data from https://www.basketball-reference.com/ to generate advanced statistics on teams(offensive, defensive and net ratings, etc.)

We parsed team logos from https://loodibee.com/ and player headshots from https://www.nba.com/

## Additional Features (Future)
In the future I will be adding:
- a match predictor using Monte Carlo simulations
- a shot chart displaying a team/player's shooting performance


## Acknowledgements
- https://github.com/swar for deploying the nba_api

