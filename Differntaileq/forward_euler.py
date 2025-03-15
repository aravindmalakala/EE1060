import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation
from matplotlib.widgets import Slider, Button

# Define square wave input
def square_wave(t, alpha, T, A=20):  
    return A if 0 < t % T < alpha * T else 0

# Forward Euler Method for RL Circuit
def forward_euler(T, R, L, alpha, h, time_end):
    time_points = np.linspace(0, time_end, int(time_end / h))  
    current = np.zeros_like(time_points)
    y = 0  

    for i in range(1, len(time_points)):
        vin = square_wave(time_points[i - 1], alpha, T)  
        dy = (vin - R * y) / L  
        y += h * dy  
        current[i] = y  

    return time_points, current

# Default parameters
alpha = 0.5  
R = 1        
L = 1        
T = 1        
h = 0.01     
time_end = 10  

fig, ax = plt.subplots(figsize=(8, 5))
plt.subplots_adjust(left=0.25, bottom=0.4)
ax.set_xlabel('Time [s]')
ax.set_ylabel('Current [A]')
ax.set_title('Forward Euler RL Circuit')
ax.set_xlim(0, time_end)  
ax.set_ylim(0, 25)  
line, = ax.plot([], [], lw=2, color='blue', label="Current")
dot, = ax.plot([], [], 'ro', markersize=8)  

ax_L = plt.axes([0.25, 0.25, 0.65, 0.03])
ax_R = plt.axes([0.25, 0.2, 0.65, 0.03])
ax_T = plt.axes([0.25, 0.15, 0.65, 0.03])
ax_alpha = plt.axes([0.25, 0.1, 0.65, 0.03])

L_slider = Slider(ax_L, 'L (Inductance)', 0.1, 5, valinit=L)
R_slider = Slider(ax_R, 'R (Resistance)', 0.1, 10, valinit=R)
T_slider = Slider(ax_T, 'T (Time Period)', 0.1, 5, valinit=T)
alpha_slider = Slider(ax_alpha, 'Alpha (Duty Cycle)', 0, 1, valinit=alpha)

# Store animation globally
ani = None

# Function to reset the animation
def start_animation(event):
    global ani  

    # Update values from sliders
    L = L_slider.val
    R = R_slider.val
    T = T_slider.val
    alpha = alpha_slider.val

    # Get new simulation data
    t_vals, i_vals = forward_euler(T, R, L, alpha, h, time_end)

    # Clear previous animation
    if ani:
        ani.event_source.stop()  
        ani = None  

    # Reset plot data
    line.set_data([], [])
    dot.set_data([], [])

    # Animation function
    def animate(i):
        line.set_data(t_vals[:i], i_vals[:i])
        if i > 0:
            dot.set_data(t_vals[i-1], i_vals[i-1])  
            color_intensity = np.clip(abs(i_vals[i-1]) / max(abs(i_vals) + 1e-6), 0, 1)  
            dot.set_color((1, 0, 0, color_intensity))  
        return line, dot

    # Start the new animation
    ani = animation.FuncAnimation(fig, animate, frames=len(t_vals), interval=20, blit=True)
    plt.draw()

# Button to start animation
start_ax = plt.axes([0.4, 0.03, 0.2, 0.04])
start_button = Button(start_ax, 'Start Animation', hovercolor='0.8')
start_button.on_clicked(start_animation)

ax.legend()
plt.show()

