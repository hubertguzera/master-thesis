# -*- coding: utf-8 -*-
import zalozenia,pickle, random
from generowanie_swiata import swiat,lokalizacja,konsument
from sklearn import tree
import funkcje_analizadanych as f_a
import funkcje_firma as f_f
import funkcje_pomocnicze as f_p
import funkcje_mapa as f_m



class rynek(object):
      def __init__(self,swiat):
            self.tura = 0
            self.swiat = swiat
            self.symulowana_firma = firma(swiat)
            self.produkty_na_rynku = [self.symulowana_firma.produkt.macierz_cech] + [produkt().macierz_cech for x in range(zalozenia.ilosc_produktow)]
      def sprzedaz_w_sklepach(self):
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
            self.tura += 1
            for sklep in self.symulowana_firma.sklepy:
                  sklep.klienci = []
                  sklep.sklad = {}
                  sklep.sprzedaz = {}
                  sklep.klienci_historycznie.append([])

              
class firma(object):
      def __init__(self, swiat):
          self.fabryki = [fabryka(swiat) for x in range(zalozenia.ilosc_fabryk)]
          self.magazyny = [magazyn(swiat) for x in range(zalozenia.ilosc_magazyn)]
          self.sklepy = [sklep(swiat) for x in range(zalozenia.ilosc_sklepow)]
          self.produkt = produkt(1)
      def klienci_w_sklepach(self,swiat,tura=0):
          print "Przyporządkowuje klientow do sklepu..."
          for sklep in self.sklepy : sklep.klienci = []
          for czlowiek in swiat.ludnosc:
            for sklep in self.sklepy:             
                        if sklep.lokalizacja == czlowiek.odwiedzony_sklep(swiat):
                              sklep.klienci.append(czlowiek.macierz_cech())
                              sklep.klienci_historycznie[tura].append(czlowiek.macierz_cech())
          print "Skonczylem przyporzadkowywac"
          
class fabryka(firma):
    def __init__(self,swiat):
        self.nazwa = "Fabryka"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        
class magazyn(firma):
    def __init__(self,swiat):
        self.nazwa = "Magazyn"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)

class sklep(firma):
    def __init__(self,swiat):
        self.nazwa = "Sklep"
        self.lokalizacja = f_f.wybierz_lokalizacje(swiat,"Przestrzen komercyjna",self.nazwa)
        self.klienci = []
        self.klienci_historycznie = [[]]
        self.sklad = {}
        self.sprzedaz = {}
    def dostawa_towaru(self,rynek, symulowany_towar = 999,inne_towary=999):
        self.sklad={}
        for produkt in rynek.produkty_na_rynku:
              if produkt[0] == rynek.symulowana_firma.produkt.nazwa:
                    self.sklad[produkt[0]] = symulowany_towar
              else:
                    self.sklad[produkt[0]] = inne_towary

    def sprzedaz_w_sklepie(self,towar):
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
            zalozenia.niedozwolone_nazwy.append(self.nazwa)
            self.cena = random.randrange(1,6)
            self.smak = random.randrange(1,6)
            self.opakowanie = random.randrange(1,6)
            los = random.randrange(3)
            if los==0:
                  self.premium=1
                  self.budzetowe=0
            if los==1:
                  self.premium=0
                  self.budzetowe=1
            if los==2:
                  self.premium=0
                  self.budzetowe=0
            los = random.randrange(2)
            if los==1:
                  self.lager=1
                  self.smakowe=0
            if los==0:
                  self.lager=0
                  self.smakowe=1
            self.marketing = random.randrange(1,6)
            self.macierz_cech = [self.nazwa,self.cena,self.smak,self.opakowanie,self.premium,self.budzetowe,self.lager,self.smakowe,self.marketing]

#symulowany_swiat = swiat()
#pickle.dump(symulowany_swiat ,open("Swiat.p","wb"))
symulowany_swiat = pickle.load(open("Swiat.p","rb"))
symulowany_rynek = rynek(symulowany_swiat)
f_m.rysujmape(symulowany_swiat,"mapy/po_lokalizacji_sklepow")


for sklep in symulowany_rynek.symulowana_firma.sklepy:
      sklep.dostawa_towaru(symulowany_rynek,10,10)
symulowany_rynek.sprzedaz_w_sklepach()
for sklep in symulowany_rynek.symulowana_firma.sklepy:
      print sklep.sprzedaz
print f_f.zlicz_sprzedaz(symulowany_rynek.symulowana_firma.sklepy,symulowany_rynek.symulowana_firma.produkt.nazwa)

##
##for i in range(0,2):
##      symulowany_rynek.symulowana_firma.klienci_w_sklepach(symulowany_swiat,i)
##      symulowany_rynek.nowa_tura()
##symulowany_rynek.symulowana_firma.klienci_w_sklepach(symulowany_swiat,2)
##for sklep in symulowany_rynek.symulowana_firma.sklepy:
##      for row in sklep.klienci_historycznie:
##            print row
##            raw_input()
##      
      print "---"
