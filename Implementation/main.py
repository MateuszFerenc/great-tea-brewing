import tkinter as tk
import tkinter.ttk as ttk
import constants
import types
import re


def get_center(parent, axis, val):
    assert axis in ['x', 'y']
    ax = {"x": parent.winfo_screenwidth(), "y": parent.winfo_screenheight()}
    return int(ax[axis] / 2 - val / 2)


class MainWindow(tk.Tk):
    def __init__(self):
        super().__init__()
        self.__drawmain__()

    def __drawmain__(self):
        self.style = ttk.Style()
        self.style.theme_use('clam')
                  
        #self.style.theme_settings(self.style.theme_use(),
        #                        settings={
        #"TNotebook": {"configure": {"tabmargins": [2, 5, 2, 0] } },
        #"TNotebook.Tab": {"configure": {"padding": [20, 10] },}})
        
        self.title("Tea Brewing Simulator")
        self.geometry(f"{constants.window_width}x{constants.window_height}+"
                      f"{get_center(self, 'x', constants.window_width)}+{get_center(self, 'y', constants.window_height)}")
        self.resizable(False, False)
        self.configure(bg=constants.window_background_color)

        self.grid()

        self.notebook = ttk.Notebook(self, takefocus=False, width=constants.window_width, height=constants.window_height)
        self.notebook.grid(column=0, row=0)

        self.notebook_frames = []
        for win_frame in sim_frames:
            frame = win_frame(parent=self)
            self.notebook.add(frame, text=frame.name)
            self.notebook_frames.append(frame)
            

class SimulationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Simulation"
        self.long_name = "SimulationFrame"
        self.parent = parent
        self.grid()

        label = ttk.Label(self, text="Tab 0")
        label.grid(column=0, row=0)
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class InputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Inputs"
        self.long_name = "InputsFrame"
        self.parent = parent
        self.grid()

        label = ttk.Label(self, text="Tab 1")
        label.grid(column=0, row=0)
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
        self.button = ttk.Button(self, text="switch theme", command=self.change_theme)
        self.button.grid(column=0, row=1)
        self.label = ttk.Label(self, text=self.parent.style.theme_use())
        self.label.grid(column=1, row=1)

    def change_theme(self):
        selected_style = self.parent.style.theme_names().index(self.parent.style.theme_use())
        self.parent.style.theme_use(self.parent.style.theme_names()[selected_style + 1 if selected_style < len(self.parent.style.theme_names()) - 1 else 0])
        self.label.config(text=self.parent.style.theme_use())

    def content_update(self):
        pass

class OutputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent, padx=10, pady=10)
        self.name = "Outputs"
        self.long_name = "OutputsFrame"
        self.parent = parent
        self.grid()

        label = ttk.Label(self, text="Tab 3")
        label.grid(column=0, row=0)
        # self.create_ui()
        # self.content_update()

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

if __name__ == "__main__":
    main = MainWindow()
    main.mainloop()