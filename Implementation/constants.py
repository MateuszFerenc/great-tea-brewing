if __name__ == "__main__":
    exit(-1)

window_width = 1250                             #  width of the window, can be changed if desired, be aware of layout misplace wheen changing width or height value
window_height = 750                             #  height of the window
window_background_color = "#BBBBBB"             #  some random background color, can be changed if desired
entry_background_color = "#AAAAAA"

simulation_tick = 10                            # ms, amount of time for one tick of simulation
simulation_default_sampling = 10                # samples per second, 1000 ms / sampling = one sample time (ms) [1000ms/5=200ms => 200ms/10ms=20 simulation ticks per sample]
graph_update_time = 500                         # ms, amount of time before next plot (graph) update
simulation_rewind_delay = 10*40000                    # us, amount of time to sleep in loop during rewind mode
assert type(simulation_default_sampling) is int
assert type(simulation_tick) is int
assert (1000/simulation_default_sampling) >= simulation_tick

# names of the plots
plot_names = {
    "water_temp": "Water Temperature", 
    "heat_pwr": "Heater Power", 
    "water_lvl": "Water Level"
    }

# simulator states
class SimulatorStates:
    RUNNING = 'running'
    STOPPED = 'stopped'
    PAUSED = 'paused'
    REWIND = 'rewind'
    RESTART = 'restart'
    DATA = 'data'       # temporally, remove upon release
    READY = 'ready'     # temporally, remove upon release

# process states
class ProcessStates:
    IDLE = 0
    FILLING = 1
    HEATING = 2
    DRAINING = 3


# entry names
SAMPLES_ENTRY = 'samples_entry'
WATER_ITEMP = 'water_initial_temperature_entry'
WATER_TTEMP = 'water_target_temperature_entry'
BOILER_HEIGHT = 'boiler_height_entry'
BOILER_WIDTH = 'boiler_width_entry'
BOILER_DEPTH = 'boiler_depth_entry'
HEATER_EFFICIENCY = 'heater_efficiency_entry'
WATER_AMOUNT = 'desired_water_amount_entry'
INTAKE_FLOW = 'intake_valve_flow_entry'
OUTTAKE_FLOW = 'outtake_valve_flow_entry'



# available entries: format, min, max, float_type, time_type
entries_validation_dict = {
    SAMPLES_ENTRY: {
        "format": "^[0-9]{1,3}$",
        "min": 1,
        "max": 1000//simulation_tick
    },
    WATER_ITEMP: {
        "format": "^[0-9]{1,2}$",
        "min": 0,
        "max": 45
    },
    WATER_TTEMP: {
        "format": "^[0-9]{1,3}$",
        "min": 50,
        "max": 100
    },
    BOILER_HEIGHT: {
        "format": "^[0-9]{1,3}$",
        "min": 10,
        "max": 300
    },
    BOILER_WIDTH: {
        "format": "^[0-9]{1,3}$",
        "min": 10,
        "max": 300
    },
    BOILER_DEPTH: {
        "format": "^[0-9]{1,3}$",
        "min": 10,
        "max": 300
    },
    HEATER_EFFICIENCY: {
        "format": "^[0-9]{1,2}$",
        "min": 1,
        "max": 99
    },
    WATER_AMOUNT: {
        "format": "^[0-9]+$",
        "min": 1,
        "max": 27000
    },
    INTAKE_FLOW: {
        "format": "^[0-9]{1,2}$",
        "min": 0,
        "max": 2000
    },
    OUTTAKE_FLOW: {
        "format": "^[0-9]{1,2}$",
        "min": 0,
        "max": 2000
    }
}

entries_validation_dict[WATER_AMOUNT]["max"] = (
    ( 
        entries_validation_dict[BOILER_HEIGHT]["max"] *
        entries_validation_dict[BOILER_WIDTH]["max"] *
        entries_validation_dict[BOILER_DEPTH]["max"] 
        ) / 1000
)
