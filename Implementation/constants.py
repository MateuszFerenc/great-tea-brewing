if __name__ == "__main__":
    exit(-1)

window_width = 1400          #  width of the window, can be changed if desired, be aware of layout misplace wheen changing width or height value
window_height = 800         #  height of the window
window_background_color = "#BBBBBB"     # some random background color, can be changed if desired
simulation_tick = 10        # ms, amount of time for one tick of simulation
simulation_default_sampling = 10   # samples per second, 1000 ms / sampling = one sample time (ms) [1000ms/5=200ms => 200ms/10ms=20 simulation ticks per sample]
assert type(simulation_default_sampling) is int
assert type(simulation_tick) is int
assert (1000/simulation_default_sampling) >= simulation_tick

