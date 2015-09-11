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
                                break
      def nowa_tura(self):
          #zapisywanie statystyk po turze?
            self.tura += 1
            for sklep in self.symulowana_firma.sklepy:
                  sklep.klienci = []
                  sklep.sklad = {}
                  sklep.sprzedaz = {}
                  sklep.klienci_historycznie.append([])
            for fabryka in self.symulowana_firma.fabryki:
                fabryka.oblozenie = 0
            for magazyn in self.symulowana_firma.magazyny:
                magazyn.oblozenie = 0
            for key in self.trasy.trasy:
                self.trasy.trasy[key] = 0
            for droga in self.trasy.drogi:
                droga.oblozenie = 0



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
          for czlowiek in swiat.ludnosc:
            print swiat.ludnosc.index(czlowiek) , "/" , str(len(swiat.ludnosc))
            odwiedzone = czlowiek.odwiedzony_sklep(swiat)
            for sklep in self.sklepy:             
                        if sklep.lokalizacja == odwiedzone:
                              sklep.klienci.append(czlowiek.macierz_cech())
                              sklep.klienci_historycznie[tura].append(czlowiek.macierz_cech())
          print "Skonczylem przyporzadkowywac"

      def wypisz_wyniki(self):

          wyniki_csv = open("rezultaty/koszty.csv",'wb')
          wr = csv.writer(wyniki_csv )
          wr.writerow(["Symbol","Oblozenie","Koszt jednostkowy","Efekt skali","Koszt"])

          for item in self.fabryki + self.magazyny + self.sklepy:
              self.wyniki.append([item.symbol,item.oblozenie,item.koszt,item.efekt_skala,f_p.koszt_jednostki(item)])
          wr.writerows(self.wyniki)

          self.wyniki = []

          wyniki_csv = open("rezultaty/trasy.csv",'wb')
          wr = csv.writer(wyniki_csv)
          wr.writerow(["Fabryka","Magazyn","Sklep","Droga1","Droga2","Oblozenie"])

          for item in self.trasy.trasy:
              temp = []
              for jednostka in item.elementy:
                  temp.append(jednostka.symbol)
              self.wyniki.append(temp+[item.oblozenie]+[f_p.koszt_trasy(item)])
          wr.writerows(self.wyniki)
          self.wyniki = []

          wyniki_csv = open("rezultaty/wyniki.csv",'wb')
          wr = csv.writer(wyniki_csv)
          wr.writerow(["Fabryka","Magazyn","Sklep","Droga1","Droga2","Oblozenie"])

          for sklep in self.sklepy:
              if "Symulowane" in sklep.sprzedaz:
                  temp2 = sklep.sprzedaz["Symulowane"]
              else:
                  temp2 = 0

              temp = [sklep.symbol,temp2,temp2 * self.cena]
              temp3=0

              for item in self.trasy.trasy:
                  if sklep in item.elementy:
                      temp3 += f_p.koszt_trasy(item)

              self.wyniki.append(temp+[temp2]+[temp2*self.cena-temp3])
          wr.writerows(self.wyniki)
          self.wyniki = []


      def przypisz_koszty(self,losowe=False,skala=False,min_cen=0.8,max_cena=1.3,min_skala=0.9,max_skala=1.1):
          for item in self.fabryki:
              if  not(losowe):
                  item.koszt = zalozenia.koszt_fabryka
                  item.efekt_skala = zalozenia.skala_fabryka
              else:
                  item.koszt = random.uniform(min_cen, max_cena)
                  item.efekt_skala = random.uniform(min_skala, max_skala)
          for item in self.sklepy:
              if not(losowe):
                  item.koszt = zalozenia.koszt_sklepy
                  item.efekt_skala = zalozenia.skala_sklepy
              else:
                  item.koszt = random.uniform(min_cen, max_cena)
                  item.efekt_skala = random.uniform(min_skala, max_skala)
          for item in self.magazyny:
              if not(losowe):
                  item.koszt = zalozenia.koszt_magazyny
                  item.efekt_skala = zalozenia.skala_magazyny
              else:
                  item.koszt = random.uniform(min_cen, max_cena)
                  item.efekt_skala = random.uniform(min_skala, max_skala)
          for item in self.magazyny:
              if not(losowe):
                  item.koszt = zalozenia.koszt_magazyny
                  item.efekt_skala = zalozenia.skala_magazyny
              else:
                  item.koszt = random.uniform(min_cen, max_cena)
                  item.efekt_skala = random.uniform(min_skala, max_skala)
          for item in self.trasy.drogi:
              if not(losowe):
                  item.koszt = zalozenia.koszt_sciezka * item.odleglosc
                  item.efekt_skala = zalozenia.skala_sciezka
                  print item.koszt
              else:
                  item.koszt = random.uniform(min_cen, max_cena) * item.odleglosc
                  item.efekt_skala = random.uniform(min_skala, max_skala)

class fabryka(firma):
    def __init__(self,swiat,x):
        self.nazwa = "Fabryka"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.droga = swiat.mapa[self.lokalizacja[0]][self.lokalizacja[1]].droga[0]
        self.oblozenie = 0
        self.symbol = sympy.symbols("f" + str(x+1))
        self.koszt = 0
        self.efekt_skali = 0

class magazyn(firma):
    def __init__(self,swiat, x):
        self.nazwa = "Magazyn"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.droga = swiat.mapa[self.lokalizacja[0]][self.lokalizacja[1]].droga[0]
        self.oblozenie = 0
        self.symbol = sympy.symbols("m" + str(x+1))
        self.koszt = 0
        self.efekt_skali = 0

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
        self.efekt_skali = 0
        self.przewidywana_sprzedaz = 0

    def dostawa_towaru(self, rynek, trasa,symulowany_towar = 30,inne_towary=30):
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
            if key.elementy==trasa:
                key.oblozenie += ilosc
                for item in key.elementy:
                    item.oblozenie += ilosc


class trasa(trasy):
    def __init__(self,elementy,x):
        self.elementy = elementy
        self.oblozenie = 0
        self.udzial = 0
        self.symbol = self.symbol = sympy.symbols("t" + str(x+1))


    def dodaj_do_trasy(self,ilosc,trasa):
        for key in self.trasy:
            if key==tuple(trasa):
                self.trasy[key] += ilosc
                for item in key:
                    item.oblozenie += ilosc

class sciezka(trasy):
    def __init__(self,poczatek,koniec,swiat,x):
        self.poczatek = poczatek
        self.koniec = koniec
        self.odleglosc = len(f_m.szukaj_drogi(swiat.nodes,tuple(poczatek.droga),tuple(koniec.droga),nowy=True))
        self.oblozenie = 0
        self.symbol = sympy.symbols("r" + str(x+1))
        self.koszt = 0
        self.efekt_skali = 0


#symulowany_swiat = swiat()
#pickle.dump(symulowany_swiat ,open("Swiat.p","wb"))
#symulowany_swiat = pickle.load(open("Swiat.p","rb"))
#symulowany_rynek = rynek(symulowany_swiat)
#print symulowany_swiat.nodes
#pickle.dump(symulowany_rynek,open("Rynek.p","wb"))



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