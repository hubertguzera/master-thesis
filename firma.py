# -*- coding: utf-8 -*-
import zalozenia,pickle, random
from generowanie_swiata import swiat,lokalizacja,konsument
from sklearn import tree
import sympy
import csv
from funkcje import funkcje_analizadanych as f_a
from funkcje import funkcje_firma as f_f
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_mapa as f_m
from funkcje import funkcje_raportowanie as f_r

class rynek(object):
      def __init__(self,swiat):
            self.tura = 0
            self.swiat = swiat
            self.symulowana_firma = firma(swiat)
            self.produkty_na_rynku = [self.symulowana_firma.produkt.macierz_cech] + [produkt().macierz_cech for x in range(zalozenia.ilosc_produktow)]

      def sprzedaz_w_sklepach(self):
          #przeniesc do firma?
        clf = f_a.czytajdaneklientow("dane/cechy2")
        self.symulowana_firma.klienci_w_sklepach(self.swiat,self.tura)
        for sklep in self.symulowana_firma.sklepy:
              for klient in sklep.klienci:
                    tabela_y = []
                    for produkt in self.produkty_na_rynku:
                          tabela_x = klient + produkt[1:]
                          tabela_y.append([produkt[0],clf.predict_proba(tabela_x)[0][1]])
                    k=0
                    while sklep.sklad:
                          k+=1
                          wybor = f_f.prawdopodobienstwo_zakupu_piwa(tabela_y)
                          if sklep.sprzedaz_w_sklepie(wybor) or k==4:
                                sklep.klienci_historycznie[self.tura].append(klient+[wybor])
                                f_r.zapis_decyzje("rezultaty/decyzje.csv",klient+[wybor],self)
                                break
      def nowa_tura(self):
          #zapisywanie statystyk po turze?
            self.tura += 1
            for sklep in self.symulowana_firma.sklepy:
                  sklep.klienci = []
                  sklep.sklad = {}
                  sklep.sprzedaz = {}
                  sklep.oblozenie = 0
                  sklep.klienci_historycznie.append([])
            for fabryka in self.symulowana_firma.fabryki:
                fabryka.oblozenie = 0
            for magazyn in self.symulowana_firma.magazyny:
                magazyn.oblozenie = 0
            for trasa in self.symulowana_firma.trasy.trasy:
                trasa.oblozenie = 0
                trasa.udzial = 0
            for sciezka in self.symulowana_firma.trasy.drogi:
                sciezka.oblozenie = 0




class firma(object):
      def __init__(self, swiat):
          self.fabryki = [fabryka(swiat,x) for x in range(zalozenia.ilosc_fabryk)]
          self.magazyny = [magazyn(swiat,x) for x in range(zalozenia.ilosc_magazyn)]
          self.sklepy = [sklep(swiat,x) for x in range(zalozenia.ilosc_sklepow)]
          self.trasy = trasy(self,swiat)
          self.produkt = produkt(True)
          self.wyniki = []
          self.cena = zalozenia.produkt_cena

      def klienci_w_sklepach(self,swiat,tura=0): #zmienic nazwe funkcji
          print "Przyporzadkowuje klientow do sklepu..."
          for sklep in self.sklepy : sklep.klienci = []
          i= 0
          for czlowiek in swiat.ludnosc:
            i+=1
            #odwiedzone = czlowiek.odwiedzony_sklep(swiat)
            if czlowiek.mozliwe_sklepy:
                odwiedzone = random.choice(czlowiek.mozliwe_sklepy)
            else:
                odwiedzone = []
            for sklep in self.sklepy:
                if sklep.lokalizacja == odwiedzone:
                    sklep.klienci.append(czlowiek.macierz_cech())
          print "Skonczylem przyporzadkowywac"


      def przypisz_koszty(self,losowe=False,skala=False,min_cen=0.8,max_cena=1.3,min_skala=0.9,max_skala=1.1):
          for item in self.fabryki:
              item.koszt = zalozenia.koszt_fabryka * item.symbol ** zalozenia.skala_fabryka

          for item in self.sklepy:
              item.koszt = zalozenia.koszt_sklepy * item.symbol ** zalozenia.skala_sklepy

          for item in self.magazyny:
              item.koszt = zalozenia.koszt_magazyny * item.symbol ** zalozenia.skala_magazyny

          for item in self.trasy.drogi:
              item.koszt = zalozenia.koszt_sciezka * item.odleglosc * item.symbol ** zalozenia.skala_sciezka


class fabryka(firma):
    def __init__(self,swiat,x):
        self.nazwa = "Fabryka"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.droga = swiat.mapa[self.lokalizacja[0]][self.lokalizacja[1]].droga[0]
        self.oblozenie = 0
        self.symbol = sympy.symbols("f" + str(x+1))
        self.koszt = 0


class magazyn(firma):
    def __init__(self,swiat, x):
        self.nazwa = "Magazyn"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.droga = swiat.mapa[self.lokalizacja[0]][self.lokalizacja[1]].droga[0]
        self.oblozenie = 0
        self.symbol = sympy.symbols("m" + str(x+1))
        self.koszt = 0


class sklep(firma):
    def __init__(self,swiat,x):
        self.nazwa = "Sklep"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.droga = swiat.mapa[self.lokalizacja[0]][self.lokalizacja[1]].droga[0]
        self.klienci = []
        self.klienci_historycznie = [[]]
        self.sklad = {}
        self.sprzedaz = {}
        self.oblozenie = 0
        self.symbol = sympy.symbols("s" + str(x+1))
        self.koszt = 0

        self.przewidywana_sprzedaz = 0

    def dostawa_towaru(self, rynek, trasa=None,symulowany_towar = 30,inne_towary=30):
        for produkt in rynek.produkty_na_rynku:
            #to można wrzucić do funkcji
              if produkt[0] == rynek.symulowana_firma.produkt.nazwa:
                    if produkt[0] in self.sklad:
                        self.sklad[produkt[0]] += symulowany_towar
                    else:
                        self.sklad[produkt[0]] = symulowany_towar
              else:
                    if produkt[0] in self.sklad:
                        self.sklad[produkt[0]] += inne_towary
                    else:
                        self.sklad[produkt[0]] = inne_towary
        b = []
        if trasa=="Los":
            for element in rynek.symulowana_firma.trasy.trasy:
                if element.elementy[2].lokalizacja==self.lokalizacja:
                    b.append(element)
            trasa = random.choice(b)
        if trasa=="Krotka":
            d = {}
            for element in rynek.symulowana_firma.trasy.trasy:
                if element.elementy[2].lokalizacja==self.lokalizacja:
                    d[element] =  element.elementy[4].koszt.subs(element.elementy[4].symbol,1).evalf()
                    print self.symbol,element.symbol,d[element]
            trasa = min(d.items(), key=lambda x: x[1])[0]
            print "wybrana", trasa.symbol
        rynek.symulowana_firma.trasy.dodaj_do_trasy(symulowany_towar,trasa)

    def sprzedaz_w_sklepie(self,towar):
        #zmienic nazwy
        if towar in self.sklad and self.sklad[towar]>0:
              self.sklad[towar] += -1
              if self.sklad[towar] == 0:
                    del self.sklad[towar]
              if towar in self.sprzedaz: 
                    self.sprzedaz[towar] += 1
              else:
                    self.sprzedaz[towar] = 1
              return True
        else:
              return False

class produkt(object):
      def __init__(self,symulowany=False):
        if symulowany:
            self.nazwa = "Symulowane"
        else:
            self.nazwa = f_p.losuj_bez_powtorzen(zalozenia.mozliwe_nazwy,zalozenia.niedozwolone_nazwy)
        self.macierz_cech = f_p.wylosuj_cechy_piwa(self.nazwa,symulowany)

class trasy(firma):
    def __init__(self,firma,swiat):
        self.drogi = []
        self.trasy = []
        k=0
        for item in (f_f.kombinacja_wszytkich_lokalizacji([firma.fabryki , firma.magazyny]) + f_f.kombinacja_wszytkich_lokalizacji([firma.magazyny, firma.sklepy])):
            self.drogi.append(sciezka(item[0],item[1],swiat,k))
            k+=1
        k=0
        for item in f_f.kombinacja_wszytkich_lokalizacji([firma.fabryki , firma.magazyny, firma.sklepy]):
            for droga in self.drogi:
                if (droga.poczatek == item[0] and droga.koniec == item[1]) or (droga.poczatek == item[1] and droga.koniec == item[2]):
                    item.append(droga)
            self.trasy.append(trasa(item,k))
            k+=1


    def dodaj_do_trasy(self,ilosc,trasa):
        for key in self.trasy:
            if key==trasa:
                key.oblozenie += ilosc
                for item in key.elementy:
                    item.oblozenie += ilosc


class trasa(trasy):
    def __init__(self,elementy,x):
        self.elementy = elementy
        self.oblozenie = 0
        self.udzial = 0
        self.symbol = self.symbol = sympy.symbols("t" + str(x+1))



class sciezka(trasy):
    def __init__(self,poczatek,koniec,swiat,x):
        self.poczatek = poczatek
        self.koniec = koniec
        self.odleglosc = len(f_m.szukaj_drogi(swiat.nodes,tuple(poczatek.droga),tuple(koniec.droga),nowy=True))
        self.oblozenie = 0
        self.symbol = sympy.symbols("r" + str(x+1))
        self.koszt = 0


def tworz_swiat_i_rynek():
    symulowany_swiat = swiat()
    pickle.dump(symulowany_swiat ,open("Swiat.p","wb"))
    symulowany_swiat = pickle.load(open("Swiat.p","rb"))
    symulowany_rynek = rynek(symulowany_swiat)
    for czlowiek in symulowany_rynek.swiat.ludnosc:
        czlowiek.mozliwe_sklepy = czlowiek.wypisz_mozliwe_sklep(symulowany_rynek.swiat)
    #print symulowany_swiat.nodes
    pickle.dump(symulowany_rynek,open("Rynek.p","wb"))
    f_m.rysujmape(symulowany_rynek.swiat,"mapy/typy")
    f_m.rysujludnosc(symulowany_rynek.swiat, symulowany_rynek.swiat.ludnosc,"mapy/ludnosc")
    f_m.rysujmapefirmy(symulowany_rynek.swiat,"mapy/firma")
    f_r.zapis_ludnosc("rezultaty/ludnosc.csv",symulowany_rynek.swiat)
    f_r.zapis_produkty("rezultaty/produkty.csv",symulowany_rynek)

#tworz_swiat_i_rynek()


# for sklep in symulowany_rynek.symulowana_firma.sklepy:
#      sklep.dostawa_towaru(symulowany_rynek,symulowany_rynek.trasy.kombinacje[f_p.wypisz_trasy(sklep,symulowany_rynek.trasy.kombinacje)])
# symulowany_rynek.sprzedaz_w_sklepach()
# for sklep in symulowany_rynek.symulowana_firma.sklepy:
#      print "sprzedaż", sklep.sprzedaz
#
# expr = 0
# alfa = sympy.symbols('alfa')
# for item in symulowany_rynek.symulowana_firma.fabryki:
#     expr = expr + item.symbol * item.oblozenie ** alfa
#
# for item in symulowany_rynek.symulowana_firma.magazyny:
#     expr = expr + item.symbol * item.oblozenie ** alfa
#
# for item in symulowany_rynek.symulowana_firma.sklepy:
#     expr = expr + item.symbol * item.oblozenie ** alfa
#
# print "111",expr
# print sympy.simplify(expr.subs(alfa,0.5)).subs("f0",1)

# for i in range(0,3):
#      symulowany_rynek.symulowana_firma.klienci_w_sklepach(symulowany_swiat,i)
#      symulowany_rynek.nowa_tura()
# symulowany_rynek.symulowana_firma.klienci_w_sklepach(symulowany_swiat,2)
# for sklep in symulowany_rynek.symulowana_firma.sklepy:
#      print sklep.klienci_historycznie


print "---"