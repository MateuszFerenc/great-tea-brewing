# great-tea-brewing
Projekt zaliczeniowy na studia z przedmiotu Podstawy Automatyki

Aby uruchomić projekt należy wykonać następujące kroki:
``` ps
git clone --depth=1 https://github.com/mateuszferenc/great-tee-brewing.git

cd Implementation
python3 -m venv venv
.\venv\Scripts\activate
pip3 install -r ../requirements.txt
python3 main.py 
```

~~Proces produkcji herbaty będzie polegać na odmierzeniu konkretnej ilości wody i zagotowaniu jej (boiler), a następnie wymieszanie jej (mixer) z ziołami herbaty.~~

~~Szczegóły procesu będą polegały na:~~
~~- kontroli poziomu wody w kotle (boiler -> level Hi/Mid/Lo)~~
~~- kontroli temperatury wody w kotle (boiler -> temp)~~
~~- sterowaniu grzałką (heater) na podstawie temperatury oraz poziomu wody w zbiorniku (zabezpieczenie przed podgrzewaniem pustego kotła)~~
~~- kontroli poziomu ziół herbacianych (herbs tank -> Level Hi/Mid/Lo)~~
~~- kontroli silnika mieszającego zioła w mieszalniku (mixer -> motor -> tachometer)~~
~~- kontroli zaworów odpowiedzialnych za poszczególne części procesu (Vx, gdzie x to numer zaworu)~~

# Klauzula informacyjna
Zastrzegamy prawo do wykorzystania informacji zawartych w tym projekcie, oraz zrzekamy się odpowiedzialności za szkody powstałe na skutek realizacji tego projektu jako układu rzeczywistego. Gdyż modele, schematy oraz inne informacje są hipotetyczne i nie nadają się do bezpośredniego wykorzystania w końcowej realizacji układu.

***Pełna treść klauzuli znajduje się w dokumentacji***:   
Design &#8594; Documentation &#8594; NEW &#8594;Dokumentacja_GreatTeeBrewing.pdf