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
        self.water_mass = self.rho * (self.V / 1000)                                # initial water mass [kg]
        self.T_env = 25                                                     # environment temperature [°C]
        self.h = 10                                                         # heat transfer coefficient [W/m^2°C]

        # heater parameters      
        self.heater_efficiency = 0.85                                        # percentage of heater efficiency [%]   (0-1 => 0-100)
        self.heat_loss = 0.05                                               # percentage of heat loss [%]   (0-1 => 0-100)
        self.heater_c = 385                                                 # specific heat of heater [J/(kg*K)]
        self.heater_setpoint = 100                                          # heater temperature setpoint [°C]
        self.heater_temperature = 0                                         # heater actual temperature [°C]
        self.heater_max_power = 0                                           # heater maximum power [J]
        self.heater_power = 0                                               # heater actual power [J]
        
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
        self.heater_setpoints = []
        self.Time = 0
        self.dTime = 1

    def update_dtime(self, samples_ps: int):
        self.dTime = round(1 / samples_ps, 6)

    def update_boiler(self, width: int, height: int, depth: int, heat_loss: float = 0.5):
        self.boiler_w = width
        self.boiler_h = height
        self.boiler_d = depth
        self.A = 2 * (self.boiler_d * self.boiler_w + self.boiler_d * self.boiler_h + self.boiler_w * self.boiler_h)
        self.boiler_volume = ( self.boiler_w * self.boiler_h * self.boiler_d ) / 1000 
        self.heat_loss = heat_loss

    def update_heater(self, power: int, heater_efficiency: int, environment_temperature: float, heater_setpoint):
        self.heater_power = power
        self.heater_efficiency = heater_efficiency
        self.T_env = environment_temperature
        self.heater_setpoint = heater_setpoint

    def append_sample(self):
        self.samples.append(self.Time)
        self.Time = round(self.Time + self.dTime, 6)
        self.water_levels.append(self.V)
        self.water_temperatures.append(self.water_temp)

    def resetoperator(self):
        self.samples = []
        self.water_temperatures = []
        self.water_levels = []
        self.heater_temperatures = []
        self.heater_powers = []
        self.heater_setpoints = []
        self.Time = 0
        self.V = 0
        self.water_temp = 0

    def pouringinitialize(self, target_water: float, Q_in, Q_out):
        self.target_water = target_water
        self.Q_in = Q_in
        self.Q_out = Q_out

    def heatinginitialize(self, initial_temperature: float, target_temperature: float):
        self.water_temp = initial_temperature
        self.target_temperature = target_temperature

    def pouringwater(self, sample_ready: bool = True):
        if sample_ready:
            self.V = self.V + (self.Q_in/1000) * self.dTime
            self.water_mass = self.rho * (self.V / 1000)

    def drainingwater(self, sample_ready: bool = True):
        if sample_ready:
            self.V = self.V - (self.Q_out/1000) * self.dTime
            if self.V < 0.001:
                self.V = 0
            self.water_mass = self.rho * (self.V / 1000)

    def heatingupwater(self, sample_ready: bool = True):
        if sample_ready:
            Q_heat = self.heater_power * self.heater_efficiency
            Q_loss = self.heater_power * self.heat_loss * (self.water_temp - self.T_env)
            dt_heat = Q_heat / ( self.water_mass * self.water_c )
            dt_loss = Q_loss / ( self.water_mass * self.water_c )
            #print(f'Q_heat: {Q_heat}, Q_loss: {Q_loss}, dt_heat: {dt_heat}, dt_loss: {dt_loss}')
            self.water_temp = self.water_temp + dt_heat - dt_loss

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

class PID:
    def __init__(self, Kp: float, Ki: float, Kd: float, output_limits: (float, float) = (None, None)):
        self.Kp, self.Ki, self.Kd = Kp, Ki, Kd
        self._limits = output_limits
        self.error = 0
        self.setpoint = 0
        self.output = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0

    def compute(self, dt, actual):
        self.error = self.setpoint - actual
        self.integral += self._get_limit(self.error * dt, self._limits)
        self.derivative = (self.error - self.last_error) / dt
        self.output = get_limit(self.Kp * self.error + self.Ki * self.integral + self.Kd * self.derivative, self._limits)
        self.last_error = self.error

    def reset(self):
        self.error = 0
        self.setpoint = 0
        self.output = 0
        self.integral = 0
        self.derivative = 0
        self.last_error = 0

    def update_setpoint(self, setpoint):
        self.setpoint = setpoint

    def set_limits(self, min_, max_):
        self._limits = (min_, max_)


def get_limit(value, limits):
    lower, upper = limits
    if value is None:
        return None
    elif (upper is not None) and (value > upper):
        return upper
    elif (lower is not None) and (value < lower):
        return lower
    return value
    