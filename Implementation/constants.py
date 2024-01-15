if __name__ == "__main__":
    exit(-1)

window_width = 1250                             #  width of the window, can be changed if desired, be aware of layout misplace wheen changing width or height value
window_height = 750                             #  height of the window
window_background_color = "#BBBBBB"             # some random background color, can be changed if desired
entry_background_color = "#AAAAAA"

simulation_tick = 10                            # ms, amount of time for one tick of simulation
simulation_default_sampling = 10                 # samples per second, 1000 ms / sampling = one sample time (ms) [1000ms/5=200ms => 200ms/10ms=20 simulation ticks per sample]
graph_update_time = 500                         # ms, amount of time before next plot (graph) update
assert type(simulation_default_sampling) is int
assert type(simulation_tick) is int
assert (1000/simulation_default_sampling) >= simulation_tick

plot_names = ("Water Temperature", "Heater Power")
RUNNING = 'running'
STOPPED = 'stopped'
PAUSED = 'paused'
REWIND = 'rewind'
RESTART = 'restart'

SAMPLES_ENTRY = 'samples_entry'
WATER_ITEMP = 'water_initial_temperature_entry'
WATER_TTEMP = 'water_target_temperature_entry'
BOILER_HEIGHT = 'boiler_height_entry'
BOILER_WIDTH = 'boiler_width_entry'
BOILER_DEPTH = 'boiler_depth_entry'
HEATER_EFFICIENCY = 'heater_efficiency_entry'
WATER_AMOUNT = 'desired_water_amount_entry'