import tkinter as tk
import tkinter.ttk as ttk
from tkinter import messagebox
import functions
import constants
import re
from threading import Thread
from time import sleep
from os.path import join

from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib
matplotlib.use("TkAgg")

from PIL import Image, ImageTk


def get_center(parent, axis, val):
    assert axis in ['x', 'y']
    ax = {"x": parent.winfo_screenwidth(), "y": parent.winfo_screenheight()}
    return int(ax[axis] / 2 - val / 2)


class my_Entry(ttk.Entry):
    def __init__(self, master=None, lc_command=None, **kw) -> None:

        background = kw.pop('background', ...)
        foreground = kw.pop('foreground', ...)
        selectforeground = kw.pop('selectforeground', ...)
        font = kw.pop('font', None)

        super().__init__(master, **kw)

        self.style_name = self._name + ".TEntry"

        self.style = ttk.Style(master)
        background = self.style.lookup("TEntry", "fieldbackground") if background is ... else background
        foreground = self.style.lookup("TEntry", "foreground") if foreground is ... else foreground
        selectforeground = self.style.lookup("TEntry", "selectforeground") if selectforeground is ... else selectforeground
        self.style.configure(style=self.style_name, background=background, fieldbackground=background, foreground=foreground,
                             font=font, selectforeground=selectforeground)
        self.configure(style=self.style_name)

        if lc_command is not None:
            self.bind("<Button-3>", func=lc_command)

def my_showinfo(title: str, obj_name: str, entry_dict: dict):
    entry = entry_dict[title]
    msg =   f"{obj_name} entry properties:\n"\
            f"- min: {entry['min']}\n"\
            f"- max: {entry['max']}\n"
    if 'float_type' in entry.keys():
        msg += "- Floating point type"
    elif 'time_type' in entry.keys():
        msg += "- Time type"
    else:
        msg += "- Integer type"
    messagebox.showinfo(title=title, message=msg)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.protocol("WM_DELETE_WINDOW", self.on_closing)
        self.alive = True

        self.style = ttk.Style()
        self.style.theme_use('clam')
        self.style.theme_settings(self.style.theme_use(), {
            "frames_notebook.TNotebook": {
                "configure": {
                    "tabposition": 'n', 
                    "tabmargins": (2, 5, 2, 0)
                },
            },
            "frames_notebook.TNotebook.Tab": {
                "configure": {
                    "padding": [10, 5],
                    "font": ("Consolas", 15, "bold")
                },
                "map": {
                    "padding": [("selected", [20,10])]
                }
            },
            "TLabel": {
                "configure": {
                    "background": constants.window_background_color,
                    "font": ("Consolas", 10, "bold")
                }
            },
            "TScale": {
                "configure": {
                    "background": constants.window_background_color,
                    "font": ("Consolas", 10, "bold")
                }
            },
            "TEntry": {
                "configure": {
                    "fieldbackground ": constants.entry_background_color, 
                    "selectbackground" : "#000000"
                }
            },
            "LittleFrame.TFrame": {
                "configure": {
                    "background": constants.window_background_color
                }
            },
            "TButton": {
                "configure": {
                    "font": ("Consolas", 10, "bold")
                }
            },
            "pstates.TFrame": {
                "configure": {
                    "background": "#999999"
                }
            },
            "statistics.TFrame": {
                "configure": {
                    "background": "#999999"
                }
            },
            "statistics.TLabel": {
                "configure": {
                    "background": "#999999",
                    "font": ("Consolas", 10, "bold")
                }
            }
            })
        
        self.__drawmain__()

    def on_closing(self):
        self.alive = False
        self.destroy()

    def __drawmain__(self):
        self.title("Tea Brewing Simulator")
        self.geometry(f"{constants.window_width}x{constants.window_height}+"
                      f"{get_center(self, 'x', constants.window_width)}+{get_center(self, 'y', constants.window_height)}")
        self.resizable(False, False)
        self.configure(bg=constants.window_background_color)

        
        self.notebook = ttk.Notebook(self, takefocus=False, width=constants.window_width, height=constants.window_height, style="frames_notebook.TNotebook")
        self.notebook.grid(column=0, row=1)

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
        self.configure(background=constants.window_background_color)

        self.simulation_state = constants.SimulatorStates.STOPPED

        self.heater_image_last_state = 20
        self.fill_image_last_state = 20
        self.drain_image_last_state = 20
        self.water_image_last_state = 20
        
        self.create_ui()

    def create_ui(self):
        self.assets_directory = join('Assets', 'images')

        self.heater_image_path = join(self.assets_directory, 'heater_temperature')
        self.fill_image_path = join(self.assets_directory, 'pouring_in')
        self.drain_image_path = join(self.assets_directory, 'pouring_out')
        self.water_image_path = join(self.assets_directory, 'water_level')

        self.image_width = 800
        self.image_height = 640

        self.schematic = ttk.Label(self, image=None, borderwidth=1, relief='solid')
        self.schematic.grid(column=0, row=0, columnspan=4, sticky=tk.NW)

        self.update_schematic()


        self.start_button = ttk.Button(self, text="Start", command=self.start)
        self.start_button.grid(column=0, row=1, sticky=tk.NSEW)

        self.pause_button = ttk.Button(self, text="Pause", command=self.pause, state=tk.DISABLED)
        self.pause_button.grid(column=1, row=1, sticky=tk.NSEW)

        self.restart_button = ttk.Button(self, text="Restart", command=self.restart, state=tk.DISABLED)
        self.restart_button.grid(column=2, row=1, sticky=tk.NSEW)

        self.rewind_button = ttk.Button(self, text="Rewind", command=self.rewind)
        self.rewind_button.grid(column=3, row=1, sticky=tk.NSEW)

        self.timer_label = ttk.Label(self, text="Time: --- min -- s --- ms")
        self.timer_label.grid(column=4, row=1, padx=(30,0), pady=(0, 0), sticky=tk.E)

        ttk.Label(self, text="Sample rate: \t samples/s").grid(column=5, row=1, padx=(20, 0), pady=(0, 0), sticky=tk.E)
        my_Entry(self, width=3, name=constants.SAMPLES_ENTRY, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.SAMPLES_ENTRY, obj_name="Sample rate", entry_dict=constants.entries_validation_dict)).grid(column=5, row=1, padx=(110, 0), pady=(0, 0), ipadx=0, sticky=tk.W)

        self.process_states_board_frame = ttk.Frame(self, style="pstates.TFrame")
        self.process_states_board_frame.grid(column=4, row=0, columnspan=2, padx=(40, 0), pady=(40, 0), sticky=tk.NW)
        ttk.Label(self.process_states_board_frame, text="Process states:", background="#999999").grid(column=0, row=0, columnspan=2, padx=(10, 0), pady=(10, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="●", name="ps_run", background="#999999", font=(20)).grid(column=0, row=1, padx=(20, 0), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="RUN", background="#999999").grid(column=1, row=1, padx=(10, 20), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="●", name="ps_fill", background="#999999", font=(20)).grid(column=0, row=2, padx=(20, 0), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="Boiler fill", background="#999999").grid(column=1, row=2, padx=(10, 20), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="●", name="ps_drain", background="#999999", font=(20)).grid(column=0, row=3, padx=(20, 0), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="Boiler draining", background="#999999").grid(column=1, row=3, padx=(10, 20), pady=(0, 0), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="●", name="ps_heat", background="#999999", font=(20)).grid(column=0, row=4, padx=(20, 0), pady=(0, 10), sticky=tk.W)
        ttk.Label(self.process_states_board_frame, text="Heating", background="#999999").grid(column=1, row=4, padx=(10, 20), pady=(0, 10), sticky=tk.W)

        # temporally, remove upon release
        self.temporary_button = ttk.Button(self.process_states_board_frame, text="Fill test data", command=self.fill_test_data)
        self.temporary_button.grid(column=0, row=5, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=tk.NW)

    def fill_test_data(self):   # temporally, remove upon release
        self.simulation_state = constants.SimulatorStates.DATA

    def start(self):
        self.simulation_state = constants.SimulatorStates.RUNNING
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.ACTIVE)
        self.restart_button.configure(state=tk.ACTIVE)
        self.rewind_button.configure(state=tk.DISABLED)

    def pause(self):
        self.simulation_state = constants.SimulatorStates.PAUSED
        self.start_button.configure(state=tk.ACTIVE)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.ACTIVE)

    def restart(self):
        self.simulation_state = constants.SimulatorStates.RESTART
        self.start_button.configure(state=tk.ACTIVE)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.DISABLED)
        self.rewind_button.configure(state=tk.ACTIVE)
        self.parent.notebook.tab(1, state=tk.NORMAL)
        self.parent.notebook.tab(2, state=tk.NORMAL)
        self.parent.notebook.tab(3, state=tk.NORMAL)

    def rewind(self):
        self.simulation_state = constants.SimulatorStates.REWIND
        self.start_button.configure(state=tk.DISABLED)
        self.pause_button.configure(state=tk.DISABLED)
        self.restart_button.configure(state=tk.ACTIVE)
        self.parent.notebook.tab(1, state=tk.DISABLED)
        self.parent.notebook.tab(2, state=tk.DISABLED)
        self.parent.notebook.tab(3, state=tk.DISABLED)

    def update_schematic(self, heater_state: int = 0, fill_state: int = 0, drain_state: int = 0, water_state: int = 0):
        if any((heater_state != self.heater_image_last_state, fill_state != self.fill_image_last_state, 
               drain_state != self.drain_image_last_state, water_state != self.water_image_last_state)):
            self.heater_image_last_state = heater_state
            self.fill_image_last_state = fill_state
            self.drain_image_last_state = drain_state
            self.water_image_last_state = water_state

            heater_image = Image.open(join(self.heater_image_path, f'{heater_state}.png')).convert("RGBA").resize((self.image_width, self.image_height))
            fill_image = Image.open(join(self.fill_image_path, f'{fill_state}.png')).convert("RGBA").resize((self.image_width, self.image_height))
            drain_image = Image.open(join(self.drain_image_path, f'{drain_state}.png')).convert("RGBA").resize((self.image_width, self.image_height))
            water_image = Image.open(join(self.water_image_path, f'{water_state}.png')).convert("RGBA").resize((self.image_width, self.image_height))

            result_image = Image.new('RGBA', (self.image_width, self.image_height), (0, 0, 0, 0))

            result_image.paste(heater_image, (0, 0), heater_image)
            result_image.paste(fill_image, (0, 0), fill_image)
            result_image.paste(drain_image, (0, 0), drain_image)
            result_image.paste(water_image, (0, 0), water_image)

            self.tk_image = ImageTk.PhotoImage(result_image)

            self.schematic.configure(image=self.tk_image)


class InputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Inputs"
        self.long_name = "InputsFrame"
        self.parent = parent
        self.configure(background=constants.window_background_color)
        
        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Water initial temperature: ").grid(column=0, row=0, padx=(20, 0), pady=(20, 10), sticky=tk.NW)
        water_iT_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_iT_frame.grid(column=1, row=0, padx=20, pady=(20, 10), sticky=tk.NSEW)
        my_Entry(water_iT_frame, width=8, name=constants.WATER_ITEMP, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.WATER_ITEMP, obj_name="Water initial temperature", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_iT_frame, text="°C").grid(column=1, row=0, sticky=tk.NSEW)
        

        ttk.Label(self, text="Water Target Temperature: ").grid(column=0, row=1, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        water_tT_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_tT_frame.grid(column=1, row=1, padx=20, pady=(0, 10), sticky=tk.NSEW)
        my_Entry(water_tT_frame, width=8, name=constants.WATER_TTEMP, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.WATER_TTEMP, obj_name="Water target temperature", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_tT_frame, text="°C").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Boiler dimensions: ").grid(column=0, row=2, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        boiler_dimensions_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        ttk.Label(boiler_dimensions_frame, text="Height: ").grid(column=0, row=0, sticky=tk.NSEW)
        my_Entry(boiler_dimensions_frame, width=4, name=constants.BOILER_HEIGHT, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.BOILER_HEIGHT, obj_name="Height", entry_dict=constants.entries_validation_dict)).grid(column=1, row=0, padx=0, pady=(0, 0), sticky=tk.NSEW)
        ttk.Label(boiler_dimensions_frame, text="cm").grid(column=2, row=0, padx=(0, 10), sticky=tk.NSEW)
        ttk.Label(boiler_dimensions_frame, text="Width: ").grid(column=3, row=0, sticky=tk.NSEW)
        my_Entry(boiler_dimensions_frame, width=4, name=constants.BOILER_WIDTH, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.BOILER_WIDTH, obj_name="Width", entry_dict=constants.entries_validation_dict)).grid(column=4, row=0, padx=0, pady=(0, 0), sticky=tk.NSEW)
        ttk.Label(boiler_dimensions_frame, text="cm").grid(column=5, row=0, padx=(0, 10), sticky=tk.NSEW)
        ttk.Label(boiler_dimensions_frame, text="Depth: ").grid(column=6, row=0, sticky=tk.NSEW)
        my_Entry(boiler_dimensions_frame, width=4, name=constants.BOILER_DEPTH, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.BOILER_DEPTH, obj_name="Depth", entry_dict=constants.entries_validation_dict)).grid(column=7, row=0, padx=0, pady=(0, 0), sticky=tk.NSEW)
        ttk.Label(boiler_dimensions_frame, text="cm").grid(column=8, row=0, padx=(0, 0), sticky=tk.NSEW)
        boiler_dimensions_frame.grid(column=1, row=2, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)

        ttk.Label(self, text="Heater temperature setpoint: ").grid(column=0, row=4, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        heater_setpoint_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        heater_setpoint_frame.grid(column=1, columnspan=2, row=4, padx=20, pady=(0, 10), sticky=tk.NW)
        self.heater_power_scale=tk.Scale(heater_setpoint_frame, orient="horizontal", cursor="plus", from_=constants.entries_validation_dict[constants.WATER_ITEMP]['max'], to= 120, length = 400, resolution = 1, background=constants.window_background_color, highlightthickness=0, font=("Consolas", 10, "bold"), tickinterval=15)
        self.heater_power_scale.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(heater_setpoint_frame, text="°C").grid(column=1, row=0, sticky=tk.NW)

        ttk.Label(self, text="Pouring water in flow: ").grid(column=0, row=5, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        water_intake_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_intake_frame.grid(column=1, columnspan=2, row=5, padx=20, pady=(0, 10), sticky=tk.NW)
        self.water_in_scale=tk.Scale(water_intake_frame, orient="horizontal", cursor="plus", from_=1, to=100, length = 400, resolution = 1, background=constants.window_background_color, highlightthickness=0, font=("Consolas", 10, "bold"), tickinterval=25)
        self.water_in_scale.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_intake_frame, text="%").grid(column=1, row=0, sticky=tk.NW)

        ttk.Label(self, text="Pouring water out flow: ").grid(column=0, row=6, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        water_outtake_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_outtake_frame.grid(column=1, columnspan=2, row=6, padx=20, pady=(0, 20), sticky=tk.NW)
        self.water_out_scale=tk.Scale(water_outtake_frame, orient="horizontal", cursor="plus", from_=1, to= 100, length = 400, resolution = 1, background=constants.window_background_color, highlightthickness=0, font=("Consolas", 10, "bold"), tickinterval=25)
        self.water_out_scale.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_outtake_frame, text="%").grid(column=1, row=0, sticky=tk.NW)

        ttk.Label(self, text="Heater efficiency: ").grid(column=3, row=0, padx=(20, 0), pady=(20, 10), sticky=tk.NW)
        heater_efficiency_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        heater_efficiency_frame.grid(column=4, row=0, padx=20, pady=(20, 10), sticky=tk.NSEW)
        my_Entry(heater_efficiency_frame, width=8, name=constants.HEATER_EFFICIENCY, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.HEATER_EFFICIENCY, obj_name="Heater efficiency", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(heater_efficiency_frame, text="%").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Heater maximum power: ").grid(column=3, row=1, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        heater_pow_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        heater_pow_frame.grid(column=4, row=1, padx=20, pady=(0, 10), sticky=tk.NSEW)
        my_Entry(heater_pow_frame, width=8, name=constants.HEATER_POWER, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.HEATER_POWER, obj_name="Heater maximum power", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(heater_pow_frame, text="kJ").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Desired water amount: ").grid(column=3, row=2, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        water_amount_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_amount_frame.grid(column=4, row=2, padx=20, pady=(0, 10), sticky=tk.NSEW)
        my_Entry(water_amount_frame, width=8, name=constants.WATER_AMOUNT, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.WATER_AMOUNT, obj_name="Desired water amount", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_amount_frame, text="L").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Intake valve flow capacity: ").grid(column=3, row=3, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        invalve_cap_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        invalve_cap_frame.grid(column=4, row=3, padx=20, pady=(0, 10), sticky=tk.NSEW)
        my_Entry(invalve_cap_frame, width=8, name=constants.INTAKE_FLOW, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.INTAKE_FLOW, obj_name="Intake valve flow capacity", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(invalve_cap_frame, text="mL/s").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Outtake valve flow capacity: ").grid(column=3, row=4, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        outvalve_cap_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        outvalve_cap_frame.grid(column=4, row=4, padx=20, pady=(0, 10), sticky=tk.NSEW)
        my_Entry(outvalve_cap_frame, width=8, name=constants.OUTTAKE_FLOW, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.OUTTAKE_FLOW, obj_name="Outtake valve flow capacity", entry_dict=constants.entries_validation_dict)).grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(outvalve_cap_frame, text="mL/s").grid(column=1, row=0, sticky=tk.NSEW)

        self.heater_pid_frame = ttk.Frame(self, style="statistics.TFrame")
        self.heater_pid_frame.grid(column=3, row=5, columnspan=2, rowspan=5, padx=(20, 0), pady=(0, 10), sticky=tk.NW)
        ttk.Label(self.heater_pid_frame, text="Heater PID:", style="statistics.TLabel").grid(column=0, row=0, columnspan=2, padx=(10, 10), pady=(10, 10), sticky=tk.NW)

        ttk.Label(self.heater_pid_frame, text="Kp: ", style="statistics.TLabel").grid(column=0, row=1, padx=(20, 10), pady=(0, 10), sticky=tk.NW)
        my_Entry(self.heater_pid_frame, width=8, name=constants.HEATER_PID_KP, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.HEATER_PID_KP, obj_name="Kp", entry_dict=constants.entries_validation_dict)).grid(column=1, row=1, padx=(0, 10), pady=(0, 0), sticky=tk.NW)

        ttk.Label(self.heater_pid_frame, text="Ki: ", style="statistics.TLabel").grid(column=0, row=2, padx=(20, 10), pady=(0, 10), sticky=tk.NW)
        my_Entry(self.heater_pid_frame, width=8, name=constants.HEATER_PID_KI, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.HEATER_PID_KI, obj_name="Ki", entry_dict=constants.entries_validation_dict)).grid(column=1, row=2, padx=(0, 10), pady=(0, 0), sticky=tk.NW)

        ttk.Label(self.heater_pid_frame, text="Kd: ", style="statistics.TLabel").grid(column=0, row=3, padx=(20, 10), pady=(0, 10), sticky=tk.NW)
        my_Entry(self.heater_pid_frame, width=8, name=constants.HEATER_PID_KD, font= ("Consolas", 10, "bold"),
                 lc_command=lambda x: my_showinfo(title=constants.HEATER_PID_KD, obj_name="Kd", entry_dict=constants.entries_validation_dict)).grid(column=1, row=3, padx=(0, 10), pady=(0, 0), sticky=tk.NW)

        ttk.Label(self, text="To get help on the acceptable values, click with the right mouse button on the desired entry.",
                  foreground="#808080", cursor='question_arrow').grid(column=0, row=7, columnspan=2, padx=(20, 0), pady=(10, 10), sticky=tk.NW)


class OutputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Outputs"
        self.long_name = "OutputsFrame"
        self.parent = parent
        self.configure(background=constants.window_background_color)

        self.create_ui()

    def create_ui(self):
        ttk.Label(self, text="Current temperature: ").grid(column=0, row=0, padx=(20, 0), pady=(20, 10), sticky=tk.NSEW)
        curr_temp_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        curr_temp_frame.grid(column=1, row=0, padx=20, pady=(20, 10), sticky=tk.NSEW)
        self.current_temperature_out = ttk.Label(curr_temp_frame, text="---")
        self.current_temperature_out.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(curr_temp_frame, text="°C").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Water level: ").grid(column=0, row=1, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)
        water_lvl_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_lvl_frame.grid(column=1, row=1, padx=20, pady=(0, 10), sticky=tk.NSEW)
        self.current_water_level_out = ttk.Label(water_lvl_frame, text="---")
        self.current_water_level_out.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_lvl_frame, text="L").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Heater power: ").grid(column=0, row=2, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)
        heater_power_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        heater_power_frame.grid(column=1, row=2, padx=20, pady=(0, 10), sticky=tk.NSEW)
        self.current_heater_power_out = ttk.Label(heater_power_frame, text="---")
        self.current_heater_power_out.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(heater_power_frame, text="kJ").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Water intake: ").grid(column=0, row=3, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)
        water_intake_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_intake_frame.grid(column=1, row=3, padx=20, pady=(0, 10), sticky=tk.NSEW)
        self.current_water_intake_out = ttk.Label(water_intake_frame, text="---")
        self.current_water_intake_out.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_intake_frame, text="mL/s").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Water outake: ").grid(column=0, row=4, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)
        water_outtake_frame = ttk.Frame(self, style="LittleFrame.TFrame")
        water_outtake_frame.grid(column=1, row=4, padx=20, pady=(0, 10), sticky=tk.NSEW)
        self.current_water_outtake_out = ttk.Label(water_outtake_frame, text="---")
        self.current_water_outtake_out.grid(column=0, row=0, sticky=tk.NSEW)
        ttk.Label(water_outtake_frame, text="mL/s").grid(column=1, row=0, sticky=tk.NSEW)

        ttk.Label(self, text="Displayed values may differ from actual in process values, due to sampling time.",
                  foreground="#808080", cursor='question_arrow').grid(column=0, row=5, columnspan=10, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)

        self.statistics_frame = ttk.Frame(self, style="statistics.TFrame")
        self.statistics_frame.grid(column=0, row=6, columnspan=4, padx=(20, 0), pady=(0, 10), sticky=tk.NSEW)
        ttk.Label(self.statistics_frame, text="Simulation statistics:", style="statistics.TLabel").grid(column=0, row=0, padx=(20, 10), pady=(10, 10), sticky=tk.NSEW)

        ttk.Label(self.statistics_frame, text="Boiler filling time: ", style="statistics.TLabel").grid(column=0, row=1, padx=(20, 10), pady=(10, 10), sticky=tk.NSEW)
        self.boiler_fill_time = ttk.Label(self.statistics_frame, text="---", style="statistics.TLabel")
        self.boiler_fill_time.grid(column=1, row=1, sticky=tk.NSEW)
        ttk.Label(self.statistics_frame, text="s", style="statistics.TLabel").grid(column=2, row=1, sticky=tk.NSEW)

        ttk.Label(self.statistics_frame, text="Boiler draining time: ", style="statistics.TLabel").grid(column=0, row=2, padx=(20, 10), pady=(10, 10), sticky=tk.NSEW)
        self.boiler_drain_time = ttk.Label(self.statistics_frame, text="---", style="statistics.TLabel")
        self.boiler_drain_time.grid(column=1, row=2, sticky=tk.NSEW)
        ttk.Label(self.statistics_frame, text="s", style="statistics.TLabel").grid(column=2, row=2, sticky=tk.NSEW)

        ttk.Label(self.statistics_frame, text="Boiler heating time: ", style="statistics.TLabel").grid(column=0, row=3, padx=(20, 10), pady=(10, 10), sticky=tk.NSEW)
        self.boiler_heat_time = ttk.Label(self.statistics_frame, text="---", style="statistics.TLabel")
        self.boiler_heat_time.grid(column=1, row=3, sticky=tk.NSEW)
        ttk.Label(self.statistics_frame, text="s", style="statistics.TLabel").grid(column=2, row=3, sticky=tk.NSEW)

        ttk.Label(self.statistics_frame, text="Average heater power: ", style="statistics.TLabel").grid(column=0, row=4, padx=(20, 10), pady=(10, 10), sticky=tk.NSEW)
        self.heater_avg_pwr = ttk.Label(self.statistics_frame, text="---", style="statistics.TLabel")
        self.heater_avg_pwr.grid(column=1, row=3, sticky=tk.NSEW)
        ttk.Label(self.statistics_frame, text="kJ", style="statistics.TLabel").grid(column=2, row=4, sticky=tk.NSEW)


class GraphsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Graphs"
        self.long_name = "GraphsFrame"
        self.parent = parent
        self.configure(background=constants.window_background_color)

        self.create_ui()

    def create_ui(self):
        dir_var = tk.Variable(value=list(constants.plot_names.values()))
        self.graphs_list = tk.Listbox(self, listvariable=dir_var, height=6, width=30, selectmode=tk.SINGLE,
                                      background=constants.window_background_color, font=("Consolas", 10, "bold"),
                                      selectbackground="#999999")
        self.graphs_list.grid(column=0, row=0, padx=60, pady=60, sticky=tk.NS)
        self.graphs_list.select_set(0)

        self.fig = Figure(figsize=(7, 5), dpi=100, frameon=True)
        self.ax = self.fig.subplots()
        self.line, = self.ax.plot([], [])
        self.ax.set_ylim((0, 1))

        self.canvas = FigureCanvasTkAgg(self.fig, master=self)
        self.canvas.draw()

        self.canvas.get_tk_widget().configure(borderwidth=1, relief='solid')
        self.canvas.get_tk_widget().grid(column=2, row=0, padx=100, pady=20, columnspan=2, rowspan=4, sticky=tk.E)




sim_frames = list(globals()[c] for c, x in globals().copy().items() if re.match('.*Frame$', c))
# create list of class types defined in this scope


def logic_thread(root):
    simulation_counter = 0
    tick_counter = 0
    simulation_old_state, simulation_new_state = constants.SimulatorStates.STOPPED, constants.SimulatorStates.STOPPED
    graph_select_old, graph_select_new = root.notebook_frames[3].graphs_list.curselection()[0], root.notebook_frames[3].graphs_list.curselection()[0]
    ms, sec, min = 0, 0, 0
    data_all = {}
    simulation_sleep = 0.01
    boiler_Ftime = 0
    boiler_Dtime = 0
    boiler_Htime = 0

    process_state = constants.ProcessStates.IDLE

    simulation_sampling_rate = constants.simulation_default_sampling
    
    operators = functions.Functions()
    scale_sample = []

    root.notebook_frames[1].heater_power_scale.set(100)
    root.notebook_frames[1].water_in_scale.set(50)
    root.notebook_frames[1].water_out_scale.set(50)

    heater_PID = functions.PID(1.5, 1, 0.05)

    while 1:
        simulation_old_state = simulation_new_state
        simulation_new_state = root.notebook_frames[0].simulation_state

        # temporally, remove upon release
        if simulation_new_state == constants.SimulatorStates.DATA:
            data_all = {
                'samples_entry': [5, True, ""], 
                'water_initial_temperature_entry': [20, True, ""], 
                'water_target_temperature_entry': [100, True, ""], 
                'boiler_height_entry': [100, True, ""], 
                'boiler_width_entry': [100, True, ""], 
                'boiler_depth_entry': [100, True, ""], 
                'heater_efficiency_entry': [99, True, ], 
                'heater_power_entry': [10000, True, ""], 
                'desired_water_amount_entry': [10, True, ""], 
                'intake_valve_flow_entry': [1000, True, ""], 
                'outtake_valve_flow_entry': [1000, True, ""], 
                'heater_pid_kp': [1.5, True, ""], 
                'heater_pid_ki': [1, True, ""], 
                'heater_pid_kd': [0.05, True, ""]
                }
            root.notebook_frames[0].simulation_state = constants.SimulatorStates.READY            

        # validate entered values upon simulator start
        if ( simulation_new_state in (constants.SimulatorStates.RUNNING, constants.SimulatorStates.REWIND) ):
            if simulation_old_state == constants.SimulatorStates.PAUSED:
                root.notebook_frames[0].process_states_board_frame.nametowidget("ps_run").configure(foreground='red')
            elif simulation_old_state == constants.SimulatorStates.STOPPED:
                all_valid = True
                data_all = {}
                for frame in root.notebook_frames:
                    entry_widgets = rsearch_forentry(frame)
                    if entry_widgets is not None:
                        invalid, data = inputs_validator(frame, entry_widgets)
                        data_all.update(data)
                        if invalid:
                            all_valid = False
                            
                try:
                    if not all_valid:
                        raise Exception()
                    
                    desired_water = int(data_all[constants.WATER_AMOUNT][0])
                    boiler_width = int(data_all[constants.BOILER_WIDTH][0])
                    boiler_height = int(data_all[constants.BOILER_HEIGHT][0])
                    boiler_depth = int(data_all[constants.BOILER_DEPTH][0])
                    if desired_water > ( boiler_width * boiler_height * boiler_depth ) / 1000:
                        data_all[constants.WATER_AMOUNT][1] = False
                        raise Exception()
                    
                    water_Qin = int(data_all[constants.INTAKE_FLOW][0]) * (root.notebook_frames[1].water_in_scale.get() / 100)
                    water_Qout = int(data_all[constants.OUTTAKE_FLOW][0]) * (root.notebook_frames[1].water_out_scale.get() / 100)
                    
                    operators.pouringinitialize(desired_water, water_Qin, water_Qout)
                    operators.heatinginitialize(int(data_all[constants.WATER_ITEMP][0]), int(data_all[constants.WATER_TTEMP][0]), 5000)
                    operators.update_boiler(boiler_width, boiler_depth, boiler_height, heat_loss=0.05)
                    operators.update_heater(power=1000, heater_efficiency=0.95, environment_temperature=25, heater_setpoint=root.notebook_frames[1].heater_power_scale.get())

                    scale_sample = []

                    simulation_sampling_rate = int(data_all[constants.SAMPLES_ENTRY][0])

                    if simulation_new_state == constants.SimulatorStates.RUNNING:   # REALTIME run mode
                        operators.update_dtime(simulation_sampling_rate)
                        simulation_sleep = constants.simulation_tick / 1000
                    else:   # REWIND run mode
                        operators.update_dtime(constants.simulation_rewind_delay * 100000)
                        simulation_sleep = constants.simulation_rewind_delay / 1000000
                        root.config(cursor="watch")

                    operators.resetoperator()
                    ms, sec, min = 0, 0, 0
                    root.notebook_frames[2].boiler_fill_time.configure(text="---")
                    root.notebook_frames[2].boiler_drain_time.configure(text="---")
                    root.notebook_frames[2].boiler_heat_time.configure(text="---")

                    root.config(cursor="watch")

                except Exception as e:
                    root.notebook_frames[0].restart()
                    root.notebook_frames[0].simulation_state = constants.SimulatorStates.STOPPED
                    simulation_new_state = constants.SimulatorStates.STOPPED

                finally:
                    select_invalid(root, data_all)
            # remove upon release
            elif simulation_old_state == constants.SimulatorStates.READY:
                ms, sec, min = 0, 0, 0
                
                operators.resetoperator()
                root.notebook_frames[2].boiler_fill_time.configure(text="---")
                root.notebook_frames[2].boiler_drain_time.configure(text="---")
                root.notebook_frames[2].boiler_heat_time.configure(text="---")
                water_Qin = int(data_all[constants.INTAKE_FLOW][0]) * (root.notebook_frames[1].water_in_scale.get() / 100)
                water_Qout = int(data_all[constants.OUTTAKE_FLOW][0]) * (root.notebook_frames[1].water_out_scale.get() / 100)
                heater_power = int(data_all[constants.HEATER_POWER][0])
                    
                desired_water = int(data_all[constants.WATER_AMOUNT][0])
                operators.pouringinitialize(desired_water, water_Qin, water_Qout)
                operators.heatinginitialize(int(data_all[constants.WATER_ITEMP][0]), int(data_all[constants.WATER_TTEMP][0]), heater_power)
                operators.update_boiler(int(data_all[constants.BOILER_WIDTH][0]), int(data_all[constants.BOILER_DEPTH][0]), int(data_all[constants.BOILER_HEIGHT][0]), heat_loss=0.01)
                operators.update_heater(power=1000, heater_efficiency=0.95, environment_temperature=25, heater_setpoint=root.notebook_frames[1].heater_power_scale.get())
                scale_sample = []
                simulation_sampling_rate = int(data_all[constants.SAMPLES_ENTRY][0])
                heater_PID.set_limits(min_ = 0, max_ = heater_power)
                

                if simulation_new_state == constants.SimulatorStates.RUNNING:   # REALTIME run mode
                    operators.update_dtime(simulation_sampling_rate)
                    simulation_sleep = constants.simulation_tick / 1000
                else:   # REWIND run mode
                    # operators.update_dtime(constants.simulation_rewind_delay * 100000)
                    operators.update_dtime(simulation_sampling_rate*constants.simulation_rewind_delay*10)
                    simulation_sleep = constants.simulation_rewind_delay / 1000000
                    root.config(cursor="watch")

        # make sample every simulation loop iteration, calculate relation sample time to simulation tick
        if ( ( simulation_counter >= 1000/simulation_sampling_rate ) and simulation_new_state == constants.SimulatorStates.RUNNING):
            simulation_counter = 0
            operators.append_sample()

            operators.Q_in = int(data_all[constants.INTAKE_FLOW][0]) * (root.notebook_frames[1].water_in_scale.get() / 100)
            operators.Q_out = int(data_all[constants.OUTTAKE_FLOW][0]) * (root.notebook_frames[1].water_out_scale.get() / 100)

            scale_sample.append(root.notebook_frames[1].heater_power_scale.get())   
            root.notebook_frames[2].current_temperature_out.configure(text=round(operators.water_temp, 2))
            root.notebook_frames[2].current_water_level_out.configure(text=int(operators.V))
            root.notebook_frames[2].current_water_intake_out.configure(text=operators.Q_in)
            root.notebook_frames[2].current_water_outtake_out.configure(text=operators.Q_out) 

        if ( tick_counter > 65000):
            tick_counter = 0
        
        # check if a other graph was selected, if so change displayed graph
        try:
            graph_select_new = root.notebook_frames[3].graphs_list.curselection()[0]
        except:
            pass
        if ( ( graph_select_new != graph_select_old ) or not ( tick_counter * constants.simulation_tick ) % constants.graph_update_time ):
            if root.notebook_frames[3].graphs_list.get(graph_select_new) == constants.plot_names['water_temp']:
                display_water_temperature_graph(root.notebook_frames[3], operators.samples, operators.water_temperatures)
            elif root.notebook_frames[3].graphs_list.get(graph_select_new) == constants.plot_names['heat_pwr']:
                display_heater_power_graph(root.notebook_frames[3], operators.samples, scale_sample)
            elif root.notebook_frames[3].graphs_list.get(graph_select_new) == constants.plot_names['water_lvl']:
                display_water_level_graph(root.notebook_frames[3], operators.samples, operators.water_levels)
        graph_select_old = graph_select_new

        if simulation_new_state == constants.SimulatorStates.RESTART:
            root.notebook_frames[0].simulation_state = constants.SimulatorStates.STOPPED
            simulation_new_state = constants.SimulatorStates.STOPPED
            process_state = constants.ProcessStates.IDLE

            ms, sec, min = 0, 0, 0
            scale_sample = []
            root.notebook_frames[0].timer_label.configure(text=f"Time: --- min -- s --- ms")
            root.notebook_frames[2].current_temperature_out.configure(text="---")
            root.notebook_frames[2].current_water_level_out.configure(text="---")
            root.notebook_frames[2].current_water_intake_out.configure(text="---")
            root.notebook_frames[2].current_water_outtake_out.configure(text="---")
            root.notebook_frames[0].process_states_board_frame.nametowidget("ps_run").configure(foreground='black')
            root.notebook_frames[0].process_states_board_frame.nametowidget("ps_fill").configure(foreground='black')
            root.notebook_frames[0].process_states_board_frame.nametowidget("ps_drain").configure(foreground='black')
            root.notebook_frames[0].process_states_board_frame.nametowidget("ps_heat").configure(foreground='black')
            root.config(cursor="")
            root.notebook_frames[0].update_schematic()

            simulation_sleep = constants.simulation_tick / 1000


        if simulation_new_state == constants.SimulatorStates.RUNNING:
            ms, sec, min = count_time(ms, sec, min, ms_incr=constants.simulation_tick)
            simulation_counter += constants.simulation_tick

        if ( simulation_new_state == constants.SimulatorStates.PAUSED and simulation_old_state in (constants.SimulatorStates.RUNNING, constants.SimulatorStates.REWIND) ):
            root.notebook_frames[0].process_states_board_frame.nametowidget("ps_run").configure(foreground='black')

        if simulation_new_state in (constants.SimulatorStates.RUNNING, constants.SimulatorStates.REWIND):
            water_state = operators.return_in_range(operators.V, operators.boiler_volume)
            fill_state = operators.return_in_range(root.notebook_frames[1].water_in_scale.get()/100, 1)
            drain_state = operators.return_in_range(root.notebook_frames[1].water_out_scale.get()/100, 1)

            operators.append_sample()

            if process_state == constants.ProcessStates.IDLE:
                # change process state to FILLING
                process_state = constants.ProcessStates.FILLING
                root.notebook_frames[0].process_states_board_frame.nametowidget("ps_run").configure(foreground='red')
                root.notebook_frames[0].process_states_board_frame.nametowidget("ps_fill").configure(foreground='red')
                boiler_Ftime = operators.Time
            elif process_state == constants.ProcessStates.FILLING:
                if operators.water_reached_target():
                    process_state = constants.ProcessStates.HEATING
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_heat").configure(foreground='red')
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_fill").configure(foreground='black')
                    boiler_Ftime = -(boiler_Ftime - operators.Time)
                    boiler_Htime = operators.Time
                else:
                    # pour water into boiler until target water amount is not reached
                    operators.pouringwater()
                    # update_schematic(self, heater_state: int = 0, fill_state: int = 0, drain_state: int = 0, water_state: int = 0):
                    if simulation_new_state == constants.SimulatorStates.RUNNING:       # no need to redraw schematic during fast forward simualtion mode
                        root.notebook_frames[0].update_schematic(water_state=water_state, fill_state=fill_state)
            elif process_state == constants.ProcessStates.HEATING:
                if operators.temp_reached_target():
                    process_state = constants.ProcessStates.DRAINING
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_drain").configure(foreground='red')
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_heat").configure(foreground='black')
                    boiler_Htime = -(boiler_Htime - operators.Time)
                    boiler_Dtime = operators.Time
                else:
                    # heat up water until target temperature is not reached
                    operators.heatingupwater()
                    if simulation_new_state == constants.SimulatorStates.RUNNING:       # no need to redraw schematic during fast forward simualtion mode
                        root.notebook_frames[0].update_schematic(water_state=water_state)
            elif process_state == constants.ProcessStates.DRAINING:
                if operators.V == 0:
                    boiler_Dtime = -(boiler_Dtime - operators.Time)
                    root.notebook_frames[2].boiler_fill_time.configure(text=round(boiler_Ftime, 2))
                    root.notebook_frames[2].boiler_drain_time.configure(text=round(boiler_Dtime, 2))
                    root.notebook_frames[2].boiler_heat_time.configure(text=round(boiler_Htime, 2))
                    # go into IDLE state after cycle is finished
                    process_state = constants.ProcessStates.IDLE
                    root.notebook_frames[0].update_schematic()
                    root.notebook_frames[0].restart()
                    root.notebook_frames[0].simulation_state = constants.SimulatorStates.STOPPED
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_run").configure(foreground='black')
                    root.notebook_frames[0].process_states_board_frame.nametowidget("ps_drain").configure(foreground='black')
                    root.notebook_frames[2].current_temperature_out.configure(text="---")
                    root.notebook_frames[2].current_water_level_out.configure(text="---")
                    root.notebook_frames[2].current_water_intake_out.configure(text="---")
                    root.notebook_frames[2].current_water_outtake_out.configure(text="---")
                    root.notebook_frames[1].heater_power_scale.set(100)
                    root.notebook_frames[1].water_in_scale.set(50)
                    root.notebook_frames[1].water_out_scale.set(50)
                    root.config(cursor="")
                    simulation_sleep = constants.simulation_tick / 1000
                else:
                    # drain water from the boiler, until it's empty
                    operators.drainingwater()
                    if simulation_new_state == constants.SimulatorStates.RUNNING:       # no need to redraw schematic during fast forward simualtion mode
                        root.notebook_frames[0].update_schematic(water_state=water_state, drain_state=drain_state)
            
            if simulation_new_state == constants.SimulatorStates.REWIND:
                # rewind simulation mode
                ...
            else:   
                # realtime simulation mode
                root.notebook_frames[0].timer_label.configure(text=f"Time: {min:003n} min {sec:02n} s {ms:003n} ms")
                
        sleep(simulation_sleep)
        tick_counter += 1
        
def display_water_temperature_graph(root, x_vals, y_vals):
    root.ax.clear()
    root.ax.plot(x_vals, y_vals, color="r", label='current temperature')
    root.ax.set_ylim((0, 110))
    root.ax.set_xlabel("t [s]")
    root.ax.set_ylabel("T [°C]")
    root.ax.set_title(label=constants.plot_names['water_temp'])
    root.ax.grid(visible=True, linestyle=':', linewidth=0.5)
    root.ax.legend()
    root.canvas.draw()

def display_heater_power_graph(root, x_vals, y_vals):
    root.ax.clear()
    root.ax.plot(x_vals, y_vals, color="r", label='power setpoint')
    root.ax.set_ylim((0, 100))
    root.ax.set_xlabel("t [s]")
    root.ax.set_ylabel("P [W]")
    root.ax.set_title(label=constants.plot_names['heat_pwr'])
    root.ax.grid(visible=True, linestyle=':', linewidth=0.5)
    root.ax.legend()
    root.canvas.draw()

def display_water_level_graph(root, x_vals, y_vals):
    root.ax.clear()
    root.ax.plot(x_vals, y_vals, color="r", label='current water level')
    root.ax.set_ylim((-1, max(y_vals, default=constants.entries_validation_dict[constants.WATER_AMOUNT]["max"])*1.2))
    root.ax.set_xlabel("t [s]")
    root.ax.set_ylabel("V [L]")
    root.ax.set_title(label=constants.plot_names['water_lvl'])
    root.ax.grid(visible=True, linestyle=':', linewidth=0.5)
    root.ax.legend()
    root.canvas.draw()

def count_time(ms: int, sec: int, min: int, ms_incr: int = 0, sec_inc: int = 0, min_incr: int = 0):
    ms += ms_incr
    d_ms = ms // 1000
    ms -= d_ms * 1000
    sec += sec_inc + d_ms
    d_sec = sec // 60
    sec -= d_sec * 60
    min += min_incr + d_sec
    return ms, sec, min

def unpack_isvalid(input: (str | int | float), entries: dict):
    assert type(entries) is dict
    assert 1 < len(entries) < 7

    args = []
    arg_list = ("format", "min", "max", "float_type", "time_type")

    for key in arg_list:
        args.append(entries[key] if key in entries.keys() else None)
    
    return is_valid(input, args[0], args[1], args[2], args[3], args[4])

def is_valid(input: (str | int | float), format: str, min: (int | float) = None, max: (int | float) = None, float_type: bool = False, time_type: bool = False):
    test1 = re.search(format, input)  # REGEXP search for string by given filter (format)
    try:
        test1.group(0)  # Try to get value from first group, if input is not as format it causes exception
    except:
        return False  # input is not valid
    if min is not None and max is not None:  # Do if min and max values are given
        if float_type:  # Do if float type flag is raised
            if min <= float(input) <= max:  # Check input to be in range of min and max
                return True  # input in range min, max
            else:
                return False  # input beyond range min, max
        else:
            if min <= int(input) <= max:  # Check input to be in range of min and max
                return True  # input in range min, max
            else:
                return False  # input beyond range min, max
    else:  # Do if min and max are not specified
        if time_type:  # Do if time type flag is raised
            time = re.search("([0-9]{1,2}):([0-9]{2}):([0-9]{2})",
                             input)  # Divide time (input) to hours, minutes and seconds
            if 1 <= int(time.group(1)) <= 99:  # Check if hours are in range of 1 to 99
                if 0 <= int(time.group(2)) <= 59:  # Check if minutes are in range of 1 to 59
                    if 0 <= int(time.group(3)) and 59 >= int(
                            time.group(3)):  # Check if seconds are in range of 1 to 59
                        return True
                    else:
                        return False
                else:
                    if 0 <= int(time.group(3)) <= 59:
                        return True
                    else:
                        return False
            else:
                if 1 <= int(time.group(2)) <= 59:
                    if 0 <= int(time.group(3)) <= 59:
                        return True
                    else:
                        return False
                else:
                    if 1 <= int(time.group(3)) <= 59:
                        return True
                    else:
                        return False
        else:
            return True
        
# Returns None if is_valid is True, otherwise return inputs_t
def return_if_bad(is_valid: bool, input_name: str):
    return None if is_valid else input_name

# Marks invalid fields with red background
def select_invalid(root, input):
    for name in input.keys():
        root.nametowidget(input[name][2]).style.configure(str(input[name][2]).split(".")[-1] + ".TEntry", fieldbackground=constants.entry_background_color if input[name][1] is True else '#FF0000')

# search recursively Frame widget and return list of tkinter Entry instances present in given Frame
def rsearch_forentry(widget):
    widgets_list = widget.winfo_children()
    found_entries = []
    for w in widgets_list:
        if w.__class__.__name__ == "Frame":
            # search deeper if Frame found
            temp = rsearch_forentry(w)
            if temp is not None:
                found_entries = [*found_entries, *temp]
        elif w.__class__.__name__ in ("Entry", "my_Entry") :
            # append Entry instance when found
            found_entries.append(w)

    # return list of found Entries, if empty return None
    return found_entries if len(found_entries) else None

def inputs_validator(root, entries):
    data = {}
    invalid_amount = 0

    for entry in entries:
        name = entry._name
        value = root.nametowidget(".".join(str(entry).split(".")[2:])).get()
        data[name] = [value, unpack_isvalid(value, constants.entries_validation_dict[name]), entry]
        if not data[name][1]:
            invalid_amount += 1

    return invalid_amount, data     # return amount of invalid entries, dict of lists: name: (value, is_valid, raw_name), ..., name: (value, is_valid, raw_name)


if __name__ == "__main__":
    main = MainWindow()
    secondary_thread = Thread(target=logic_thread, daemon=True, args=(main,))
    secondary_thread.start()
    main.mainloop()

