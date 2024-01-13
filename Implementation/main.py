import tkinter as tk
import tkinter.ttk as ttk
from tkinter import ttk
import functions
import constants
import re
from threading import Thread
from time import sleep
import functions

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

from PIL import Image, ImageTk
import os
from pathlib import Path


def get_center(parent, axis, val):
    assert axis in ['x', 'y']
    ax = {"x": parent.winfo_screenwidth(), "y": parent.winfo_screenheight()}
    return int(ax[axis] / 2 - val / 2)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.alive = True
        self.__drawmain__()

    def on_closing(self):
        self.alive = False
        self.destroy()

    def __drawmain__(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')

        self.style.theme_settings(self.style.theme_use(), {
            "frames_notebook.TNotebook": {
                "configure": {"tabposition": 'n', "tabmargins": (2, 5, 2, 0)},
            },
            "frames_notebook.TNotebook.Tab": {
                "configure": {"padding": [10, 5]},
                "map":       {
                "padding": [("selected", [20,10])] 
                }
            }
            })
        
        self.title("Tea Brewing Simulator")
        self.geometry(f"{constants.window_width}x{constants.window_height}+"
                      f"{get_center(self, 'x', constants.window_width)}+{get_center(self, 'y', constants.window_height)}")
        self.resizable(False, False)
        self.configure(bg=constants.window_background_color)

        self.grid()

        self.notebook = ttk.Notebook(self, takefocus=False, width=constants.window_width, height=constants.window_height, style="frames_notebook.TNotebook")
        self.notebook.grid(column=0, row=0)

        self.notebook_frames = []
        for win_frame in sim_frames:
            frame = win_frame(parent=self)
            frame.grid(sticky=tk.NSEW)
            self.notebook.add(frame, text=frame.name)
            self.notebook_frames.append(frame)
            

class SimulationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Simulation"
        self.long_name = "SimulationFrame"
        self.parent = parent
        self.grid(column=4, row=2)

        self.simulation_state = constants.STOPPED
        
        self.create_ui()

    def create_ui(self):
           # Load images
        self.image1 = tk.StringVar(value='0.png')
        self.image2 = tk.StringVar(value='1.png')
        self.image3 = tk.StringVar(value='2.png')
        self.image4 = tk.StringVar(value='3.png')


        self.image_paths = [self.image1, self.image2, self.image3, self.image4]

        self.images = [Image.open(path.get()) for path in self.image_paths]

        # Resize images to the same dimensions
        width, height = 600, 600
        self.images = [img.resize((width, height), Image.LANCZOS) for img in self.images]

        # Create an empty image with an alpha channel
        self.result_image = Image.new('RGBA', (width, height), (0, 0, 0, 0))

        # Paste images onto the result image, considering alpha channel
        positions = [(0, 0), (0, 0), (0, 0), (0, 0)]
        for img, pos in zip(self.images, positions):
            self.result_image.paste(img, pos, img)

        # # Convert the result to Tkinter PhotoImage
        self.tk_image = ImageTk.PhotoImage(self.result_image)

        # Create label to display the overlaid image
        self.display = ttk.Label(self, image=self.tk_image)
        self.display.grid(column=0, row=0, sticky=tk.EW)


        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.start_button.grid(column=0, row=1, sticky=tk.S)

        self.pause_button = ttk.Button(self, text="Pause", command=self.pause, state=tk.DISABLED)
        self.pause_button.grid(column=1, row=1, sticky=tk.S)

        self.restart_button = ttk.Button(self, text="Restart", command=self.restart, state=tk.DISABLED)
        self.restart_button.grid(column=2, row=1, sticky=tk.S)

        self.rewind_button = ttk.Button(self, text="Rewind", command=self.rewind)
        self.rewind_button.grid(column=3, row=1, sticky=tk.S)

        self.timer_label = ttk.Label(self, text="Time: --- min -- s --- ms")
        self.timer_label.grid(column=4, row=1, sticky=tk.SE)

    def start(self):
        self.simulation_state = constants.RUNNING
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.ACTIVE)
        self.restart_button.configure(state=tk.ACTIVE)
        self.rewind_button.configure(state=tk.DISABLED)

    def pause(self):
        self.simulation_state = constants.PAUSED
        self.start_button.configure(state=tk.ACTIVE)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.ACTIVE)

    def restart(self):
        self.simulation_state = constants.RESTART
        self.start_button.configure(state=tk.ACTIVE)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.DISABLED)
        self.rewind_button.configure(state=tk.ACTIVE)

    def rewind(self):
        self.simulation_state = constants.REWIND
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.ACTIVE)
        self.parent.notebook.tab(1, state=tk.DISABLED)
        self.parent.notebook.tab(2, state=tk.DISABLED)
        self.parent.notebook.tab(3, state=tk.DISABLED)

class InputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Inputs"
        self.long_name = "InputsFrame"
        self.parent = parent
        self.grid()
        
        self.create_ui()

    def create_ui(self):
        input_label = ttk.Label(self, text="Heater Temperature: ")
        input_label.grid(column=0, row=0, padx=(0, 5))

        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(column=1, row=0)

        # output label field
        output_label = ttk.Label(self, text="Pouring in: ")
        output_label.grid(column=0, row=1, padx=(0, 5), pady=(10, 0))
        
        self.output_entry = ttk.Entry(self)
        self.output_entry.grid(column=1, row=1)

        self.input_entry = ttk.Entry(self)
        self.input_entry.grid(column=1, row=0)

        # heater_temperature label field
        heater_temperature_label = ttk.Label(self, text="Heater temperature: ")
        heater_temperature_label.grid(column=0, row=2, padx=(0, 5), pady=(10, 0))

        self.heater_temperature_entry = ttk.Entry(self)
        self.heater_temperature_entry.grid(column=1, row=2)

        #Power slider
        heater_power_label = ttk.Label(self, text="Heating power: ")
        heater_power_label.grid(column=0, row=4, padx=(0, 5), pady=(20, 0))
        self.my_scale=tk.Scale(self, orient="horizontal",cursor="dot", from_=500, to= 10000, length = 400, resolution = 100)
        self.my_scale.grid(column=1, row=4, padx=0, pady=0)

        # Water-in slider
        water_in_label = ttk.Label(self, text="Pouring water in level: ")
        water_in_label.grid(column=0, row=5, padx=(0, 5), pady=(20, 0))
        self.water_in=tk.Scale(self, orient="horizontal",cursor="dot", from_=500, to= 10000, length = 400, resolution = 100)
        self.water_in.grid(column=1, row=5, padx=0, pady=0)

        # Water-out slider
        water_out_label = ttk.Label(self, text="Pouring water out level: ")
        water_out_label.grid(column=0, row=6, padx=(0, 5), pady=(20, 0))
        self.water_out=tk.Scale(self, orient="horizontal",cursor="dot", from_=500, to= 10000, length = 400, resolution = 100)
        self.water_out.grid(column=1, row=6, padx=0, pady=0)


class OutputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Outputs"
        self.long_name = "OutputsFrame"
        self.parent = parent
        self.grid()

        #tu będą wartości i jednostki 

        self.current_temperature_label = ttk.Label(self, text="Current temperature: ")
        self.current_temperature_label.grid(column=0, row=0, padx=(0, 5), pady=5)


        self.current_temperature_changes_label = ttk.Label(self, text="Current temperature changes: ")
        self.current_temperature_changes_label.grid(column=0, row=1, padx=(0, 5), pady=5)


        self.water_level_label = ttk.Label(self, text="Water level: ")
        self.water_level_label.grid(column=0, row=2, padx=(0, 5), pady=5)


    def create_ui(self):
        pass

class GraphsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Graphs"
        self.long_name = "GraphsFrame"
        self.parent = parent
        self.grid()

        self.create_ui()

    def create_ui(self):
        dir_var = tk.Variable(value=constants.plot_names)
        self.graphs_list = tk.Listbox(self, listvariable=dir_var, height=6, width=30, selectmode=tk.SINGLE)
        self.graphs_list.grid(column=0, row=0)
        self.graphs_list.select_set(0)

        self.fig = Figure(figsize=(7, 5), dpi=100)
        self.ax = self.fig.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_ylim((0, 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(column=1, row=0, columnspan=2)




sim_frames = list(globals()[c] for c, x in globals().copy().items() if re.match('.*Frame$', c))
# create list of class types defined in this scope

simulation_sampling_rate = constants.simulation_default_sampling

def logic_thread(root):
    simulation_counter = 0
    tick_counter = 0
    simulation_state = constants.STOPPED
    graph_select_old, graph_select_new = root.notebook_frames[3].graphs_list.curselection()[0], root.notebook_frames[3].graphs_list.curselection()[0]
    ms, sec, min = 0, 0, 0
    
    operators = functions.Functions(simulation_sampling_rate, 1000)
    root.notebook_frames[1].my_scale.set(2000)
    operators.heatinginitialize(20, root.notebook_frames[1].my_scale.get())
    scale_sample = []
    while 1:
        simulation_state = root.notebook_frames[0].simulation_state
        if ( simulation_counter >= 1000/simulation_sampling_rate and simulation_state == constants.RUNNING):
            simulation_counter = 0
            operators.heatingupwater()
            operators.gettingpower(root.notebook_frames[1].my_scale.get())
            scale_sample.append(root.notebook_frames[1].my_scale.get())   
            root.notebook_frames[2].current_temperature_label.configure(text=f"Current temperature: {operators.T_2} °C")
            root.notebook_frames[2].water_level_label.configure(text=f"Water level: {operators.V} m^3")

        if ( tick_counter > 65000):
            tick_counter = 0
        
        # check if a other graph was selected, if so change displayed graph
        graph_select_new = root.notebook_frames[3].graphs_list.curselection()[0]
        if ( ( graph_select_new != graph_select_old ) or not ( tick_counter * constants.simulation_tick ) % constants.graph_update_time ):
            if root.notebook_frames[3].graphs_list.get(graph_select_new) == "Water Temperature":
                display_water_temperature_graph(root.notebook_frames[3], operators.samples, operators.temperatures)
            elif root.notebook_frames[3].graphs_list.get(graph_select_new) == "Heater Power":
                display_heater_power_graph(root.notebook_frames[3], operators.samples, scale_sample)
        graph_select_old = graph_select_new

        if simulation_state == constants.RESTART:
            root.notebook_frames[0].simulation_state = constants.STOPPED
            simulation_state = constants.STOPPED
            ms, sec, min = 0, 0, 0
            root.notebook_frames[0].timer_label.configure(text=f"Time: --- min -- s --- ms")

        if simulation_state == constants.RUNNING:
            ms, sec, min = count_time(ms, sec, min, ms_incr=constants.simulation_tick)

        if simulation_state != constants.REWIND:
            if simulation_state == constants.RUNNING:
                root.notebook_frames[0].timer_label.configure(text=f"Time: {min:003n} min {sec:02n} s {ms:003n} ms")

            # validate
            sleep(constants.simulation_tick/1000)
        else:
            #rewind
            if not operators.temp_reached_target():
                operators.heatingupwater()
            else:
                root.notebook_frames[0].simulation_state = constants.STOPPED
                root.notebook_frames[0].restart()
                root.notebook.tab(1, state=tk.NORMAL)
                root.notebook.tab(2, state=tk.NORMAL)
                root.notebook.tab(3, state=tk.NORMAL)

        simulation_counter += constants.simulation_tick
        tick_counter += 1
        
def display_water_temperature_graph(root, x_vals, y_vals):
    root.ax.clear()
    root.ax.plot(x_vals, y_vals, color="r")
    root.ax.set_ylim((0, 125))
    root.ax.set_xlabel("time [s]")
    root.ax.set_ylabel("T [°C]")
    root.ax.set_title(label="Water Temperature")
    root.ax.grid(visible=True, linestyle=':', linewidth=0.5)
    #root.ax.legend()
    root.canvas.draw()

def display_heater_power_graph(root, x_vals, y_vals):
    root.ax.clear()
    root.ax.plot(x_vals, y_vals, color="r")
    root.ax.set_ylim((500, 10000))
    root.ax.set_xlabel("time [s]")
    root.ax.set_ylabel("P [W]")
    root.ax.set_title(label="Heater Power")
    root.ax.grid(visible=True, linestyle=':', linewidth=0.5)
    #root.ax.legend()
    root.canvas.draw()

def count_time(ms: int, sec: int, min: int, ms_incr: int = 0, sec_inc: int = 0, min_incr: int = 0):
    ms += ms_incr
    d_ms = ms // 1000
    ms -= d_ms * 1000
    sec += sec_inc + d_ms
    d_sec = sec // 60
    ms -= d_sec * 60
    min += min_incr + d_sec
    return ms, sec, min
 

if __name__ == "__main__":
    main = MainWindow()
    secondary_thread = Thread(target=logic_thread, daemon=True, args=(main,))
    secondary_thread.start()
    main.mainloop()

