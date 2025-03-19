import numpy as np
import json

def simulate_short_rate(total_time, initial_rate, volatility, num_simulations, time_step=0.01):
    """
    Simulates the evolution of the short rate r(t) using Antithetic Sampling and NumPy Vectorization.
    """
    num_simulations = int(num_simulations)
    num_steps = int(round(total_time / time_step))
    time_grid = np.linspace(0, total_time, num_steps + 1)

    # Antithetic Sampling: Generate half the number of simulations
    half_simulations = num_simulations // 2

    # Generate standard normal random variables for Brownian motion
    brownian_motion = np.random.normal(0, np.sqrt(time_step), (half_simulations, num_steps))

    # Create antithetic samples by negating brownian_motion
    brownian_motion_full = np.vstack([brownian_motion, -brownian_motion])

    # Initialize rate paths
    rate_paths = np.full((num_simulations, num_steps + 1), initial_rate)

    # Use NumPy vectorized operations to update all paths
    rate_paths[:, 1:] = initial_rate + np.cumsum(volatility * brownian_motion_full, axis=1)

    return rate_paths, time_grid

def compute_discount_factors(rate_paths, time_grid):
    """
    Calculates the evolution of the discount factor P(0,t) for each trajectory.
    """
    dt = np.diff(time_grid)  # Time step differences
    integral = np.cumsum(rate_paths[:, :-1] * dt, axis=1)  # Integral approximation
    discount_factors = np.exp(-integral)  # Compute discount factors
    return discount_factors

def monte_carlo_bond_price(total_time, initial_rate, volatility, num_simulations, time_step=0.01):
    """
    Performs a Monte Carlo simulation using Antithetic Sampling and NumPy Vectorization.
    """
    rate_paths, time_grid = simulate_short_rate(total_time, initial_rate, volatility, num_simulations, time_step)
    discount_factors = compute_discount_factors(rate_paths, time_grid)
    
    # Retrieve final discount factors for bond pricing
    final_discount_factors = discount_factors[:, -1]
    
    # Compute Monte Carlo estimates (using antithetic sampling)
    estimated_price = np.mean(final_discount_factors)
    variance = np.var(final_discount_factors)
    
    return round(float(estimated_price), 10), round(float(variance), 10)

def run(input_data, solver_params=None, extra_arguments=None):
    """
    Runs the bond pricing simulation using an improved Monte Carlo method.
    """
    initial_rate = input_data["Initial Interest Rate"]
    volatility = input_data["Volatility"]
    bond_maturity = input_data["Maturity Time"] / 12  # Convert months to years

    # Retrieve number of simulations from solver_params
    num_simulations = solver_params.get("NumberOfSimulations", 10000)

    # Compute bond price statistics
    estimated_price, variance = monte_carlo_bond_price(bond_maturity, initial_rate, volatility, num_simulations)

    return {
        "bond_price": estimated_price,
        "variance": variance
    }