from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o
from funkcje import funkcje_modelowanie as f_m
from funkcje import funkcje_raportowanie as f_r



print "start"
rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

f_r.zapis_ludnosc("rezultaty/ludnosc.csv",rynek.swiat)
#
# firma.przypisz_koszty()
#
# for t in range(5):
#     for sklep in firma.sklepy:
#         sklep.dostawa_towaru(rynek, symulowany_towar=100,inne_towary=100)
#     rynek.sprzedaz_w_sklepach()
#     rynek.nowa_tura()
#
# training = f_m.training(firma.sklepy)
#
#
# for t in range(5):
#     for sklep in firma.sklepy:
#       sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
#       sklep.przewidywana_sprzedaz = 10
#     f_o.dostawy_optymalne(firma,rynek)
#     rynek.sprzedaz_w_sklepach()
#
#
#
# for t in range(5):
#     for sklep in firma.sklepy:
#         sklep.dostawa_towaru(rynek, symulowany_towar=100,inne_towary=100)
#     rynek.sprzedaz_w_sklepach()
#     rynek.nowa_tura()






