import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

# Define polarization state (this is user-defined in the 'real' version)
x_mag = 1
phi_x = np.deg2rad(0)
y_mag = 1
phi_y = np.deg2rad(90)

# Calculate x- and y-components of electric field vector
E_x = x_mag*np.e**(1j*phi_x)
E_y = y_mag*np.e**(1j*phi_y)

# Determine the actually useful quantities from that
E_eff = np.sqrt(x_mag**2 + y_mag**2)        
A = x_mag / E_eff
B = y_mag / E_eff
delta = phi_y - phi_x

# Define Jones vector
jonesVec = np.array([A, B*np.e**(delta*1j)])

# Plotting stuff. Chooses scaling based on which of E_x or E_y is bigger, such that the
# plot is always a square that the ellipse/circle/line fits nicely within
fig = plt.figure()
axis = plt.axes()
if (x_mag >= y_mag):
    lim = (-1.4*x_mag, 1.4*x_mag)
else:
    lim = (-1.4*y_mag, 1.4*y_mag)
    
axis.set(xlim=lim, ylim=lim)
axis.set_aspect('equal', 'box')

# Initializing the things to plot. line, is the blue trail and point, is the point at the "front"
x, y = [], []
line, = axis.plot(x, y, lw=2)
point, = axis.plot(x, y, marker="o", color='black')

def init():
    E_0 = np.array([E_eff**np.e**(1j*0)*jonesVec[0], E_eff*np.e**(1j*0)*jonesVec[1]]) 

    line.set_data([E_0[0]], [E_0[1]])
    point.set_data([E_0[0]], [E_0[1]])
        
    return line, point,

# Does all the calculations for new points iteratively. Moves the point and extends the line accordingly
def animate(i):
    z = i/100

    E = np.array([E_eff*np.e**(1j*z)*jonesVec[0], E_eff*np.e**(1j*z)*jonesVec[1]])

    x_new = E[0]
    y_new = E[1]

    x.append(x_new)
    y.append(y_new)

    line.set_data(np.real(x), np.real(y))
    point.set_data([np.real(x_new)], [np.real(y_new)])
    return line, point,

anim = animation.FuncAnimation(fig, animate, init_func=init, frames=628, interval=2, blit=True)

plt.grid()
plt.show()