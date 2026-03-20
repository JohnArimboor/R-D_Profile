# Simulating-Viral-Disease-using-Monte-Carlo
Project Overview:- 
This project explores the dynamics of an infectious disease spreading through a closed population. Using Python, I have developed a numerical model based on the classic S-I-R (Susceptible, Infected, Removed) epidemiological framework. The goal was to visualize how a virus behaves over time and understand how factors like natural immunity and recovery rates impact the epidemic curve.

Problem Solved:- 
Traditional epidemiological models rely on continuous differential equations, assuming an infinitely large population. However, real-world interactions are discrete and highly unpredictable.

To bridge this gap, I was tasked with modeling a localized outbreak: a university campus of 1,000 students over a 40-day period. Instead of using pure calculus, I have used Monte Carlo integration. By assigning probabilities to daily student interactions and recovery chances, the algorithm rolls virtual dice thousands of times to simulate real-world randomness, eventually averaging the data to find the probable outcome of the spread of disease.
