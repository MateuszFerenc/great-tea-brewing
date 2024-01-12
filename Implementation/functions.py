import math
from random import *

class Functions:
    def __init__(self, sample_time: float, initial_volume: float, boiler_height: float = 0.1, bolier_width: float = 0.1, boiler_depth: float = 0.2):
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
        self.c = 4200 # specific heat of water
        self.actualpower = 5000
        self.heating_time = 0.0
        self.T_1 = 20
        self.temp_Max = 100
        self.temp_Min = 1
        self.rho = 1000                                                     # water density [kg/m^3]
        self.V = initial_volume / 1000                                      # inital water volume [m^3]                                                       # initial water temperature (°C)
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
        self.actualpower = heater_power
        self.heating_time = 0.0
        self.T_2 = self.T_1
        self.m = self.rho * self.V

    def pouringwater(self): #w sumie jak patrzyłem to wzór jest mniej więcej w porządku, h to dla nas V po prostu :)
        self.t.append(self.t[-1] + self.sample_time)
        self.Q_d.append(self.Q_d[-1])
        self.h.append(min(max(self.sample_time * (self.Q_d[-1] - self.Q_o[-1]) / self.volume + self.h[-1], self.h_min), self.h_max))
        self.Q_o.append(self.B * math.sqrt(self.h[-1]))

    def heatingupwater(self):
        self.Q = self.actualpower * self.heating_time
        self.Q_loss = self.h * self.A * (self.T_2 - self.T_env) * self.heating_time
        self.samples.append(self.heating_time)
        self.heating_time = round(self.heating_time + self.sample_time, 4)
        self.Q_net = self.Q - self.Q_loss
        delta_T = self.Q_net / (self.c * self.m)
        self.T_2 = self.T_1 + round(delta_T, 2)
        self.temperatures.append(min(max(self.T_2, self.temp_Min), self.temp_Max))
        #jest jakiś problem z tymi wzorami, bo ta grzałka jak damy na 10000 to wywala dość mocno, 
        #a potem ta tempertura nie pozostaje na swoim miejscu :/

    def gettingpower(self, estimatedpower):
        if self.actualpower < estimatedpower: self.actualpower += randint(50,150)
        else : self.actualpower -= randint(50,150)

