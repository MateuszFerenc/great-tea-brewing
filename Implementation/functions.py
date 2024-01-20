import math
from random import *

class Functions:
    def __init__(self):
        # boiler filling and draining parameters
        self.Q_in = 100                                                     # water intake flow rate [mL/s]
        self.Q_out = 100                                                    # water outtake flow rate [mL/s]

        # water parameters
        self.water_c = 4186                                                 # specific heat of water [J/(kg*K)]
        self.target_temperature = 100                                       # target water temperature [°C]
        self.target_water = 10                                              # target water amount [L]
        self.rho = 1000                                                     # water density [kg/m^3]
        self.V = 10 / 1000                                                  # initial water volume [m^3]
        self.water_temp = 20                                                # actual temperature [°C]
        self.m = self.rho * self.V                                          # initial water mass [kg]
        self.T_env = 25                                                     # environment temperature [°C]
        self.h = 10                                                         # heat transfer coefficient [W/m^2°C]

        # heater parameters
        self.actualpower = 1000                                             # heater power [J]
        self.heater_efficency = 0.85                                        # percentage of heater efficiency [%]   (0-1 => 0-100)
        self.heat_loss = 0.05                                               # percentage of heat loss [%]   (0-1 => 0-100)
        self.heater_c = 385                                                 # specific heat of heater [J/(kg*K)]
        self.heater_setpoint = 100                                          # heater temperature setpoint [°C]
        self.heater_temperature = 0                                         # heater actual temperature [°C]
        
        # boiler parameters
        self.boiler_d = 0.1                                                 # boiler depth [m]
        self.boiler_w = 0.1                                                 # boiler width [m]
        self.boiler_h = 0.1                                                 # boiler height [m]
        self.A = 2 * (self.boiler_d * self.boiler_w + self.boiler_d * self.boiler_h + self.boiler_w * self.boiler_h)  # boiler maximum volume
        self.boiler_volume = ( self.boiler_w * self.boiler_h * self.boiler_d ) / 1000               # boiler volume [L]

        # sampling variables
        self.samples = []
        self.water_temperatures = []
        self.water_levels = []
        self.heater_temperatures = []
        self.heater_powers = []
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
        self.water_temperatures.append(self.water_temp)

    def resetoperator(self):
        self.samples = []
        self.water_temperatures = []
        self.water_levels = []
        self.Time = 0

    def pouringinitialize(self, target_water: float, Q_in, Q_out):
        self.target_water = target_water
        self.Q_in = Q_in
        self.Q_out = Q_out

    def heatinginitialize(self, initial_temperature: float, target_temperature: float, heater_power: int):
        self.water_temp = initial_temperature
        self.target_temperature = target_temperature
        self.actualpower = heater_power

    def pouringwater(self):
        self.V = self.V + (self.Q_in/1000) * self.dTime
        self.m = self.rho * self.V

    def drainingwater(self):
        self.V = self.V - (self.Q_out/1000) * self.dTime
        self.m = self.rho * self.V

    def heatingupwater(self):
        Q_heat = self.actualpower * self.heater_efficency * self.Time
        Q_loss = self.actualpower * ( self.heat_loss * (self.water_temp - self.T_env) ) * self.Time
        dt_heat = Q_heat / ( (self.m/1000) * self.water_c )
        dt_loss = Q_loss / ( (self.m/1000) * self.water_c )
        #print(f'Q_heat: {Q_heat}, Q_loss: {Q_loss}, dt_heat: {dt_heat}, dt_loss: {dt_loss}')
        self.water_temp = round(self.water_temp + dt_heat - dt_loss, 2)

    def temp_reached_target(self):
        return self.water_temp >= self.target_temperature
    
    def water_reached_target(self):
        return self.V >= self.target_water

    # def gettingpower(self, estimatedpower):
    #     if self.actualpower < estimatedpower: self.actualpower += randint(50,150)
    #     else : self.actualpower -= randint(50,150)

    @staticmethod
    def return_in_range(value, max):
        return int(math.ceil(( value / max ) * 20))
