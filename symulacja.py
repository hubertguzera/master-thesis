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
rynek1 = pickle.load(open("Rynek.p","rb"))
rynek = rynek1
firma = rynek.symulowana_firma
firma.przypisz_koszty()

#Statystyka
funkcje_mapa.rysujmapefirmy(rynek.swiat,"mapy/firma")
f_r.zapis_ludnosc("rezultaty/ludnosc.csv",rynek.swiat)
f_r.zapis_produkty("rezultaty/produkty.csv",rynek)




f_r.zapis_prognoza("rezultaty/prognoza.csv",rynek,czysc=True)


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
f_r.zapis_przychody("rezultaty/przychody_zero,csv",rynek, czysc=True)
f_r.zapis_koszty("rezultaty/koszty_zero.csv",rynek, czysc=True)
for t in range(2):
    for sklep in firma.sklepy:
        sklep.dostawa_towaru(rynek, symulowany_towar=srednia_globalna_sprzedaz,inne_towary=100, trasa="Los")
    rynek.sprzedaz_w_sklepach()
    f_r.zapis_koszty("rezultaty/przychody_zero.csv",rynek)
    f_r.zapis_przychody("rezultaty/koszty_zero,csv",rynek)
    rynek.nowa_tura()



#2. optymalizacja stale efekty
print "start"

rynek2 = pickle.load(open("Rynek.p","rb"))
rynek=rynek2
firma = rynek.symulowana_firma
firma.przypisz_koszty()

f_r.zapis_przychody("rezultaty/przychody_jeden,csv",rynek, czysc=True)
f_r.zapis_koszty("rezultaty/koszty_jeden.csv",rynek, czysc=True)

for t in range(2):
    for sklep in firma.sklepy:
        sklep.dostawa_towaru(rynek, symulowany_towar=srednia_globalna_sprzedaz,inne_towary=100, trasa="Los")
    rynek.sprzedaz_w_sklepach()
    f_r.zapis_koszty("rezultaty/przychody_jeden.csv",rynek)
    f_r.zapis_przychody("rezultaty/koszty_jeden.csv",rynek)
    rynek.nowa_tura()


print "Tworze modele predykcyjne"
training = f_m.training(firma.sklepy)


for t in range(2):
     for sklep in firma.sklepy:
       sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
       print "Przewiduje sprzedaz"
       prognoza = f_m.prognozuj_sprzedaz(sklep.klienci_historycznie,training)
       sklep.przewidywana_sprzedaz = prognoza
     print "Rozdzielam dostawy"
     f_o.dostawy_optymalne(firma,rynek)
     rynek.sprzedaz_w_sklepach()
     f_r.zapis_prognoza("rezultaty/prognoza_jeden.csv",rynek)
     f_r.zapis_koszty("rezultaty/koszty_jeden.csv",rynek)
     f_r.zapis_przychody("rezultaty/przychody_jeden.csv",rynek)
     rynek.nowa_tura()
     print "Nastepny krok!"


#3. optymalizacja efekty skali

zalozenia.skala_fabryka = 1.2
zalozenia.skala_magazyny = 1.2
zalozenia.skala_sklepy = 1.2
zalozenia.skala_sciezka = 1.2


print "start"
rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma
firma.przypisz_koszty()

f_r.zapis_przychody("rezultaty/przychody_dwa,csv",rynek, czysc=True)
f_r.zapis_koszty("rezultaty/koszty_dwa.csv",rynek, czysc=True)

for t in range(2):
    for sklep in firma.sklepy:
        sklep.dostawa_towaru(rynek, symulowany_towar=srednia_globalna_sprzedaz,inne_towary=100, trasa="Los")
    rynek.sprzedaz_w_sklepach()
    f_r.zapis_koszty("rezultaty/przychody_dwa.csv",rynek)
    f_r.zapis_przychody("rezultaty/koszty_dwa.csv",rynek)
    rynek.nowa_tura()


print "Tworze modele predykcyjne"
training = f_m.training(firma.sklepy)


for t in range(2):
     for sklep in firma.sklepy:
       sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
       print "Przewiduje sprzedaz"
       prognoza = f_m.prognozuj_sprzedaz(sklep.klienci_historycznie,training)
       sklep.przewidywana_sprzedaz = prognoza
     print "Rozdzielam dostawy"
     f_o.dostawy_optymalne(firma,rynek)
     rynek.sprzedaz_w_sklepach()
     f_r.zapis_prognoza("rezultaty/prognoza_dwa.csv",rynek)
     f_r.zapis_koszty("rezultaty/koszty_dwa.csv",rynek)
     f_r.zapis_przychody("rezultaty/przychody_dwa.csv",rynek)
     rynek.nowa_tura()
     print "Nastepny krok!"
