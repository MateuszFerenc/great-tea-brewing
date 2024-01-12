# Parametry czajnika
V = 230 # napięcie (V)
R = 20 # oporność (ohm)
c = 4190 # ciepło właściwe wody (J/kg°C)
rho = 1000 # gęstość wody (kg/m^3)
V_w = 0.0015 # objętość wody (m^3)
T_1 = 20 # temperatura początkowa wody (°C)
T_env = 25 # temperatura otoczenia (°C)
h = 10 # współczynnik przenikania ciepła (W/m^2°C)
l = 0.2 # długość czajnika (m)
w = 0.15 # szerokość czajnika (m)
h = 0.1 # wysokość czajnika (m)

# Obliczenia
P = V**2 / R # moc grzałki (W)
m = rho * V_w # masa wody (kg)
A = 2 * (l * w + l * h + w * h) # powierzchnia ścianek czajnika (m^2)
T_2 = T_1 # temperatura końcowa wody (°C)
t = 0 # czas (s)

print(f"moc grzalki: {P}")
# Symulacja
while T_2 < 100: # pętla do momentu zagotowania wody
  Q = P * t # ciepło dostarczone przez grzałkę (J)
  Q_loss = h * A * (T_2 - T_env) * t # ciepło utracone przez ścianki czajnika (J)
  Q_net = Q - Q_loss # ciepło netto dostarczone do wody (J)
  delta_T = Q_net / (c * m) # zmiana temperatury wody (°C)
  T_2 = T_1 + delta_T # temperatura końcowa wody (°C)
  print(f"Po {t} sekundach temperatura wody wynosi {T_2:.2f} °C") # wyświetlenie wyniku
  t += 1 # zwiększenie czasu o 1 sekundę