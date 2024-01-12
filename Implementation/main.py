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
        self.grid()
        self.guard = None

        #label = ttk.Label(self, text="Tab 0")
        #label.grid(column=0, row=0)
        
        self.create_ui()
        self.content_update()


    def create_ui(self):

        #if self.guard == image_paths: 
        #   return
        #self.guard = image_paths

        ### UDAŁO MI SIĘ TO ZROBIĆ, ALE MAM PROBLEM Z WRZUCANIEM NAZW PLIKÓW DO ZMIENNYCH... CIĄGLE COŚ :( 
        ###Jakby co to mam sposób na ogarnięcie tego w sposób łopatologiczny aby działał, ale nie jestem z niego zadowolony, 
        ##tak więc w ostateczności możemy z niego skorzystać

        # Load images
        self.image1 = tk.StringVar()
        self.image2 = tk.StringVar()
        self.image3 = tk.StringVar()
        self.image4 = tk.StringVar()
        self.image1 = '0.png'
        self.image2 = '1.png'
        self.image3 = '2.png'
        self.image4 = '3.png'



        self.image_paths = [self.image1, self.image2, self.image3, self.image4]


        self.images = [Image.open(path) for path in self.image_paths]

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
        self.display.grid(row=0, column=0, padx=5, pady=5)


        start_button = ttk.Button(self, text="Start", command=self.start)
        start_button.grid(column=15, row=0, padx=0, pady=0)

        # stop_button = ttk.Button(self, text="Stop", command=self.stop)
        # stop_button.grid(column=1, row=1, padx=10, pady=0)

        # restart_button = ttk.Button(self, text="Restart", command=self.restart)
        # restart_button.grid(column=2, row=1, padx=10, pady=0)

        # rewind_button = ttk.Button(self, text="Rewind", command=self.rewind)
        # rewind_button.grid(column=3, row=1, padx=10, pady=0)



    def start(self):
        print(self.image_path_1.get())

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


        self.create_ui()
        self.content_update()

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

        #tu będą wartości i jednostki 

        self.current_temperature_label = ttk.Label(self, text="Current temperature: ")
        self.current_temperature_label.grid(column=0, row=0, padx=(0, 5), pady=5)


        self.current_temperature_changes_label = ttk.Label(self, text="Current temperature changes: ")
        self.current_temperature_changes_label.grid(column=0, row=1, padx=(0, 5), pady=5)


        self.water_level_label = ttk.Label(self, text="Water level: ")
        self.water_level_label.grid(column=0, row=2, padx=(0, 5), pady=5)


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

        self.create_ui()

    def create_ui(self):
        dir_var = tk.Variable(value=constants.plot_names)
        self.graphs_list = tk.Listbox(self, listvariable=dir_var, height=6, width=30, selectmode=tk.SINGLE)
        self.graphs_list.grid(column=0, row=0)
        self.graphs_list.select_set(0)

        self.fig = Figure(figsize=(5, 4), dpi=100)
        self.ax = self.fig.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_ylim((0, 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().grid(column=1, row=0, columnspan=2)

        
    def content_update(self):
        pass


sim_frames = list(globals()[c] for c, x in globals().copy().items() if re.match('.*Frame$', c))
# create list of class types defined in this scope

simulation_sampling_rate = constants.simulation_default_sampling

def logic_thread(root):
    
    simulation_counter = 0
    tick_counter = 0
    counter = 0
    graph_select_old, graph_select_new = root.notebook_frames[3].graphs_list.curselection()[0], root.notebook_frames[3].graphs_list.curselection()[0]
    operators = functions.Functions(1000/simulation_sampling_rate, 1)
    root.notebook_frames[1].my_scale.set(2000)
    operators.heatinginitialize(20, root.notebook_frames[1].my_scale.get())
    scale_sample = []
    #operators.pouringinitialize(1, 0, 0)
    operators.V = 10 / 1000
    while 1:
        root.notebook_frames[0].image_paths = ['0.png', '1.png', '2.png', '3.png']
        if ( simulation_counter >= 1000/simulation_sampling_rate):
            #root.notebook_frames[0].create_ui(image_paths) #sposób łopatologiczny niezadawalający
            simulation_counter = 0
            operators.heatingupwater()
            operators.gettingpower(root.notebook_frames[1].my_scale.get())
            scale_sample.append(root.notebook_frames[1].my_scale.get())   
            #adding labels with current temperature and water level
            root.notebook_frames[2].current_temperature_label.configure(text=f"Current temperature: {operators.temperatures[-1]} °C") #zmieniłem zmienną bo nie działało ograniczenie na 100*C i leciało to do góry
            root.notebook_frames[2].water_level_label.configure(text=f"Water level: {operators.V} m^3")
            counter += 1

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

        sleep(constants.simulation_tick/1000)
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

def display_image(root, image1, image2, image3, image4):#funkcja do podmiany zdjęć ale nie działa, część usunąłem
    root.image1.set(image1)
    root.image2.set(image2)
    root.image3.set(image3)
    root.image4.set(image4)
    

if __name__ == "__main__":
    main = MainWindow()
    secondary_thread = Thread(target=logic_thread, daemon=True, args=(main,))
    secondary_thread.start()
    main.mainloop()

