import math
import main
volume = 100 #litry
B = 0.035 #beta
h_min = 0.0
h_max = 5.0
t_sim = 3600.0 #simulation time
sample_Time = 0.1
N = int(t_sim/sample_Time) + 1
t = [0.0]
Q_d = [0.05]
h = [0.0]
Q_o = [B * h[-1] ** 0.5]
m = 0.998 * volume #masa wody w naczyniu
c = 4200 # ciepło właściwe wody
q = 10000 / sample_Time
heating_Time = [0.0]
temp = [20.0]
temp_Max = 100
temp_Min = 1

def pouringWater():
    t.append(t[-1] + sample_Time)
    Q_d.append(Q_d[-1])
    h.append(min(max(sample_Time * (Q_d[-1] - Q_o[-1]) /volume + h[-1], h_min), h_max))
    Q_o.append(B * math.sqrt(h[-1]))


def heatingUpWater(counter):
    heating_Time.append(heating_Time[-1] + sample_Time)
    temp.append(min(max(((((q/(m*c))+temp[-1]))), temp_Min), temp_Max))
    print(temp[counter], " ")




