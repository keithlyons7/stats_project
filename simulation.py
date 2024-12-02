import numpy as np
import pandas as pd
import plotly.express as px


team_data = pd.read_csv("premStats24_25.csv")
fixture_data = pd.read_csv("fixtures.csv")
team_data.columns = team_data.columns.str.strip()
fixture_data.columns = fixture_data.columns.str.strip()


team_data["Offensive Strength"] = team_data["Goals Scored"] / team_data["Games Played"]
team_data["Defensive Strength"] = team_data["Goals Conceded"] / team_data["Games Played"]


team_data["Adjusted Possession"] = (team_data["Possession (%)"] * team_data["Passing Accuracy (%)"]) / 100


team_data["Discipline Risk"] = (team_data["Yellow Cards"] / team_data["Games Played"]) + \
                               (2 * team_data["Red Cards"] / team_data["Games Played"])

def simulate_match(home_stats, away_stats):
    home_lambda = home_stats["xG"] * (home_stats["Offensive Strength"] / away_stats["Defensive Strength"])
    away_lambda = away_stats["xG"] * (away_stats["Offensive Strength"] / home_stats["Defensive Strength"])
    
    home_lambda *= home_stats["Adjusted Possession"] / 100
    away_lambda *= away_stats["Adjusted Possession"] / 100
    
    home_lambda *= (home_stats["Shots on Target"] / home_stats["xG"])
    away_lambda *= (away_stats["Shots on Target"] / away_stats["xG"])
    
    home_discipline_factor = 1 - home_stats["Discipline Risk"]
    away_discipline_factor = 1 - away_stats["Discipline Risk"]
    
    home_goals = np.random.poisson(home_lambda * home_discipline_factor)
    away_goals = np.random.poisson(away_lambda * away_discipline_factor)
    
    if home_goals > away_goals:
        return home_goals, away_goals, "Home Win"
    elif away_goals > home_goals:
        return home_goals, away_goals, "Away Win"
    else:
        return home_goals, away_goals, "Draw"

def simulate_league(teams, fixtures):
    standings = teams.copy()
    standings["Points"] = 0
    standings["Games Won"] = 0
    standings["Games Drawn"] = 0
    standings["Games Lost"] = 0
    standings["Goals Scored Simulated"] = 0
    standings["Goals Conceded Simulated"] = 0
    standings["Clean Sheets"] = 0

    for _, match in fixtures.iterrows():
        home_team = match["HomeTeam"]
        away_team = match["AwayTeam"]
        home_stats = standings[standings["Teams"] == home_team].iloc[0]
        away_stats = standings[standings["Teams"] == away_team].iloc[0]
        home_goals, away_goals, result = simulate_match(home_stats, away_stats)
        standings.loc[standings["Teams"] == home_team, "Goals Scored Simulated"] += home_goals
        standings.loc[standings["Teams"] == away_team, "Goals Scored Simulated"] += away_goals
        standings.loc[standings["Teams"] == home_team, "Goals Conceded Simulated"] += away_goals
        standings.loc[standings["Teams"] == away_team, "Goals Conceded Simulated"] += home_goals
        if away_goals == 0:
            standings.loc[standings["Teams"] == home_team, "Clean Sheets"] += 1
        if home_goals == 0:
            standings.loc[standings["Teams"] == away_team, "Clean Sheets"] += 1
        if result == "Home Win":
            standings.loc[standings["Teams"] == home_team, "Points"] += 3
            standings.loc[standings["Teams"] == home_team, "Games Won"] += 1
            standings.loc[standings["Teams"] == away_team, "Games Lost"] += 1
        elif result == "Away Win":
            standings.loc[standings["Teams"] == away_team, "Points"] += 3
            standings.loc[standings["Teams"] == away_team, "Games Won"] += 1
            standings.loc[standings["Teams"] == home_team, "Games Lost"] += 1
        elif result == "Draw":
            standings.loc[standings["Teams"] == home_team, "Points"] += 1
            standings.loc[standings["Teams"] == away_team, "Points"] += 1
            standings.loc[standings["Teams"] == home_team, "Games Drawn"] += 1
            standings.loc[standings["Teams"] == away_team, "Games Drawn"] += 1

    standings["Goal Difference"] = standings["Goals Scored Simulated"] - standings["Goals Conceded Simulated"]
    return standings

simulation_results = []
num_simulations = 11

for sim in range(num_simulations):
    simulation_result = simulate_league(team_data, fixture_data)
    simulation_result["Simulation"] = sim + 1
    simulation_results.append(simulation_result)

combined_results = pd.concat(simulation_results)
average_standings = combined_results.groupby("Teams").mean(numeric_only=True).reset_index()

average_standings = average_standings.sort_values(
    by=["Points", "Games Won", "Games Drawn", "Games Lost", "Goals Scored Simulated", 
        "Goals Conceded Simulated", "Goal Difference"],
    ascending=[False, False, False, True, False, True, False]
).reset_index(drop=True)

average_standings.insert(0, "Position", range(1, len(average_standings) + 1))
average_standings.to_csv("average_premier_league_standings.csv", index=False)

fig_final_points = px.bar(average_standings, x="Teams", y="Points", 
                          title="Average Points Across Simulations")
fig_final_points.show()
