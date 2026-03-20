# -*- coding: utf-8 -*-
"""
Created on Thu Mar 19 12:26:23 2026

@author: John Arimboor
"""

import numpy as np
import matplotlib.pyplot as plt

# 1. Define Constants
nums = 1000       # Total students
fract = 0.01      # Fraction initially immune (1%)
recovr = 0.2      # Probability of recovery per day
numd = 40         # Number of days
reps = 40         # Number of repeat simulations

# Arrays to store the averaged daily data
avg_infected = np.zeros(numd)
avg_susceptible = np.zeros(numd)
avg_removed = np.zeros(numd)

# 3. Outer loop: Repeat calculations
for k in range(reps):
    # 2. Initialization
    P = np.ones(nums) # 1 = Susceptible
    
    # Set immune students (0)
    num_immune = int(fract * nums)
    immune_indices = np.random.choice(nums, num_immune, replace=False)
    P[immune_indices] = 0
    
    # Set 1 initially infected student (2)
    # Ensure we don't pick someone who is already immune
    susceptible_indices = np.where(P == 1)[0]
    initial_infected = np.random.choice(susceptible_indices)
    P[initial_infected] = 2
    
    # Daily trackers for this specific run
    daily_I = np.zeros(numd)
    daily_S = np.zeros(numd)
    daily_R = np.zeros(numd)
    
    # Middle loop: Days
    for j in range(numd):
        # We need a copy of P so we don't spread infections to newly infected people on the same day
        P_next = P.copy() 
        
        # Inner loop: Students
        for i in range(nums):
            if P[i] == 2: # If infected
                # Spread infection: Pick a random student
                ra = np.random.randint(0, nums)
                if P[ra] == 1: # If they are susceptible
                    P_next[ra] = 2
                
                # Chance of recovery for the CURRENT infected student
                if np.random.rand() < recovr:
                    P_next[i] = 0 # Becomes immune/removed
                    
        P = P_next.copy()
        
        # Add up daily totals
        daily_I[j] = np.sum(P == 2)
        daily_S[j] = np.sum(P == 1)
        daily_R[j] = np.sum(P == 0)
        
    # Accumulate for averaging
    avg_infected += daily_I
    avg_susceptible += daily_S
    avg_removed += daily_R

# Average the results
avg_infected /= reps
avg_susceptible /= reps
avg_removed /= reps

# Plotting the graph for SIR model for 40days 

plt.plot(avg_susceptible, label='Susceptible (S)', color='blue')
plt.plot(avg_infected, label='Infected (I)', color='red')
plt.plot(avg_removed, label='Removed/Immune (R)', color='green')
plt.title('Monte Carlo Simulation of SIR Epidemic Model (40 Days)')
plt.xlabel('Days')
plt.ylabel('Average Number of Students')
plt.legend()
plt.grid(True)
plt.show()
