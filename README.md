# visual_polarization

A little script I wrote up to help visualize how the electric field vector changes as a function of z (position in the direction of propagation, i.e. where you are on the wave) for different kinds of polarization.

The original version has the full functionality, including a GUI and user input. I do not know how to make a standalone executable (I tried, but it ended up giving me ~1 GB of dependencies that needed to be distributed alongside the .exe, which feels like it defeats the point). The downside is that it requires the user to have Python installed on their machine, as well as 3 libraries (numpy, matplotlib, and dearpygui). pip makes this easy to do, but I wish that burden didn't fall on the user.

Volume 2 is reduced rather significantly, most importantly by removing the GUI components, and as such removing any dependency on the dearpygui package, which is far and away the least common. Anyone running this, i.e. Zach and MAYBE Dr. Young, will have numpy and matplotlib installed already. The downside is that the values of E_x, E_y, phi_x, and phi_y must be changed manually in the code, without a cool GUI. I could have the input be done through the console, but that's ultimately not much prettier than just doing in the .py file itself.
