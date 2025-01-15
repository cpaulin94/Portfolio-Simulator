# Investment Portfolio Time Simulation Tool

This software simulates the growth of an investment portfolio over a specified time horizon using the Black-Scholes model. It allows users to input initial capital, expected yearly return, and volatility, among other parameters, to visualize potential outcomes and risk assessments.

## Features

- Simulates portfolio growth using Monte Carlo simulations with the Black-Scholes model.
- Supports a positive or negative periodic addition/withdrawal to the portfolio.
- Interactive plots displaying:
  - Simulated portfolio trajectories.
  - Smoothed histogram of portfolio values at any intermediate time, by clicking on the left plot.
  - Statistical summaries including mean, 5th percentile, and 95th percentile.

## Parameters

The simulation requires the following inputs:
- **Time Horizon [T] (years):** The total time period for the simulation.
- **Average Annual Return [μ] (%):** The expected yearly return of the portfolio.
- **Annual Volatility [σ] (%):** The standard deviation of the portfolio's yearly returns.
- **Initial Capital [S₀] (€):** The starting amount of investment capital.
- **Periodic Investment Interval [P] (months):** Frequency of additional investments.
- **Repeated Periodic Investment [s] (€):** Amount added to the portfolio periodically.

## Default Values

- Time Horizon: `10` years.
- Average Annual Return: `8.33%`.
- Annual Volatility: `10.87%`.
- Initial Capital: `€30,000`.
- Periodic Investment Interval: `1` month.
- Repeated Periodic Investment: `€500`.

The Average Annual Return and the Annual Volatility values were derived from historical backtesting of a 70/30 portfolio using the [Curvo](https://curvo.eu/backtest/) website, covering the period from 1992 to 2024.

## How to Use

1. **Launch the application:** Run the script to open the GUI.
2. **Input parameters:** Fill in the required fields or use the default values.
3. **Start the simulation:** Click the "Run Simulation" button.
4. **Interact with the plot:** 
   - Click on the simulation graph to view portfolio statistics at specific points in time.
   - Analyze the smoothed histogram to understand the distribution of portfolio outcomes.

## Dependencies

This project uses the following Python libraries:
- `numpy`
- `matplotlib`
- `scipy`
- `tkinter`
- `sv_ttk`

Ensure these libraries are installed before running the application.

## Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/your-repo/portfolio-sim.git
   cd portfolio-sim
2. Install the dependencies:
   ```bash
   git clone https://github.com/your-repo/investment-portfolio-simulation.git
   pip install numpy matplotlib scipy sv_ttk
3. Run the application:
   ```bash
   python portfolio-sim.py


## License
This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgements
Portfolio backtest data sourced from Curvo.
Dark mode theme powered by sv_ttk.
