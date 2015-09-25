from firma import rynek,firma,fabryka,magazyn,sklep,produkt,trasy,sciezka,trasa
from generowanie_swiata import swiat,lokalizacja,konsument
import pickle,sympy
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_optymalizacja as f_o
from funkcje import funkcje_modelowanie as f_m
from funkcje import funkcje_raportowanie as f_r
from funkcje import funkcje_mapa
import zalozenia

rynek = pickle.load(open("Rynek.p","rb"))
firma = rynek.symulowana_firma

f_r.zapis_produkty("rezultaty/produkt.csv",rynek)

# def zapis(czysc=False):
#     if czysc:
#         f_r.zapis_przychody("rezultaty/przychody.csv",rynek, czysc=True)
#         f_r.zapis_koszty("rezultaty/koszty.csv",rynek, czysc=True)
#         f_r.zapis_prognoza("rezultaty/prognoza.csv",rynek,czysc=True)
#         f_r.zapis_zysk("rezultaty/zysk.csv",rynek, czysc=True)
#         f_r.zapis_trasy("rezultaty/trasy.csv",rynek, czysc=True)
#         f_r.zapis_decyzje("rezultaty/decyzje.csv",0,0,czysc=True)
#         f_r.zapis_pojedynczej_prognozy("rezultaty/czesci_prognoz.csv",0,0,czysc=True)
#     else:
#         f_r.zapis_przychody("rezultaty/przychody.csv",rynek,)
#         f_r.zapis_koszty("rezultaty/koszty.csv",rynek)
#         f_r.zapis_prognoza("rezultaty/prognoza.csv",rynek)
#         f_r.zapis_zysk("rezultaty/zysk.csv",rynek)
#         f_r.zapis_trasy("rezultaty/trasy.csv",rynek)
#
#
# #Ladowanie mapy
# print "start"
# rynek = pickle.load(open("Rynek.p","rb"))
# firma = rynek.symulowana_firma
#
# zalozenia.skala_fabryka = 1.03
# zalozenia.skala_magazyny = 1.05
# zalozenia.skala_sklepy = 1.07
# zalozenia.skala_sciezka = 0.95
#
# firma.przypisz_koszty()
#
# print f_o.funkcja_do_optymalizacji(firma)
#
# # runda probna
# globalna_sprzedaz = 0
# for sklep in firma.sklepy:
#     sklep.dostawa_towaru(rynek, symulowany_towar=100,inne_towary=100, trasa="Krotka")
# rynek.sprzedaz_w_sklepach()
#
# for sklep in firma.sklepy:
#     if "Symulowane" in sklep.sprzedaz:
#         globalna_sprzedaz += sklep.sprzedaz["Symulowane"]
# srednia_globalna_sprzedaz = int(globalna_sprzedaz/len(firma.sklepy))
# rynek.nowa_tura()
#
# #3. optymalizacja efekty skali
#
# zapis(True)
# for t in range(20):
#     for sklep in firma.sklepy:
#         sklep.dostawa_towaru(rynek, symulowany_towar=srednia_globalna_sprzedaz,inne_towary=100, trasa="Krotka")
#     rynek.sprzedaz_w_sklepach()
#     zapis()
#     rynek.nowa_tura()
#
# print "Tworze modele predykcyjne"
# training = f_m.training(firma.sklepy)
#
# for t in range(10):
#      for sklep in firma.sklepy:
#        sklep.dostawa_towaru(rynek, symulowany_towar=0,inne_towary=100)
#        print "Przewiduje sprzedaz"
#        prognoza = 20
#        prognoza = int(f_m.prognozuj_sprzedaz(sklep.klienci_historycznie,training,rynek))
#        sklep.przewidywana_sprzedaz = prognoza
#      print "Rozdzielam dostawy"
#      f_o.dostawy_optymalne(firma,rynek)
#      rynek.sprzedaz_w_sklepach()
#      zapis()
#      rynek.nowa_tura()
#      print "Nastepny krok!"
