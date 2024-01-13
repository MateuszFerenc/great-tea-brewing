# # Parametry czajnika
# V = 230 # napięcie (V)
# R = 20 # oporność (ohm)
# c = 4190 # ciepło właściwe wody (J/kg°C)
# rho = 1000 # gęstość wody (kg/m^3)
# V_w = 0.0015 # objętość wody (m^3)
# T_1 = 20 # temperatura początkowa wody (°C)
# T_env = 25 # temperatura otoczenia (°C)
# h = 10 # współczynnik przenikania ciepła (W/m^2°C)
# l = 0.2 # długość czajnika (m)
# w = 0.15 # szerokość czajnika (m)
# h = 0.1 # wysokość czajnika (m)

# # Obliczenia
# P = V**2 / R # moc grzałki (W)
# m = rho * V_w # masa wody (kg)
# A = 2 * (l * w + l * h + w * h) # powierzchnia ścianek czajnika (m^2)
# T_2 = T_1 # temperatura końcowa wody (°C)
# t = 0 # czas (s)

# print(f"moc grzalki: {P}")
# # Symulacja
# while T_2 < 100: # pętla do momentu zagotowania wody
#   Q = P * t # ciepło dostarczone przez grzałkę (J)
#   Q_loss = h * A * (T_2 - T_env) * t # ciepło utracone przez ścianki czajnika (J)
#   Q_net = Q - Q_loss # ciepło netto dostarczone do wody (J)
#   delta_T = Q_net / (c * m) # zmiana temperatury wody (°C)
#   T_2 = T_1 + delta_T # temperatura końcowa wody (°C)
#   print(f"Po {t} sekundach temperatura wody wynosi {T_2:.2f} °C") # wyświetlenie wyniku
#   t += 1 # zwiększenie czasu o 1 sekundę

# Symulacja czajnika
# Założenia: 
# - Czajnik ma pojemność 1 litra i jest napełniony zimną wodą o temperaturze 20°C
# - Czajnik jest podłączony do prądu o napięciu 230V i mocy 2000W
# - Czajnik wyłącza się automatycznie, gdy temperatura wody osiągnie 100°C
# - Ciepło jest przekazywane z grzałki do wody z efektywnością 80%
# - Ciepło jest tracone przez ścianki czajnika z efektywnością 10%

# Parametry fizyczne
C = 4186 # ciepło właściwe wody w J/(kg*K)
M = 1 # masa wody w kg
P = 2000 # moc grzałki w W
E = 0.8 # efektywność przekazywania ciepła
L = 0.1 # efektywność utraty ciepła

# Parametry symulacji
dt = 1 # krok czasowy w s
T = 20 # temperatura początkowa wody w °C
t = 0 # czas początkowy w s
k = False # flaga gotowości

# Pętla symulacji
while not k:
  # Oblicz przyrost ciepła od grzałki
  Q_in = P * E * dt
  # Oblicz przyrost temperatury od ciepła
  dT_in = Q_in / (M * C)
  # Oblicz utratę ciepła przez ścianki
  Q_out = P * L * dt
  # Oblicz spadek temperatury od ciepła
  dT_out = Q_out / (M * C)
  # Oblicz nową temperaturę wody
  T = T + dT_in - dT_out
  # Oblicz nowy czas
  t = t + dt
  # Sprawdź, czy temperatura osiągnęła 100°C
  if t == 100:
    P = 100
  if t == 200:
    P = 2000
  if T >= 100:
    # Ustaw flagę gotowości na True
    k = True
    # Wyświetl komunikat
    print(f"Czajnik gotowy po {t} sekundach.")
  else:
    # Wyświetl aktualną temperaturę
    print(f"Temperatura wody: {T:.2f} °C, czas: {t} s")