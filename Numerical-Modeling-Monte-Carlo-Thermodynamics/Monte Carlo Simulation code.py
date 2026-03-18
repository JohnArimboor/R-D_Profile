# -*- coding: utf-8 -*-
"""
Created on Wed Mar 18 09:13:51 2026

@author: John Arimboor
"""
# Python code to calculate B2 second viral coefficient of Argon gas

import numpy as np
import matplotlib.pyplot as plt
import scipy.integrate as integrate
from scipy.optimize import fsolve

# --- Constants and Parameters (Argon) ---
k_B = 1.380649e-23     # Boltzmann constant (J/K)
N_A = 6.02214076e23    # Avogadro's number (1/mol)
T = 600.0              # Temperature in Kelvin
P = 600e5              # Pressure in Pascals (600 bar = 600 * 10^5 Pa)
R = 8.314              # Universal gas constant (J/(mol K))

# Argon parameters
sigma = 3.4            
epsilon = 1.66e-21     

# --- 1. Function Definitions ---
def U(r):
    """Lennard-Jones 6-12 Potential."""
    # Add a tiny value to r to avoid division by zero at r=0
    r_safe = np.where(r == 0, 1e-10, r)
    return 4 * epsilon * ((sigma / r_safe)**12 - (sigma / r_safe)**6)

def f(r):
    """Function to integrate for B2."""
    r_safe = np.where(r == 0, 1e-10, r)
    # Clip potential to avoid overflow in exponential
    U_val = np.clip(U(r_safe), -np.inf, 100 * k_B * T)
    return (1 - np.exp(-U_val / (k_B * T))) * (r_safe**2)

# Plot U(r) and f(r) ---
r_plot = np.linspace(2.5, 10, 1000)

fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

# Plot U(r)
ax1.plot(r_plot, U(r_plot), color='blue')
ax1.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax1.set_ylim(-2e-21, 5e-21)
ax1.set_title('Lennard-Jones Potential U(r) for Argon')
ax1.set_xlabel('r (Angstroms)')
ax1.set_ylabel('U(r) (Joules)')

# Plot f(r)
ax2.plot(r_plot, f(r_plot), color='red')
ax2.axhline(0, color='black', linestyle='--', linewidth=0.8)
ax2.set_title('Integration Function f(r) at T = 600 K')
ax2.set_xlabel('r (Angstroms)')
ax2.set_ylabel('f(r)')

plt.tight_layout()
plt.show() # This generates the plot 

#  Direct Monte Carlo Integration ---
n_guesses = 500000
r_min, r_max = 0.0, 20.0

# Find ymin and ymax for the bounding box dynamically
r_test = np.linspace(2.5, 20, 1000)
f_test = f(r_test)
y_min = np.min(f_test) * 1.1 # Add 10% padding
y_max = np.max(f_test) * 1.1

# Generate random points
Rx = np.random.uniform(r_min, r_max, n_guesses)
Ry = np.random.uniform(y_min, y_max, n_guesses)

# Evaluate function at Rx
f_Rx = f(Rx)

# Hit-or-miss logic for functions that cross the x-axis
# Hits above x-axis (positive area)
pos_hits = np.sum((Ry > 0) & (Ry <= f_Rx))
# Hits below x-axis (negative area)
neg_hits = np.sum((Ry < 0) & (Ry >= f_Rx))

net_hits = pos_hits - neg_hits
A_box = (r_max - r_min) * (y_max - y_min)

integral_MC = A_box * (net_hits / n_guesses)
B2_MC_angstrom = 2 * np.pi * integral_MC

# Convert B2 to standard molar units (m^3 / mol)
# 1 Angstrom^3 = 1e-30 m^3
B2_MC_m3_mol = B2_MC_angstrom * 1e-30 * N_A
print(f"Direct Monte Carlo B2: {B2_MC_m3_mol:.6e} m^3/mol")

# Scipy Numerical Integration ---
integral_scipy, error = integrate.quad(f, r_min, r_max)
B2_scipy_m3_mol = 2 * np.pi * integral_scipy * 1e-30 * N_A
print(f"Scipy Numerical B2:    {B2_scipy_m3_mol:.6e} m^3/mol")

# Molar Volume Equation of State ---
# (a) Ideal Gas Equation: V = RT/P
V_ideal = (R * T) / P
print(f"\nIdeal Gas Molar Volume:  {V_ideal:.6e} m^3/mol")

# (b) Virial Equation: Z = PV/RT = 1 + B2/V  => V^2 - (RT/P)V - (RT/P)B2 = 0
# We solve this quadratic equation using fsolve
def virial_eq(V):
    return V**2 - V_ideal * V - V_ideal * B2_MC_m3_mol

V_virial = fsolve(virial_eq, V_ideal)[0] # Use ideal volume as initial guess
print(f"Virial Gas Molar Volume: {V_virial:.6e} m^3/mol")
