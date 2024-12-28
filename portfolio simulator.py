import numpy as np
import matplotlib.pyplot as plt


# Simulation tool for investment portfolio time simulation. User needs to input the initial invested capital S0,
# as well as the expected yearly return and volatility. The simulation is run over a time T in years.
# The values of mu=0.085 and sigma=0.1009 for the 70/30 portfolio were obtained with a backtest on Curvo website
# from 1992 to 2024. 
# https://curvo.eu/backtest/it/portafoglio/portafoglio-60-40--NoIgCg9gTgLghgMwgcwDYEsIAIBsAGAegBY8QAaYUAGQFU8BmAdgA5mBGd+t8vAOnoC6FELQ4AmAJxixeNvXo9eRAKxDQASQCieHQA0AWgGUAaow6KxqgQKA?config=%7B%22withTer%22%3A%22false%22%7D

# Parameters for the simulation (using Black–Scholes model)
T = 8.0  # time horizon in years
N = 2520  # number of time steps
dt = T / N  # time step
mu = 0.085  # expected return per year (0.085 for a 70/30 portfolio with ETF on global stock market and global bonds)
sigma =  0.1009  # volatility, which is the std dev of expected yearly return. 0.1009 for the 70/30 portfolio
S0 = 30000  # initial invested capital in EUR



plt.figure(figsize=(10,8))
NSims = 500 # number of simulations to run
alphaVal = 30/NSims # line transparency for the simulation

for i in range(NSims):
    # Generate random increments for the Brownian motion
    #np.random.seed(123)
    dW = np.random.normal(loc=0, scale=np.sqrt(dt), size=N)

    # Compute the stock price using the Black-Scholes model
    t = np.arange(0, T, dt)
    S = S0 * np.exp((mu - 0.5 * sigma**2) * t + sigma * np.cumsum(dW))

    # Plot the simulated stock price
    plt.plot(t, S,  color='seagreen', alpha=30/NSims)


plt.grid()
plt.xlabel('Time [y]')
plt.ylabel('Price [EUR]')
plt.title(f'The graph shows {NSims} Black–Scholes model simulations of a captial of {S0} EUR\n invested in a portfolio with expected 1-year return μ={mu*100}% and 1-year volatility σ={sigma*100}%')
plt.show()