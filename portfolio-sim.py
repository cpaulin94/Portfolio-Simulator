import numpy as np
import matplotlib as mpl
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec
import tkinter as tk
from tkinter import ttk
import sv_ttk

# Set dark mode if enabled
nightmode = True
if (nightmode) :
    plt.style.use('dark_background')
    plotLinesColor = 'lightgreen'
    investedCapitalColor = "white"
    plt.rcParams.update({
        'axes.facecolor': '#1a1a2e',  # Background of the plots
        'figure.facecolor': '#1a1a2e',  # Background of the figure
        'axes.edgecolor': '#ffffff',  # Color of the axes
        'axes.labelcolor': '#ffffff',  # Color of the axis labels
        'xtick.color': '#ffffff',  # Color of the x-axis ticks
        'ytick.color': '#ffffff',  # Color of the y-axis ticks
        'grid.color': '#333333',  # Color of the grid
        'text.color': '#ffffff',  # Color of the text
        'legend.facecolor': '#333333',  # Background of the legend
        'legend.edgecolor': '#ffffff'   # Border of the legend
    })
else:
    plotLinesColor = "seagreen"
    investedCapitalColor = "black"

#remove maptlotlib toolbar
mpl.rcParams['toolbar'] = 'None' 

# Function to start the simulation with the specified parameters
def run_simulation():
    # Retrieve values from the input fields
    try:
        T = float(entry_T.get())
        mu = float(entry_mu.get())/100
        sigma = float(entry_sigma.get())/100
        S0 = float(entry_S0.get())
        P = float(entry_P.get())/12
        s = float(entry_s.get())
    except ValueError:
        status_label.config(text="Error: Please enter valid numeric values.", fg="red")
        return

    # Fixed parameters
    N = 2520  # Number of time steps
    dt = T / N  # Time step
    NSims = 500  # Number of simulations
    alphaVal = 30 / NSims

    # Initialize the figure
    fig = plt.figure(figsize=(16, 8))
    gs = GridSpec(1, 2, width_ratios=[2.8, 1])
    ax1 = fig.add_subplot(gs[0], sharey=None)
    ax2 = fig.add_subplot(gs[1], sharey=ax1)

    # Store all simulations for histogram calculation
    simulations = np.zeros((NSims, N))

    for i in range(NSims):
        S = np.empty(0)
        V_i = S0

        t = np.arange(0, T, dt)
        p = np.arange(0, P, dt)

        for j in range(int(T / P)):
            dW = np.random.normal(loc=0, scale=np.sqrt(dt), size=len(p))
            S_i = V_i * np.exp((mu - 0.5 * sigma**2) * p + sigma * np.cumsum(dW))
            V_i = S_i[-1] + s
            S = np.concatenate((S, S_i))

        simulations[i, :len(S)] = S
        ax1.plot(np.arange(0, len(S) * dt, dt), S / 1000, color='lightgreen', alpha=alphaVal)

    ax1.grid()
    ax1.set_xlabel('Time [y]')
    ax1.set_ylabel('Value [k€]')
    ax1.set_title(f'The graph shows {NSims} Black–Scholes model simulations of a capital of {S0/1000:.1f}k€ + {s}€/month\n'
                  f'invested in a portfolio with expected 1-year return μ={mu*100:.2f}% and 1-year volatility σ={sigma*100:.2f}%')

    invested_capital_line, = ax1.plot([], [], color='white', linestyle='-', label='Invested capital')
    time_marker_line, = ax1.plot([T, T], [0, ax1.get_ylim()[1]], color='red', linestyle='-', label='Clicked time')

    def update_histogram(t_idx):
        values = simulations[:, t_idx] / 1000
        mean_val = np.mean(values)
        perc_5 = np.percentile(values, 5)
        perc_95 = np.percentile(values, 95)
        inv_cap = (S0 + s * (t_idx * dt / P)) / 1000

        ax2.cla()
        kde = gaussian_kde(values)
        x = np.linspace(min(values), max(values), 500)
        ax2.plot(kde(x), x, color='lightgreen', linewidth=2, label='KDE (Smoothed Histogram)')
        ax2.axhline(inv_cap, color='white', linestyle='--', label=f'Invested capital ({inv_cap:.1f}k€)')
        ax2.axhline(mean_val, color='blue', linestyle='--', label=f'Mean value ({mean_val:.1f}k€)')
        ax2.axhline(perc_5, color='red', linestyle='--', label=f'5th Percentile ({perc_5:.1f}k€)')
        ax2.axhline(perc_95, color='gold', linestyle='--', label=f'95th Percentile ({perc_95:.1f}k€)')
        ax2.set_xlabel('Probability density')
        ax2.set_xticks([])
        ax2.set_title(f'Smoothed histogram of \n portfolio values at {int(t_idx * dt)} years and {int((t_idx * dt * 12) % 12)} months')
        ax2.legend()
        ax2.grid()

        invested_capital = [(S0 + s * (time / P)) / 1000 for time in t]
        invested_capital_line.set_data(t, invested_capital)
        fig.canvas.draw_idle()

    initial_t = int(N - 1)
    update_histogram(initial_t)

    def on_click(event):
        if event.inaxes == ax1:
            t_idx = int(event.xdata / T * N)
            update_histogram(t_idx)
            time_marker_line.set_data([event.xdata, event.xdata], ax1.get_ylim())

    fig.canvas.mpl_connect('button_press_event', on_click)


    plt.tight_layout()
    plt.show()

# Configure the main window
root = tk.Tk()
root.title("Input Montecarlo Simulation Parameters")

# Set dark color for tkinter window
sv_ttk.set_theme("dark")

# Layout for parameters
frame = ttk.Frame(root, padding="10")
frame.grid(row=0, column=0, sticky=(tk.W, tk.E, tk.N, tk.S))

# Input fields
entry_T = ttk.Entry(frame)
entry_mu = ttk.Entry(frame)
entry_sigma = ttk.Entry(frame)
entry_S0 = ttk.Entry(frame)
entry_P = ttk.Entry(frame)
entry_s = ttk.Entry(frame)

# Set default values
entry_T.insert(0, "10")
entry_mu.insert(0, "8.33")
entry_sigma.insert(0, "10.87")
entry_S0.insert(0, "28000")
entry_P.insert(0, "1")
entry_s.insert(0, "500")

# Labels
labels = ["Time Horizon [y]:", "Average Annual Return [%]:", "Annual Volatility [%]:", "Initial Capital [€]:", "Periodic investment interval [months]:", "Repeated periodic investment [€]:"]
entries = [entry_T, entry_mu, entry_sigma, entry_S0, entry_P, entry_s]

for i, (label, entry) in enumerate(zip(labels, entries)):
    ttk.Label(frame, text=label).grid(row=i, column=0, sticky=tk.W)
    entry.grid(row=i, column=1, sticky=(tk.W, tk.E))

# Button to run the simulation
btn_run = ttk.Button(frame, text="Run Simulation", command=run_simulation)
btn_run.grid(row=len(labels), column=0, columnspan=2, pady=10)

status_label = ttk.Label(frame, text="", foreground="green")
status_label.grid(row=len(labels) + 1, column=0, columnspan=2)

root.mainloop()
