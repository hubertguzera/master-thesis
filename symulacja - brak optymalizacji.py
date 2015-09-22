from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o
from funkcje import funkcje_modelowanie as f_m
from funkcje import funkcje_raportowanie as f_r
from funkcje import funkcje_mapa
import zalozenia




#Ladowanie mapy
print "start"
rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma
firma.przypisz_koszty()

#runda probna
globalna_sprzedaz = 0
for sklep in firma.sklepy:
    sklep.dostawa_towaru(rynek, symulowany_towar=100,inne_towary=100, trasa="Los")
rynek.sprzedaz_w_sklepach()
for sklep in firma.sklepy:
    if "Symulowane" in sklep.sprzedaz:
        globalna_sprzedaz += sklep.sprzedaz["Symulowane"]
        print globalna_sprzedaz
srednia_globalna_sprzedaz = int(globalna_sprzedaz/len(firma.sklepy))
print srednia_globalna_sprzedaz
rynek.nowa_tura()

#1. brak optymalizacji
f_r.zapis_przychody("rezultaty/zero/przychody.csv",rynek, czysc=True)
f_r.zapis_koszty("rezultaty/zero/koszty.csv",rynek, czysc=True)
f_r.zapis_zysk("rezultaty/zero/zysk.csv",rynek, czysc=True)
f_r.zapis_trasy("rezultaty/zero/trasy.csv",rynek, czysc=True)
for t in range(30):
    for sklep in firma.sklepy:
        sklep.dostawa_towaru(rynek, symulowany_towar=srednia_globalna_sprzedaz,inne_towary=100, trasa="Los")
    rynek.sprzedaz_w_sklepach()
    f_r.zapis_koszty("rezultaty/zero/koszty.csv",rynek)
    f_r.zapis_przychody("rezultaty/zero/przychody.csv",rynek)
    f_r.zapis_zysk("rezultaty/zero/zysk.csv",rynek)
    f_r.zapis_trasy("rezultaty/zero/trasy.csv",rynek)
    rynek.nowa_tura()


