import numpy as np
import matplotlib.pyplot as plt
from scipy.stats import gaussian_kde
from matplotlib.gridspec import GridSpec

# Parametri per la simulazione
T = 8.0  # orizzonte temporale in anni
N = 2520  # numero di step temporali
dt = T / N  # passo temporale
mu = 0.0794  # rendimento atteso annuo
sigma = 0.0868  # volatilità annuale
S0 = 218000  # capitale iniziale in EUR

# Inizializzazione della figura con proporzioni personalizzate
fig = plt.figure(figsize=(16, 8))
gs = GridSpec(1, 2, width_ratios=[2.8, 1])  # 2 unità per ax1, 1 unità per ax2
ax1 = fig.add_subplot(gs[0], sharey=None)  # Assegna ax1 alla prima colonna (più larga)
ax2 = fig.add_subplot(gs[1], sharey=ax1)   # Assegna ax2 all'ultima unità

# Numero di simulazioni
NSims = 500
alphaVal = 30 / NSims  # trasparenza delle linee delle simulazioni

# Memorizza tutte le simulazioni per il calcolo dell'istogramma
simulations = np.zeros((NSims, N))

for i in range(NSims):
    # Genera incrementi casuali per il movimento browniano
    dW = np.random.normal(loc=0, scale=np.sqrt(dt), size=N)

    # Calcola il valore del portafoglio usando il modello di Black-Scholes
    t = np.arange(0, T, dt)
    S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * np.cumsum(dW))

    # Memorizza i risultati per il calcolo dell'istogramma
    simulations[i] = S

    # Traccia la simulazione nel primo grafico
    ax1.plot(t, S / 1000, color='seagreen', alpha=alphaVal)  # Converti in k€

# Aggiungi la griglia e le etichette al primo grafico
ax1.grid()
ax1.set_xlabel('Time [y]')
ax1.set_ylabel('Price [k€]')
ax1.set_title(f'The graph shows {NSims} Black–Scholes simulations\nfor a portfolio with μ={mu*100:.2f}% and σ={sigma*100:.2f}%')

# Funzione per aggiornare l'istogramma e il titolo
def update_histogram(t_idx):
    # Calcola il valore medio e i percentili
    values = simulations[:, t_idx] / 1000  # Converti in k€
    mean_val = np.mean(values)
    perc_5 = np.percentile(values, 5)
    perc_95 = np.percentile(values, 95)

    # Aggiorna il grafico smussato con kernel density estimation
    ax2.cla()
    kde = gaussian_kde(values)  # Calcola la densità kernel
    x = np.linspace(min(values), max(values), 500)
    ax2.plot(kde(x), x, color='seagreen', linewidth=2, label='KDE (Smoothed Histogram)')

    # Aggiungi linee orizzontali per i valori calcolati
    ax2.axhline(mean_val, color='blue', linestyle='--', label=f'Mean ({mean_val:.1f}k€)')
    ax2.axhline(perc_5, color='red', linestyle='--', label=f'5th Percentile ({perc_5:.1f}k€)')
    ax2.axhline(perc_95, color='gold', linestyle='--', label=f'95th Percentile ({perc_95:.1f}k€)')

    # Aggiungi le etichette e la griglia
    ax2.set_xlabel('Probability density')
    ax2.set_xticks([])
    ax2.set_title(
        f'Smoothed histogram of portfolio values\n at {t_idx * dt:.2f} years\n'
        f'Mean = {mean_val:.1f}k€, 5th = {perc_5:.1f}k€, 95th = {perc_95:.1f}k€'
    )
    ax2.legend()


    # Ridisegna la figura
    fig.canvas.draw_idle()

# Imposta il valore iniziale dell'istogramma al tempo finale
initial_t = int(N-1)
update_histogram(initial_t)

# Collega l'evento di clic al grafico
def on_click(event):
    # Calcola l'indice del tempo t in base alla posizione X del clic
    if event.inaxes == ax1:
        t_idx = int(event.xdata / T * N)  # Map X (in anni) alla posizione t nell'array
        update_histogram(t_idx)

fig.canvas.mpl_connect('button_press_event', on_click)

# Mostra i grafici
plt.tight_layout()
plt.show()
