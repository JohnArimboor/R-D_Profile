# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 04:57:48 2026

@author: John Arimboor
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Constants & Parameters
deltax = 0.5          # Max step size (nm)
kb = 1.380649e-23     # Boltzmann Constant (J/K)
T = 300.0             # Temperature (K)
kT = kb * T
kf = 10.0             # Force constant (N/m)
nm = 1e-9             # Nanometer conversion

def calculate_energy(x_nm):
    # V = 0.5 * kf * x^2
    return 0.5 * kf * (x_nm * nm)**2

# 2. Encapsulating the simulation into a function for reuse
def run_simulation(N_steps):
    x1 = 0.0
    E1 = calculate_energy(x1)
    Etot = 0.0
    E2tot = 0.0
    x_history = []
    
    # Metropolis Loop
    for i in range(N_steps):
        x2 = x1 + (np.random.rand() * 2 - 1) * deltax
        E2 = calculate_energy(x2)
        
        delta_E = E2 - E1
        
        # Metropolis Acceptance Criterion
        if delta_E <= 0 or np.exp(-delta_E / kT) > np.random.rand():
            x1 = x2
            E1 = E2
            
        Etot += E1
        E2tot += E1**2
        x_history.append(x1)
        
    # Data Analysis for this specific run
    E_avg = Etot / N_steps
    E2_avg = E2tot / N_steps
    variance = E2_avg - E_avg**2
    
    return E_avg, variance, x_history

# RUN THE MAIN SIMULATION (N = 100,000)

N_main = 100000
E_avg_main, variance_main, x_history_main = run_simulation(N_main)
Cv = variance_main / (kb * T**2)

print(f"Average Potential Energy: {E_avg_main:.4e} J")
print(f"Theoretical Energy (0.5kT): {0.5 * kT:.4e} J")
print(f"Heat Capacity (Cv): {Cv:.4e} J/K")


# GENERATING THE PLOT

# The Distribution Plot (Histogram) 
plt.subplot(1, 2, 1)

# Plot the histogram of where the particle actually went
plt.hist(x_history_main, bins=60, density=True, alpha=0.7, color='royalblue', edgecolor='black', label='Simulated Data')

# Calculate and overlay the Theoretical Gaussian (Bell Curve)
x_theo = np.linspace(min(x_history_main), max(x_history_main), 200)
variance_x = kT / (kf * nm**2)  # Theoretical variance of position
sigma_x = np.sqrt(variance_x)
pdf_theo = (1 / (sigma_x * np.sqrt(2 * np.pi))) * np.exp(-0.5 * (x_theo / sigma_x)**2)

plt.plot(x_theo, pdf_theo, color='red', linewidth=2.5, label='Theoretical Gaussian')
plt.title('Particle Position Distribution', fontsize=14)
plt.xlabel('Position x (nm)', fontsize=12)
plt.ylabel('Probability Density', fontsize=12)
plt.legend()


# Display the plots
plt.tight_layout()
plt.show()
