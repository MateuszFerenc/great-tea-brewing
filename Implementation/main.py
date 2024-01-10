import tkinter as tk
import tkinter.ttk as ttk
import functions
import constants
import re
from threading import Thread
from time import sleep


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
            }})
        
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
        self.grid()

        #label = ttk.Label(self, text="Tab 0")
        #label.grid(column=0, row=0)
        
        self.create_ui()
        self.content_update()

    def create_ui(self):

        #button_position = ttk.Label(self)
        #button_position.grid(column=0, row=1, columnspan=4, pady=50)

        start_button = ttk.Button(self, text="Start", command=self.start)
        start_button.grid(column=0, row=1, padx=55, pady=400)

        stop_button = ttk.Button(self, text="Stop", command=self.stop)
        stop_button.grid(column=1, row=1, padx=55, pady=0)

        restart_button = ttk.Button(self, text="Restart", command=self.restart)
        restart_button.grid(column=2, row=1, padx=55, pady=0)

        rewind_button = ttk.Button(self, text="Rewind", command=self.rewind)
        rewind_button.grid(column=3, row=1, padx=55, pady=0)

    def content_update(self):
        pass

    def start(self):
        print("Start")

    def stop(self):
        print("Stop")

    def restart(self):
        print("Restart")

    def rewind(self):
        print("Rewind")

class InputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Inputs"
        self.long_name = "InputsFrame"
        self.parent = parent
        self.grid()

        #label = ttk.Label(self, text="water level: ")
        #label.grid(column=0, row=0)

        #self.input_entry = ttk.Entry(self)
        #self.input_entry.grid(column=1, row=0)

        #label2 = ttk.Label(self, text="temperature: ")
        #label2.grid(column=0, row=0)

        #self.input_entry2 = ttk.Entry(self)
        #self.input_entry2.grid(column=1, row=0)

        water_level_label = ttk.Label(self, text="Water Level:")
        water_level_label.grid(column=0, row=0, padx=(0, 5))

        self.water_level_entry = ttk.Entry(self)
        self.water_level_entry.grid(column=1, row=0)

        # Temperature label and input field
        temperature_label = ttk.Label(self, text="Temperature:")
        temperature_label.grid(column=0, row=1, padx=(0, 5), pady=(10, 0))

        self.temperature_entry = ttk.Entry(self)
        self.temperature_entry.grid(column=1, row=1)

        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class ControlFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Control"
        self.long_name = "ControlFrame"
        self.parent = parent
        self.grid()

        label = ttk.Label(self, text="Tab 2")
        label.grid(column=0, row=0)
        self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class OutputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Outputs"
        self.long_name = "OutputsFrame"
        self.parent = parent
        self.grid()

        #label = ttk.Label(self, text="Tab 3")
        #label.grid(column=0, row=0)
        # self.create_ui()
        # self.content_update()

        parameter1_label = ttk.Label(self, text="Parameter 1: ")
        parameter1_label.grid(column=0, row=0, padx=(0, 5), pady=5)

        #tu będą wartości i jednostki 

        parameter2_label = ttk.Label(self, text="Parameter 2: ")
        parameter2_label.grid(column=0, row=1, padx=(0, 5), pady=5)

        parameter3_label = ttk.Label(self, text="Parameter 3: ")
        parameter3_label.grid(column=0, row=2, padx=(0, 5), pady=5)

    def create_ui(self):
        pass

    def content_update(self):
        pass

class GraphsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Graphs"
        self.long_name = "GraphsFrame"
        self.parent = parent
        self.grid()

        label = ttk.Label(self, text="Tab 4")
        label.grid(column=0, row=0)
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass


sim_frames = list(globals()[c] for c, x in globals().copy().items() if re.match('.*Frame$', c))
# create list of class types defined in this scope

simulation_sampling_rate = constants.simulation_default_sampling

def logic_thread(root):
    simulation_counter = 0
    counter = 0
    while 1:
        if ( simulation_counter >= 1000/simulation_sampling_rate):
            print("One sample")
            simulation_counter = 0
            functions.heatingUpWater(counter)
            counter += 1
            print (counter, " ")
        sleep(constants.simulation_tick/1000)
        simulation_counter += constants.simulation_tick
        
        #root.notebook_frames[0].label.configure(text=simulation_counter)
        

if __name__ == "__main__":
    main = MainWindow()
    secondary_thread = Thread(target=logic_thread, daemon=True, args=(main,))
    secondary_thread.start()
    main.mainloop()