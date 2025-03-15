import numpy as np
import matplotlib.pyplot as plt

# Given circuit parameters
L = 1       # Inductance in Henrys
alpha = 0.5  # Duty cycle (50%)
T = 1       # Period of the square wave
h = 0.001    # Step size
t_max = 3  # Simulation time
time = np.arange(0, t_max, h)

# Define square wave input function
def square_wave(t, T, alpha, V_high=10, V_low=0):
    return V_high if (t % T) < (alpha * T) else V_low

# Resistance values to test
R_values = [0.1, 1, 10]

plt.figure(figsize=(10, 6))

for R in R_values:
    # Initialize current array
    i = np.zeros(len(time))
    
    # Forward Euler Method
    for n in range(len(time) - 1):
        v_t = square_wave(time[n], T, alpha)  # Get square wave value
        di_dt = (v_t - R * i[n]) / L  # Compute derivative
        i[n + 1] = i[n] + h * di_dt   # Euler update
    
    # Plot current response for different R values
    plt.plot(time, i, label=f"R = {R} Ω")

# Formatting the plot
plt.xlabel("Time (s)")
plt.ylabel("Current (A)")
plt.title("Effect of Resistance (R) on RL Circuit Response")
plt.legend()
plt.grid()
plt.show()

