import numpy as np
import matplotlib.pyplot as plt
import matplotlib.animation as animation

import dearpygui.dearpygui as dpg

import tkinter as tk
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

dpg.create_context()

dpg.set_global_font_scale(1.5)

gui_width = 1500

def open_window(sender, app_data):
    dpg.show_item("Settings Menu")

def close_window(sender, app_data):
    dpg.hide_item("Settings Menu")

def show_plot(sender, add_data):
    x_mag = dpg.get_value(E_x_mag)
    phi_x = np.deg2rad(dpg.get_value(x_phase))
    y_mag = dpg.get_value(E_y_mag)
    phi_y = np.deg2rad(dpg.get_value(y_phase))

    E_x = x_mag*np.e**(1j*phi_x)
    E_y = y_mag*np.e**(1j*phi_y)

    E_eff = np.sqrt(x_mag**2 + y_mag**2)        
    # the phase term of x will end up in the overall exponential. that is, E = E_eff * (Jones vector) * e^(i(kz - omega t + phi_x))
    # time is frozen at t = omega / phi_x and wavelength is set at 2pi (definitely not visible light but its just for visualization
    # and it makes the math easier)

    # soooooo E = E_eff * (Jones vector) * e^(ikz)

    A = x_mag / E_eff
    B = y_mag / E_eff

    delta = phi_y - phi_x

    jonesVec = np.array([A, B*np.e**(delta*1j)])


    fig = plt.figure()
    axis = plt.axes()
    if (x_mag >= y_mag):
        lim = (-1.4*x_mag, 1.4*x_mag)
    else:
        lim = (-1.4*y_mag, 1.4*y_mag)
    
    axis.set(xlim=lim, ylim=lim)
    axis.set_aspect('equal', 'box')
    #axis.set_axis_off()

    x, y = [], []
    line, = axis.plot(x, y, lw=2)
    point, = axis.plot(0,1, marker="o", color='black')


    def init():
        E_0 = np.array([E_eff**np.e**(1j*0)*jonesVec[0], E_eff*np.e**(1j*0)*jonesVec[1]])  # When z = 0, the exponential term becomes e^0 = 1

        line.set_data([E_0[0]], [E_0[1]])
        point.set_data([E_0[0]], [E_0[1]])
        
        return line, point,

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

    anim = animation.FuncAnimation(fig, animate, init_func=init,
                                frames=628, interval=3, blit=True)

    plt.grid()

    #writergif = animation.PillowWriter(fps=60)
    #anim.save('figures/anim.gif',writer=writergif

    # Create a Tkinter window
    root = tk.Tk()
    root.title("Matplotlib Plot")

    # Embed the Matplotlib plot in the Tkinter window
    canvas = FigureCanvasTkAgg(fig, master=root)
    canvas.draw()
    canvas.get_tk_widget().pack()

    # Start the Tkinter event loop
    root.mainloop()
    
    #plt.show()


# MAIN WINDOW
with dpg.window(tag="Primary Window", label="Example Window", width = gui_width, height=600):
    dpg.add_text("Hello! This is a little script that I made to help myself visualize polarization. More specifically, I wanted to")
    dpg.add_text("see how changing the x- and y-components of the electric field vector would affect the geometry of the ellipse as")
    dpg.add_text("the light hits a screen.")
    

    dpg.add_button(label="Settings", callback=open_window)
    dpg.add_button(label="Show plot", callback=show_plot)

# SETTINGS MENU
with dpg.window(tag="Settings Menu", label="Settings Menu", pos=(160,200), width=720, height=180, show = False, modal=True):
    E_x_mag = dpg.add_input_float(tag="|E_x|", label="|E_x|", min_value = 0, max_value = 20, default_value = 1)
    E_y_mag = dpg.add_input_float(tag="|E_y|", label="|E_y|", min_value = 0, max_value = 20, default_value = 1)
    x_phase = dpg.add_input_float(tag="phi_x", label="Phase of x (degrees)", min_value = -180, max_value = 180, default_value = 0)
    y_phase = dpg.add_input_float(tag="phi_y", label="Phase of y (degrees)", min_value = -180, max_value = 180, default_value = 0)

    dpg.add_button(label="Save & Close", callback=close_window, parent="Settings Menu")



dpg.create_viewport(title='Visualizing Polarization', width=gui_width, height=600)

dpg.setup_dearpygui()
dpg.show_viewport()

dpg.set_primary_window("Primary Window", True)

dpg.start_dearpygui()
dpg.destroy_context()