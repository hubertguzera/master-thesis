from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o

rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

firma.przypisz_koszty()

for sklep in firma.sklepy:
    sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
    sklep.przewidywana_sprzedaz = 10


f_o.dostawy_optymalne(firma,rynek)
for sklep in firma.sklepy:
    print sklep.sklad


rynek.sprzedaz_w_sklepach()
for sklep in firma.sklepy:
    print sklep.sklad
    print sklep.klienci_historycznie

firma.wypisz_wyniki()