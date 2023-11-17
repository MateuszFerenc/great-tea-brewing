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
        self.title("Tea Brewing Simulator")
        self.geometry(f"{constants.window_width}x{constants.window_height}+"
                      f"{get_center(self, 'x', constants.window_width)}+{get_center(self, 'y', constants.window_height)}")
        self.resizable(False, False)
        self.configure(bg=constants.window_background_color)

        self.notebook = ttk.Notebook(self, takefocus=False, width=constants.window_width, height=constants.window_height)
        self.notebook.place(rely=0, relwidth=1)

        self.notebook_frames = []
        for win_frame in sim_frames:
            frame = win_frame(parent=self)
            frame.pack(expand=False)
            self.notebook.add(frame, text=frame.name)
            self.notebook_frames.append(frame)
            

class SimulationFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Simulation"
        self.long_name = "SimulationFrame"
        self.parent = parent
        label = ttk.Label(self, text="Tab 0")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class InputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Inputs"
        self.long_name = "InputsFrame"
        self.parent = parent
        label = ttk.Label(self, text="Tab 1")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class ControlFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Control"
        self.long_name = "ControlFrame"
        self.parent = parent
        label = ttk.Label(self, text="Tab 2")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class OutputsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Outputs"
        self.long_name = "OutputsFrame"
        self.parent = parent
        label = ttk.Label(self, text="Tab 3")
        label.pack()
        # self.create_ui()
        # self.content_update()

    def create_ui(self):
        pass

    def content_update(self):
        pass

class GraphsFrame(tk.Frame):
    def __init__(self, parent):
        super().__init__(parent)
        self.name = "Graphs"
        self.long_name = "GraphsFrame"
        self.parent = parent
        label = ttk.Label(self, text="Tab 4")
        label.pack()
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