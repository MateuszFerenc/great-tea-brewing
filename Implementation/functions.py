import math
from random import *

class Functions:
    def __init__(self):
        # fix pouring
        self.B = 0.035 #beta
        self.h_min = 0.0
        self.h_max = 5.0
        self.t = [0.0]
        self.Q_d = [0.05]
        #self.Q_o = [self.B * self.h[-1] ** 0.5]

        self.c = 4186                                                       # specific heat of water [J/(kg*K)]
        self.actualpower = 5000
        self.temp = 20                                                      # actual temperature [°C]
        self.target_temperature = 100                                       # target water temperature [°C]
        self.target_water = 10                                              # target water amount [L]
        self.temp_Max = 100
        self.temp_Min = 1
        self.rho = 1000                                                     # water density [kg/m^3]
        self.V = 10 / 1000                                      # initial water volume [m^3]
        self.m = self.rho * self.V                                          # initial water mass [kg]
        self.T_env = 25                                                     # environment temperature [°C]
        self.h = 10                                                         # heat transfer coefficient [W/m^2°C]
        self.boiler_d = 0.1                                        # boiler depth [m]
        self.boiler_w = 0.1                                        # boiler width [m]
        self.boiler_h = 0.1                                       # boiler height [m]
        self.A = 2 * (self.boiler_d * self.boiler_w + self.boiler_d * self.boiler_h + self.boiler_w * self.boiler_h)  # boiler maximum volume
        self.boiler_volume = ( self.boiler_w * self.boiler_h * self.boiler_d ) / 1000               # boiler volume [L]
        self.heater_efficency = 0.85                                        
        self.heat_loss = 0.05
        self.samples = []
        self.temperatures = []
        self.water_levels = []
        self.Time = 0
        self.dTime = 1

    def update_dtime(self, sample_time: int):
        self.dTime = round(1 / sample_time, 6)

    def update_boiler(self, width: int, height: int, depth: int, heat_loss: float = 0.5):
        self.boiler_w = width
        self.boiler_h = height
        self.boiler_d = depth
        self.A = 2 * (self.boiler_d * self.boiler_w + self.boiler_d * self.boiler_h + self.boiler_w * self.boiler_h)
        self.boiler_volume = ( self.boiler_w * self.boiler_h * self.boiler_d ) / 1000 
        self.heat_loss = heat_loss

    def update_heater(self, power: int, heater_efficency: int, environment_temperature: float):
        self.actualpower = power
        self.heater_efficency = heater_efficency
        self.T_env = environment_temperature


    def append_sample(self):
        self.samples.append(self.Time)
        self.Time = round(self.Time + self.dTime, 6)
        self.water_levels.append(self.V)
        self.temperatures.append(self.temp)

    def resetoperator(self):
        self.samples = []
        self.temperatures = []
        self.water_levels = []
        self.Time = 0

    def pouringinitialize(self, initial_volume: int, target_water: float, Q_d, Q_o):
        self.V = initial_volume / 1000
        self.target_water = target_water
        self.Q_d = Q_d
        self.Q_o = Q_o

    def heatinginitialize(self, initial_temperature: float, target_temperature: float, heater_power: int):
        self.temp = initial_temperature
        self.target_temperature = target_temperature
        self.actualpower = heater_power

    def pouringwater(self):
        self.V += 1
        #self.t.append(self.t[-1] + self.sample_time)
        #self.Q_d.append(self.Q_d[-1])
        #self.h.append(min(max(self.sample_time * (self.Q_d[-1] - self.Q_o[-1]) / self.volume + self.h[-1], self.h_min), self.h_max))
        #self.Q_o.append(self.B * math.sqrt(self.h[-1]))

    def drainingwater(self):
        self.V -= 1
        if self.V < 1:
            self.V = 0

    def heatingupwater(self):
        Q_heat = self.actualpower * self.heater_efficency * self.dTime
        Q_loss = self.actualpower * self.heat_loss * self.dTime
        dt_heat = Q_heat / ( self.m * self.c )
        dt_loss = Q_loss / ( self.m * self.c )
        #self.temp = round(self.temp + dt_heat - dt_loss, 2)
        self.temp = self.temp + 1

    def temp_reached_target(self):
        return self.temp >= self.target_temperature
    
    def water_reached_target(self):
        return self.V >= self.target_water

    def gettingpower(self, estimatedpower):
        if self.actualpower < estimatedpower: self.actualpower += randint(50,150)
        else : self.actualpower -= randint(50,150)

    @staticmethod
    def return_in_range(value, max):
        return int(math.ceil(( value / max ) * 20))
