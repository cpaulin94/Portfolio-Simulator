import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec




# Imposta la modalità notturna se attiva
nightmode = True
if (nightmode) :
    plt.style.use('dark_background')
    plotLinesColor = 'lightgreen'
    investedCapitalColor = "white"
    plt.rcParams.update({
        'axes.facecolor': '#1a1a2e',  # Sfondo dei grafici
        'figure.facecolor': '#1a1a2e',  # Sfondo della figura
        'axes.edgecolor': '#ffffff',  # Colore degli assi
        'axes.labelcolor': '#ffffff',  # Colore delle etichette degli assi
        'xtick.color': '#ffffff',  # Colore dei tick sull'asse x
        'ytick.color': '#ffffff',  # Colore dei tick sull'asse y
        'grid.color': '#333333',  # Colore della griglia
        'text.color': '#ffffff',  # Colore del testo
        'legend.facecolor': '#333333',  # Sfondo della legenda
        'legend.edgecolor': '#ffffff'   # Bordo della legenda
    })
else:
    plotLinesColor = "seagreen"
    investedCapitalColor = "black"

# Parametri per la simulazione
T = 10  # orizzonte temporale in anni
N = 2520  # numero di step temporali
dt = T / N  # passo temporale
mu = 0.0833  # rendimento atteso annuo
sigma = 0.1087  # volatilità annuale
S0 = 28000  # capitale iniziale in EUR
P = 1 / 12  # tempo tra acquisti consecutivi in anni
s = 500  # quantità investita ogni periodo P

# Inizializzazione della figura con proporzioni personalizzate
fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, 2, width_ratios=[2.8, 1])
ax1 = fig.add_subplot(gs[0], sharey=None)
ax2 = fig.add_subplot(gs[1], sharey=ax1)

# Numero di simulazioni
NSims = 500
alphaVal = 30 / NSims

# Memorizza tutte le simulazioni per il calcolo dell'istogramma
simulations = np.zeros((NSims, N))

for i in range(NSims):
    # Valore iniziale del portafoglio
    S = np.empty(0)
    V_i = S0

    # Tempo iniziale
    t = np.arange(0, T, dt)
    p = np.arange(0, P, dt)

    for j in range(int(T / P)):
        # Genera incrementi casuali per il movimento browniano
        dW = np.random.normal(loc=0, scale=np.sqrt(dt), size=len(p))

        # Calcola il valore del portafoglio usando il modello di Black-Scholes
        S_i = V_i * np.exp((mu - 0.5 * sigma**2) * p + sigma * np.cumsum(dW))
        V_i = S_i[-1] + s  # Aggiungi il nuovo investimento
        S = np.concatenate((S, S_i))

    # Memorizza i risultati per il calcolo dell'istogramma
    simulations[i, :len(S)] = S

    # Traccia la simulazione nel primo grafico
    ax1.plot(np.arange(0, len(S) * dt, dt), S / 1000, color=plotLinesColor, alpha=alphaVal)  # Converti in k€

# Aggiungi la griglia e le etichette al primo grafico
ax1.grid()
ax1.set_xlabel('Time [y]')
ax1.set_ylabel('Value [k€]')
ax1.set_title(f'The graph shows {NSims} Black–Scholes model simulations of a capital of {S0/1000:.1f}k€ + {s}€/month \n invested in a portfolio with expected 1-year return μ={mu*100:.2f}% and 1-year volatility σ={sigma*100:.2f}%')

# Inizializza il riferimento alla linea del capitale investito
invested_capital_line, = ax1.plot([], [], color=investedCapitalColor, linestyle='--', label='Invested capital')

# Inizializza il riferimento alla linea verticale
time_marker_line, = ax1.plot([T, T], [0, ax1.get_ylim()[1]], color='red', linestyle='--', label='Clicked time')

# Funzione per aggiornare l'istogramma e il titolo
def update_histogram(t_idx):
    # Calcola il valore medio e i percentili
    values = simulations[:, t_idx] / 1000
    mean_val = np.mean(values)
    perc_5 = np.percentile(values, 5)
    perc_95 = np.percentile(values, 95)
    inv_cap = (S0 + s * (t_idx * dt / P)) / 1000  # Capitale investito fino al tempo t

    # Aggiorna il grafico dell'istogramma
    ax2.cla()
    kde = gaussian_kde(values)
    x = np.linspace(min(values), max(values), 500)
    ax2.plot(kde(x), x, color=plotLinesColor, linewidth=2, label='KDE (Smoothed Histogram)')

    # Aggiungi linee orizzontali per i valori calcolati
    ax2.axhline(inv_cap, color='white', linestyle='--', label=f'Invested capital ({inv_cap:.1f}k€)')
    ax2.axhline(mean_val, color='blue', linestyle='--', label=f'Mean value({mean_val:.1f}k€)')
    ax2.axhline(perc_5, color='red', linestyle='--', label=f'5th Percentile ({perc_5:.1f}k€)')
    ax2.axhline(perc_95, color='gold', linestyle='--', label=f'95th Percentile ({perc_95:.1f}k€)')

    # Aggiungi le etichette e la griglia
    ax2.set_xlabel('Probability density')
    ax2.set_xticks([])
    ax2.set_title(
        f'Smoothed histogram of \n portfolio values at {int(t_idx * dt)} years and {int((t_idx * dt * 12) % 12)} months'
    )
    ax2.legend()
    ax2.grid()
    
    # Aggiorna la linea dell'invested capital sul grafico a sinistra
    invested_capital = [(S0 + s * (time / P)) / 1000 for time in t]
    invested_capital_line.set_data(t, invested_capital)

    # Aggiorna la figura
    fig.canvas.draw_idle()

# Imposta il valore iniziale dell'istogramma al tempo finale
initial_t = int(N - 1)
update_histogram(initial_t)

# Collega l'evento di clic al grafico
def on_click(event):
    if event.inaxes == ax1:
        t_idx = int(event.xdata / T * N)
        update_histogram(t_idx)
        # Sposta la linea verticale rossa al tempo cliccato
        time_marker_line.set_data([event.xdata, event.xdata], ax1.get_ylim())

fig.canvas.mpl_connect('button_press_event', on_click)

# Mostra i grafici
plt.tight_layout()
plt.show()
