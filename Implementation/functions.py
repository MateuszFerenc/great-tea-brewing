import math


class Functions:
    def __init__(self, sample_time: int, initial_volume: float, boiler_height: float = 0.1, bolier_width: float = 0.1, boiler_depth: float = 0.2):
        assert type(sample_time) is int
        assert sample_time > 0
        assert initial_volume > 0

        # fix pouring
        self.B = 0.035 #beta
        self.h_min = 0.0
        self.h_max = 5.0
        self.sample_time = round(sample_time / 1000, 4)
        self.t = [0.0]
        self.Q_d = [0.05]
        #self.Q_o = [self.B * self.h[-1] ** 0.5]
        #

        self.c = 4200                                                       # specific heat of water [J/kg°C]
        self.p = 1500                                                       # heating Wattage [W]
        self.heating_time = 0.0
        self.temp_Max = 105
        self.temp_Min = 1
        self.rho = 1000                                                     # water density [kg/m^3]
        self.V = initial_volume / 1000                                      # inital water volume [m^3]
        self.T_1 = 20                                                       # initial water temperature (°C)
        self.T_env = 25                                                     # environment temperature [°C]
        self.h = 10                                                         # heat transfer coefficient [W/m^2°C]
        self.l = boiler_depth                                               # boiler depth [m]
        self.w = bolier_width                                               # boiler width [m]
        self.h = boiler_height                                              # boiler height [m]
        self.A = 2 * (self.l * self.w + self.l * self.h + self.w * self.h)  # boiler maximum volume
        self.samples = []
        self.temperatures = []


    def pouringinitialize(self, initial_volume, Q_d, Q_o):
        self.V = initial_volume / 1000
        self.Q_d = Q_d
        self.Q_o = Q_o

    def heatinginitialize(self, initial_temperature, heater_power):
        self.T_1 = initial_temperature
        self.p = heater_power
        self.heating_time = 0.0
        self.T_2 = self.T_1
        self.m = self.rho * self.V

    def pouringwater(self):
        self.t.append(self.t[-1] + self.sample_time)
        self.Q_d.append(self.Q_d[-1])
        self.h.append(min(max(self.sample_time * (self.Q_d[-1] - self.Q_o[-1]) / self.volume + self.h[-1], self.h_min), self.h_max))
        self.Q_o.append(self.B * math.sqrt(self.h[-1]))

    def heatingupwater(self, sample_time):
        self.Q = self.p * self.heating_time
        self.Q_loss = self.h * self.A * (self.T_2 - self.T_env) * self.heating_time
        self.samples.append(self.heating_time)
        self.heating_time = round(self.heating_time + round(sample_time / 1000, 4), 4)
        self.Q_net = self.Q - self.Q_loss
        delta_T = self.Q_net / (self.c * self.m)
        self.T_2 = self.T_1 + delta_T
        self.temperatures.append(self.T_2)
        #print(f"Po {self.heating_time} sekundach temperatura wody wynosi {self.T_2:.2f} °C") # wyświetlenie wyniku


def heater_temperature():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), ..., (95, 100)]

        for interval in intervals:
            if interval[0] <= number <= interval[1]:
                display_image_heater_temperature(interval)
                return
        if number == 0:
            display_image_heater_temperature((0, 0))
            return
        elif number == 100:
            display_image_heater_temperature((100, 100))
            return
    except ValueError: #if user is an idiot
        pass

def display_image_heater_temperature(interval):
    placeholder_image_paths = {
            (0, 5): "ht0.png",
            (5, 10): "ht1.png",
            (10, 15): "ht2.png",
            (15, 20): "ht3.png",
            (20, 25): "ht4.png",
            (25, 30): "ht5.png",
            (30, 35): "ht6.png",
            (35, 40): "ht7.png",
            (40, 45): "ht8.png",
            (45, 50): "ht9.png",
            (50, 55): "ht10.png",
            (55, 60): "ht11.png",
            (60, 65): "ht12.png",
            (65, 70): "ht13.png",
            (70, 75): "ht14.png",
            (75, 80): "ht15.png",
            (80, 85): "ht16.png",
            (85, 90): "ht17.png",
            (90, 95): "ht18.png",
            (95, 100): "ht19.png",
            (0, 0): "ht20",
            (100, 100): "ht21.png",
    }


def puring_in():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), ..., (95, 100)]

        for interval in intervals:
            if interval[0] <= number <= interval[1]:
                display_image_puring_in(interval)
                return
        if number == 0:
            display_image_puring_in((0, 0))
            return
        elif number == 100:
            display_image_puring_in((100, 100))
            return
    except ValueError: #if user is an idiot
        pass

def display_image_puring_in(interval):
    placeholder_image_paths = {
            (0, 5): "pi0.png",
            (5, 10): "pi1.png",
            (10, 15): "pi2.png",
            (15, 20): "pi3.png",
            (20, 25): "pi4.png",
            (25, 30): "pi5.png",
            (30, 35): "pi6.png",
            (35, 40): "pi7.png",
            (40, 45): "pi8.png",
            (45, 50): "pi9.png",
            (50, 55): "pi10.png",
            (55, 60): "pi11.png",
            (60, 65): "pi12.png",
            (65, 70): "pi13.png",
            (70, 75): "pi14.png",
            (75, 80): "pi15.png",
            (80, 85): "pi16.png",
            (85, 90): "pi17.png",
            (90, 95): "pi18.png",
            (95, 100): "pi19.png",
            (0, 0): "pi20",
            (100, 100): "pi21.png",
    }


def puring_out():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), ..., (95, 100)]

        for interval in intervals:
            if interval[0] <= number <= interval[1]:
                display_image_puring_out(interval)
                return
        if number == 0:
            display_image_puring_out((0, 0))
            return
        elif number == 100:
            display_image_puring_out((100, 100))
            return
    except ValueError: #if user is an idiot
        pass

def display_image_puring_out(interval):
    placeholder_image_paths = {
            (0, 5): "po0.png",
            (5, 10): "po1.png",
            (10, 15): "po2.png",
            (15, 20): "po3.png",
            (20, 25): "po4.png",
            (25, 30): "po5.png",
            (30, 35): "po6.png",
            (35, 40): "po7.png",
            (40, 45): "po8.png",
            (45, 50): "po9.png",
            (50, 55): "po10.png",
            (55, 60): "po11.png",
            (60, 65): "po12.png",
            (65, 70): "po13.png",
            (70, 75): "po14.png",
            (75, 80): "po15.png",
            (80, 85): "po16.png",
            (85, 90): "po17.png",
            (90, 95): "po18.png",
            (95, 100): "po19.png",
            (0, 0): "po20",
            (100, 100): "po21.png",
    }


def water_level():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), ..., (95, 100)]

        for interval in intervals:
            if interval[0] <= number <= interval[1]:
                display_image_water_level(interval)
                return
        if number == 0:
            display_image_water_level((0, 0))
            return
        elif number == 100:
            display_image_water_level((100, 100))
            return
    except ValueError: #if user is an idiot
        pass

def display_image_water_level(interval):
    placeholder_image_paths = {
            (0, 5): "wl0.png",
            (5, 10): "wl1.png",
            (10, 15): "wl2.png",
            (15, 20): "wl3.png",
            (20, 25): "wl4.png",
            (25, 30): "wl5.png",
            (30, 35): "wl6.png",
            (35, 40): "wl7.png",
            (40, 45): "wl8.png",
            (45, 50): "wl9.png",
            (50, 55): "wl10.png",
            (55, 60): "wl11.png",
            (60, 65): "wl12.png",
            (65, 70): "wl13.png",
            (70, 75): "wl14.png",
            (75, 80): "wl15.png",
            (80, 85): "wl16.png",
            (85, 90): "wl17.png",
            (90, 95): "wl18.png",
            (95, 100): "wl19.png",
            (0, 0): "wl20",
            (100, 100): "wl21.png",
    }