# Premier League Monte Carlo Simulation and Random Temperature Process Analysis

This repository contains the implementation of two primary tasks:

1. **Simulation of a Random Temperature Process over a Continuous Time Interval [0,1]**  
2. **Forecasting the Final Standings of the Premier League 2024/25 Season Using Monte Carlo Simulations**

Both tasks utilize Python to model, simulate, and visualize the results efficiently.

---

## Project Structure

### Files and Directories
- `premStats24_25.csv`: Contains team statistics for the Premier League 2024/25 season.
- `fixtures.csv`: The fixture list of Premier League matches for the 2024/25 season.
- `temperature_simulation.py`: Code for simulating the random temperature process.
- `premier_league_simulation.py`: Code for forecasting Premier League standings using Monte Carlo simulations.
- `average_premier_league_standings.csv`: Output file containing average standings across simulations.
- `README.md`: Project documentation.
- `requirements.txt`: List of Python dependencies.

---

## Task 1: Random Temperature Process Simulation

### Objective
To model a temperature process \( X(t) \), varying randomly over time interval \( t \in [0, 1] \), and estimate:
- \( P \): The proportion of time where \( X(t) > 0 \).
- \( T_{\text{max}} \): The time where the maximum temperature is reached.

### Key Features
- Simulates the temperature process using normal distributions for increments (\( \mathcal{N}(0, \Delta t) \)).
- Estimates distributions of \( P \) and \( T_{\text{max}} \) using Monte Carlo simulations.
- Visualizes the results using `plotly`.

### Outputs
- Histograms showing the distributions of \( P \) and \( T_{\text{max}} \).

---

## Task 2: Premier League Standings Forecasting

### Objective
To predict the final standings of the Premier League 2024/25 season using historical team statistics and Monte Carlo simulations.

### Key Features
- **Mathematical Approach**:
  - **Offensive Strength**: \( \text{Offensive Strength} = \frac{\text{Goals Scored}}{\text{Games Played}} \)
  - **Defensive Strength**: \( \text{Defensive Strength} = \frac{\text{Goals Conceded}}{\text{Games Played}} \)
  - Adjusted metrics like possession and passing accuracy, xG (expected goals), and discipline metrics influence match outcomes.
- **Simulation**:
  - Simulates individual match outcomes using Poisson distributions.
  - Tracks points, wins, draws, losses, goals scored, goals conceded, and goal differences.
- **Visualization**:
  - Bar charts, box plots, and heatmaps for insights into team performance variability.

### Outputs
- `average_premier_league_standings.csv`: Final standings averaged across simulations.
- Visualizations showing points, goal differences, and other key metrics.

---

## Installation and Usage

### Prerequisites
Ensure Python 3.8+ is installed. Install dependencies using:

```bash
pip install -r requirements.txt
