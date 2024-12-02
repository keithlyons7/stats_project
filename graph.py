# Author: Luke Hand

import pandas as pd
import plotly.express as px

def load_data(file_path):
    data = pd.read_csv(file_path)
    data["Position"] = (
        data.sort_values(by=["Simulation", "Points", "GoalDifference", "Goals Scored"],
                         ascending=[True, False, False, False])
        .groupby("Simulation")
        .cumcount() + 1
    )
    return data

def plot_average_points(data):
    average_points = data.groupby("Teams")["Points"].mean().reset_index()
    average_points["Points"] = average_points["Points"].astype(int)
    fig = px.bar(
        average_points,
        x="Teams",
        y="Points",
        title="Average Points Across Simulations",
        labels={"Points": "Average Points", "Teams": "Teams"},
        text="Points"
    )
    fig.update_traces(texttemplate='%{text}')
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    fig.show()

def plot_points_distribution(data):
    fig = px.box(
        data,
        x="Teams",
        y="Points",
        title="Points Distribution Across Simulations",
        labels={"Points": "Points", "Teams": "Teams"}
    )
    fig.update_layout(xaxis_tickangle=-45, title_x=0.5)
    fig.show()

def plot_positions_distribution(data):
    fig = px.histogram(
        data,
        x="Position",
        color="Teams",
        title="League Positions Distribution Across Simulations",
        labels={"Position": "League Position", "Teams": "Teams"},
        barmode="group",
        nbins=20
    )
    fig.update_layout(title_x=0.5)
    fig.show()

def plot_points_vs_goal_difference(data):
    fig = px.scatter(
        data,
        x="GoalDifference",
        y="Points",
        color="Teams",
        title="Points vs. Goal Difference Across Simulations",
        labels={"GoalDifference": "Goal Difference", "Points": "Points"},
        hover_data=["Teams"]
    )
    fig.update_layout(title_x=0.5)
    fig.show()

def plot_correlation_heatmap(data):
    numerical_columns = ["Points", "Goals Scored", "Goals Conceded", "GoalDifference", "Expected Goals (xG)", "xG Conceded"]
    correlation_matrix = data[numerical_columns].corr()
    fig = px.imshow(
        correlation_matrix,
        text_auto=True,
        color_continuous_scale="Blues",
        title="Correlation Heatmap of Metrics",
        labels={"color": "Correlation"}
    )
    fig.update_layout(title_x=0.5)
    fig.show()

def plot_team_evolution(data, team_name):
    if team_name not in data["Teams"].unique():
        raise ValueError(f"Team '{team_name}' does not exist in the data.")
    team_data = data[data["Teams"] == team_name]
    fig = px.line(
        team_data,
        x="Simulation",
        y="Points",
        title=f"Points Evolution for {team_name} Across Simulations",
        labels={"Simulation": "Simulation Number", "Points": "Points"}
    )
    fig.update_layout(title_x=0.5)
    fig.show()

if __name__ == "__main__":
    file_path = "simulations.csv"
    data = load_data(file_path)
    plot_average_points(data)
    plot_points_distribution(data)
    plot_positions_distribution(data)
    plot_points_vs_goal_difference(data)
    plot_correlation_heatmap(data)
    plot_team_evolution(data, "Manchester City")
