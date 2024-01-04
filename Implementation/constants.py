if __name__ == "__main__":
    exit(-1)

window_width = 800          #  width of the window, can be changed if desired, be aware of layout misplace wheen changing width or height value
window_height = 500         #  height of the window
window_background_color = "#BBBBBB"     # some random background color, can be changed if desired
simulation_tick = 10        # ms, amount of time for one tick of simulation
simulation_default_sampling = 5    # samples per second, 1000 ms / sampling = one sample time (ms) [1000ms/50=20ms => 4 simulation ticks per sample]
assert type(simulation_default_sampling) is int
#assert 1 <= simulation_default_sampling < simulation_tick