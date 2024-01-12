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
q = 100 / sample_Time
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