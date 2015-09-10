from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p

rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

firma.przypisz_koszty()

podmien = []

for sklep in firma.sklepy:
    sklep.dostawa_towaru(rynek,firma.trasy.trasy[f_p.wypisz_trasy(sklep,firma.trasy.trasy)])
    sklep.przewidywana_sprzedaz = 10
    podmien.append((sklep.symbol,sklep.przewidywana_sprzedaz))
rynek.sprzedaz_w_sklepach()



firma.wypisz_wyniki()

print f_p.funkcja_do_optymalizacji(firma)

print f_p.podstaw(f_p.funkcja_do_optymalizacji(firma),podmien)

print sympy.expand(f_p.podstaw(f_p.funkcja_do_optymalizacji(firma),podmien))