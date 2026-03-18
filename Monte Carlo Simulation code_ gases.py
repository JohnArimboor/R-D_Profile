# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:14:11 2026

@author: John Arimboor
"""
# Python code to calcaulte B2 second viral coefficients  of gases He, N2 and Xe
import numpy as np
import scipy.integrate as integrate

# --- Constants ---
k_B = 1.380649e-23     # Boltzmann constant (J/K)
N_A = 6.02214076e23    # Avogadro's number (1/mol)
T = 600.0              # Temperature in Kelvin

# --- Dictionary of Gas Parameters ---
# Format: 'Gas Name': {'sigma': Angstroms, 'epsilon': Joules}
gases = {
    'He': {'sigma': 2.56, 'epsilon': 1.41e-22},
    'N2': {'sigma': 3.75, 'epsilon': 1.32e-21},
    'Ar': {'sigma': 3.40, 'epsilon': 1.66e-21},
    'Xe': {'sigma': 4.07, 'epsilon': 3.04e-21}
}


def calculate_B2_MC(sigma, epsilon, T, n_guesses=500000):
    """Calculates B2 using Direct Monte Carlo integration for given parameters."""
    
    def U(r):
        r_safe = np.where(r == 0, 1e-10, r)
        return 4 * epsilon * ((sigma / r_safe)**12 - (sigma / r_safe)**6)

    def f(r):
        r_safe = np.where(r == 0, 1e-10, r)
        U_val = np.clip(U(r_safe), -np.inf, 100 * k_B * T)
        return (1 - np.exp(-U_val / (k_B * T))) * (r_safe**2)

    # Integration limits and bounding box
    r_min, r_max = 0.0, 20.0
    r_test = np.linspace(2.5, 20, 1000)
    f_test = f(r_test)
    y_min = np.min(f_test) * 1.1 
    y_max = np.max(f_test) * 1.1

    # Random guesses
    Rx = np.random.uniform(r_min, r_max, n_guesses)
    Ry = np.random.uniform(y_min, y_max, n_guesses)

    # Hit-or-miss logic
    f_Rx = f(Rx)
    pos_hits = np.sum((Ry > 0) & (Ry <= f_Rx))
    neg_hits = np.sum((Ry < 0) & (Ry >= f_Rx))
    net_hits = pos_hits - neg_hits
    
    A_box = (r_max - r_min) * (y_max - y_min)
    integral_MC = A_box * (net_hits / n_guesses)
    
    # Convert from Angstroms^3 to m^3/mol
    B2_m3_mol = 2 * np.pi * integral_MC * 1e-30 * N_A
    return B2_m3_mol

# --- Run Simulation for All Gases ---
print(f"--- Second Virial Coefficients (B2) at T = {T} K ---\n")

for gas_name, params in gases.items():
    B2_val = calculate_B2_MC(params['sigma'], params['epsilon'], T)
    print(f"{gas_name} (MC):    {B2_val:.6e} m^3/mol")