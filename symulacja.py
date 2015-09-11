from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o

rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

firma.przypisz_koszty()

prognozowana = []

for sklep in firma.sklepy:

    sklep.przewidywana_sprzedaz = 10
    prognozowana.append((sklep.symbol,sklep.przewidywana_sprzedaz))
rynek.sprzedaz_w_sklepach()



firma.wypisz_wyniki()

punkty_stacjonarne = f_o.punkty_stacjonarne(firma,prognozowana)

f_o.dostawy_optymalne(firma,rynek)

for sklep in firma.sklepy:
    print sklep.sklad