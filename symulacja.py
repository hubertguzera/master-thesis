from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o
from funkcje import funkcje_modelowanie as f_m
print "start"
rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

firma.przypisz_koszty()

# for sklep in firma.sklepy:
#     sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
#     sklep.przewidywana_sprzedaz = 10
# f_o.dostawy_optymalne(firma,rynek)
# rynek.sprzedaz_w_sklepach()
# firma.wypisz_wyniki()



for t in range(5):
    for sklep in firma.sklepy:
        sklep.dostawa_towaru(rynek, symulowany_towar=100,inne_towary=100)
    rynek.sprzedaz_w_sklepach()
    rynek.nowa_tura()


for sklep in firma.sklepy:
    print f_m.ilosc_odwiedzajacych(sklep.klienci_historycznie)


# print f_m.wypisz_cechy(f_m.lacz_historie(f_m.historia_wszystkich(firma.sklepy)),0)
# print f_m.licz_cechy(f_m.lacz_historie(f_m.historia_wszystkich(firma.sklepy)),0)
# print f_m.licz_prawdopodobienstwo_cech(f_m.lacz_historie(f_m.historia_wszystkich(firma.sklepy)),0,{1:1})
# print f_m.stworz_konsumenta(f_m.lacz_historie(f_m.historia_wszystkich(firma.sklepy)))

f_m.training(firma.sklepy)

