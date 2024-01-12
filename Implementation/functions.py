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
        number = float((self.temperatures[-1]/self.temp_Max)/100)  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), 
                     (70, 75), (75, 80), (80, 85), (85, 90), (90, 95), (95, 100)]

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
            (0, 0): "Assets\images\heater_temperature\0.png",
            (0, 5): "Assets\images\heater_temperature\1.png",
            (5, 10): "Assets\images\heater_temperature\2.png",
            (10, 15): "Assets\images\heater_temperature\3.png",
            (15, 20): "Assets\images\heater_temperature\4.png",
            (20, 25): "Assets\images\heater_temperature\5.png",
            (25, 30): "Assets\images\heater_temperature\6.png",
            (30, 35): "Assets\images\heater_temperature\7.png",
            (35, 40): "Assets\images\heater_temperature\8.png",
            (40, 45): "Assets\images\heater_temperature\9.png",
            (45, 50): "Assets\images\heater_temperature\10.png",
            (50, 55): "Assets\images\heater_temperature\11.png",
            (55, 60): "Assets\images\heater_temperature\12.png",
            (60, 65): "Assets\images\heater_temperature\13.png",
            (65, 70): "Assets\images\heater_temperature\14.png",
            (70, 75): "Assets\images\heater_temperature\15.png",
            (75, 80): "Assets\images\heater_temperature\16.png",
            (80, 85): "Assets\images\heater_temperature\17.png",
            (85, 90): "Assets\images\heater_temperature\18.png",
            (90, 95): "Assets\images\heater_temperature\19.png",
            (95, 100): "Assets\images\heater_temperature\20.png",
            (100, 100): "Assets\images\heater_temperature\21.png",
    }


def puring_in():
    try:
        number = float()  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), 
                     (70, 75), (75, 80), (80, 85), (85, 90), (90, 95), (95, 100)]

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
            (0, 0): "Assets\images\pouring_in\0.png",
            (0, 5): "Assets\images\pouring_in\1.png",
            (5, 10): "Assets\images\pouring_in\2.png",
            (10, 15): "Assets\images\pouring_in\3.png",
            (15, 20): "Assets\images\pouring_in\4.png",
            (20, 25): "Assets\images\pouring_in\5.png",
            (25, 30): "Assets\images\pouring_in\6.png",
            (30, 35): "Assets\images\pouring_in\7.png",
            (35, 40): "Assets\images\pouring_in\8.png",
            (40, 45): "Assets\images\pouring_in\9.png",
            (45, 50): "Assets\images\pouring_in\10.png",
            (50, 55): "Assets\images\pouring_in\11.png",
            (55, 60): "Assets\images\pouring_in\12.png",
            (60, 65): "Assets\images\pouring_in\13.png",
            (65, 70): "Assets\images\pouring_in\14.png",
            (70, 75): "Assets\images\pouring_in\15.png",
            (75, 80): "Assets\images\pouring_in\16.png",
            (80, 85): "Assets\images\pouring_in\17.png",
            (85, 90): "Assets\images\pouring_in\18.png",
            (90, 95): "Assets\images\pouring_in\19.png",
            (95, 100): "Assets\images\pouring_in\20.png",
            (100, 100): "Assets\images\pouring_in\21.png",
    }


def puring_out():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), 
                     (70, 75), (75, 80), (80, 85), (85, 90), (90, 95), (95, 100)]

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
            (0, 0): "Assets\images\pouring_out\0.png",
            (0, 5): "Assets\images\pouring_out\1.png",
            (5, 10): "Assets\images\pouring_out\2.png",
            (10, 15): "Assets\images\pouring_out\3.png",
            (15, 20): "Assets\images\pouring_out\4.png",
            (20, 25): "Assets\images\pouring_out\5.png",
            (25, 30): "Assets\images\pouring_out\6.png",
            (30, 35): "Assets\images\pouring_out\7.png",
            (35, 40): "Assets\images\pouring_out\8.png",
            (40, 45): "Assets\images\pouring_out\9.png",
            (45, 50): "Assets\images\pouring_out\10.png",
            (50, 55): "Assets\images\pouring_out\11.png",
            (55, 60): "Assets\images\pouring_out\12.png",
            (60, 65): "Assets\images\pouring_out\13.png",
            (65, 70): "Assets\images\pouring_out\14.png",
            (70, 75): "Assets\images\pouring_out\15.png",
            (75, 80): "Assets\images\pouring_out\16.png",
            (80, 85): "Assets\images\pouring_out\17.png",
            (85, 90): "Assets\images\pouring_out\18.png",
            (90, 95): "Assets\images\pouring_out\19.png",
            (95, 100): "Assets\images\pouring_out\20.png",
            (100, 100): "Assets\images\pouring_out\21.png",
    }


def water_level():
    try:
        number = int(entry.get())  #getting the number from entry
        intervals = [(0, 5), (5, 10), (10, 15), (15, 20), (20, 25), (25, 30), (30, 35), (35, 40), (40, 45), (45, 50), (50, 55), (55, 60), (60, 65), (65, 70), 
                     (70, 75), (75, 80), (80, 85), (85, 90), (90, 95), (95, 100)]

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
            (0, 0): "Assets\images\water_level\0.png",
            (0, 5): "Assets\images\water_level\1.png",
            (5, 10): "Assets\images\water_level\2.png",
            (10, 15): "Assets\images\water_level\3.png",
            (15, 20): "Assets\images\water_level\4.png",
            (20, 25): "Assets\images\water_level\5.png",
            (25, 30): "Assets\images\water_level\6.png",
            (30, 35): "Assets\images\water_level\7.png",
            (35, 40): "Assets\images\water_level\8.png",
            (40, 45): "Assets\images\water_level\9.png",
            (45, 50): "Assets\images\water_level\10.png",
            (50, 55): "Assets\images\water_level\11.png",
            (55, 60): "Assets\images\water_level\12.png",
            (60, 65): "Assets\images\water_level\13.png",
            (65, 70): "Assets\images\water_level\14.png",
            (70, 75): "Assets\images\water_level\15.png",
            (75, 80): "Assets\images\water_level\16.png",
            (80, 85): "Assets\images\water_level\17.png",
            (85, 90): "Assets\images\water_level\18.png",
            (90, 95): "Assets\images\water_level\19.png",
            (95, 100): "Assets\images\water_level\20.png",
            (100, 100): "Assets\images\water_level\21.png",
    }