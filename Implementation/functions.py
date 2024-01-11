import math


class Functions:
    def __init__(self, sample_time: int, initial_volume: int):
        assert type(sample_time) is int
        assert sample_time > 0
        assert type(initial_volume) is int
        assert initial_volume > 0

        self.volume = initial_volume #volume of boiler [liters]
        self.B = 0.035 #beta
        self.h_min = 0.0
        self.h_max = 5.0
        self.sample_time = sample_time / 1000
        self.t = [0.0]
        self.Q_d = [0.05]
        self.h = [0.0] #amount of water in boiler [liters]
        self.Q_o = [self.B * self.h[-1] ** 0.5]
        self.c = 4200 # specific heat of water
        self.p = 1500
        self.heating_time = [0.0]
        self.temp = [20.00]
        self.temp_Max = 100
        self.temp_Min = 1
        self.m = 0

    def pouringinitialize(self, initial_h, Q_d, Q_o):
        self.h = [initial_h]
        self.m = 0.998 * self.h[-1] #current water mass in boiler [kgs]
        self.Q_d = Q_d
        self.Q_o = Q_o

    def heatinginitialize(self, initial_temperature, heater_power):
        self.temp = [initial_temperature]
        self.p = heater_power
        self.heating_time = [0.0]

    def pouringwater(self):
        self.t.append(self.t[-1] + self.sample_time)
        self.Q_d.append(self.Q_d[-1])
        self.h.append(min(max(self.sample_time * (self.Q_d[-1] - self.Q_o[-1]) / self.volume + self.h[-1], self.h_min), self.h_max))
        self.Q_o.append(self.B * math.sqrt(self.h[-1]))

    def heatingupwater(self, counter):
        self.heating_time.append(self.heating_time[-1] + self.sample_time)
        print(f"self.p: {self.p}, self.m: {self.m}, self.c: {self.c}, self.sample_time: {self.sample_time}")
        self.temp.append(min(max((((((self.p/self.sample_time)/(self.m*self.c))+self.temp[-1]))), self.temp_Min), self.temp_Max))
        print(self.temp[counter], " ")




