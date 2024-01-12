import math


class Functions:
    def __init__(self, sample_time: int, initial_volume: int):
        assert type(sample_time) is int
        assert sample_time > 0
        assert type(initial_volume) is int
        assert initial_volume > 0

        self.B = 0.035 #beta
        self.h_min = 0.0
        self.h_max = 5.0
        self.sample_time = sample_time / 1000
        self.t = [0.0]
        self.Q_d = [0.05]
        #self.Q_o = [self.B * self.h[-1] ** 0.5]
        self.c = 4200 # specific heat of water
        self.p = 1500
        self.heating_time = 0.0
        self.temp_Max = 100
        self.temp_Min = 1
        self.rho = 1000 # gęstość wody (kg/m^3)
        self.V = 0.0015 # objętość wody (m^3)
        self.T_1 = 20 # temperatura początkowa wody (°C)
        self.T_env = 25 # temperatura otoczenia (°C)
        self.h = 10 # współczynnik przenikania ciepła (W/m^2°C)
        self.l = 0.2 # długość czajnika (m)
        self.w = 0.15 # szerokość czajnika (m)
        self.h = 0.1 # wysokość czajnika (m)
        self.A = 2 * (self.l * self.w + self.l * self.h + self.w * self.h) # powierzchnia ścianek czajnika (m^2)
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
        self.T_2 = self.T_1 # temperatura końcowa wody (°C)
        self.m = self.rho * self.V # masa wody (kg)

    def pouringwater(self):
        self.t.append(self.t[-1] + self.sample_time)
        self.Q_d.append(self.Q_d[-1])
        self.h.append(min(max(self.sample_time * (self.Q_d[-1] - self.Q_o[-1]) / self.volume + self.h[-1], self.h_min), self.h_max))
        self.Q_o.append(self.B * math.sqrt(self.h[-1]))

    def heatingupwater(self):
        #self.heating_time.append(self.heating_time[-1] + self.sample_time)
        #print(f"self.p: {self.p}, self.m: {self.m}, self.c: {self.c}, self.sample_time: {self.sample_time}")
        #self.temp.append(min(max((((((self.p/self.sample_time)/(self.m*self.c))+self.temp[-1]))), self.temp_Min), self.temp_Max))T_2 = T_1 # temperatura końcowa wody (°C)
        #print(self.temp[counter], " ")

        self.Q = self.p * self.heating_time # ciepło dostarczone przez grzałkę (J)
        self.Q_loss = self.h * self.A * (self.T_2 - self.T_env) * self.heating_time # ciepło utracone przez ścianki czajnika (J)
        self.samples.append(self.heating_time)
        self.heating_time += self.sample_time
        self.Q_net = self.Q - self.Q_loss # ciepło netto dostarczone do wody (J)
        delta_T = self.Q_net / (self.c * self.m) # zmiana temperatury wody (°C)
        self.T_2 = self.T_1 + delta_T # temperatura końcowa wody (°C)
        self.temperatures.append(self.T_2)
        print(f"Po {self.heating_time} sekundach temperatura wody wynosi {self.T_2:.2f} °C") # wyświetlenie wyniku




