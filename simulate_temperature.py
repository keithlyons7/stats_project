import numpy as np
import plotly.express as px
import pandas as pd

# Re-run with validation of delta_t effects
def simulate_temperature_with_validation(delta_t, num_trials):
    n_steps = int(1 / delta_t)
    times = np.linspace(0, 1, n_steps + 1)
    
    P_samples = []
    Tmax_samples = []
    
    for _ in range(num_trials):
        # Generate increments from N(0, delta_t)
        increments = np.random.normal(0, np.sqrt(delta_t), n_steps)
        X = np.concatenate(([0], np.cumsum(increments)))  # Cumulative sum, starting at 0
        
        # Proportion of time temperature is positive
        P = np.sum(X > 0) / n_steps
        P_samples.append(P)
        
        # Time of maximum temperature
        Tmax = times[np.argmax(X)]
        Tmax_samples.append(Tmax)
    
    return P_samples, Tmax_samples

# Parameters
delta_t_values = [0.01, 0.001, 0.0001]
num_trials = 10000

results_adjusted = []

for delta_t in delta_t_values:
    P_samples, Tmax_samples = simulate_temperature_with_validation(delta_t, num_trials)
    
    # Store results in a DataFrame for Plotly
    results_adjusted.append(pd.DataFrame({
        'P': P_samples,
        'Tmax': Tmax_samples,
        'Delta_t': delta_t
    }))

# Combine results from all delta_t values
results_df_adjusted = pd.concat(results_adjusted, ignore_index=True)

# Plot distribution of P
fig_p_adjusted = px.histogram(
    results_df_adjusted,
    x="P",
    color="Delta_t",
    barmode="overlay",
    histnorm="probability",
    title="Adjusted Distribution of P",
    labels={"P": "Proportion of Time Temperature is Positive", "Delta_t": "Delta t"},
    nbins=50
)
fig_p_adjusted.update_layout(xaxis_title="P (Proportion of Time > 0)", yaxis_title="Probability")

# Plot distribution of Tmax
fig_tmax_adjusted = px.histogram(
    results_df_adjusted,
    x="Tmax",
    color="Delta_t",
    barmode="overlay",
    histnorm="probability",
    title="Adjusted Distribution of Tmax",
    labels={"Tmax": "Time of Maximum Temperature", "Delta_t": "Delta t"},
    nbins=50
)
fig_tmax_adjusted.update_layout(xaxis_title="Tmax (Time of Maximum Temperature)", yaxis_title="Probability")

fig_p_adjusted.show()
fig_tmax_adjusted.show()
