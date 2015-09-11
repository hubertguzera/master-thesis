import random,zalozenia
import sympy

def konwertuj_wyksztalcenie(wyksztalcenie):
   mozliwosci = {"Podstawowe":1,"Zawodowe":2,"Srednie":3,"Wyzsze":4,"Brak":0}
   return mozliwosci[wyksztalcenie]
      
def konwertuj_zainteresowania(zainteresowania):
   mozliwe = ["moda","gotowanie","finanse","kultura","historia","koncerty","motoryzacja","kosmetyki","malarstwo","ogrodnictwo","gry","sport","boks","fotografia","kulturaalternatywna","nightlife","teatr","ksiazka","historiapolski","natura","piwowarstwo","muzykaklasyczna","ksiazki"]
   macierz = [0 for x in range(23)]
   for item in zainteresowania:
      for i in range(len(mozliwe)):
         if item==mozliwe[i]:
            macierz[i]=1
   return macierz
         
def losuj_bez_powtorzen(losuj_z,sprawdz_z=[]):
   wybor = random.choice(losuj_z)
   while wybor in sprawdz_z:
      wybor = random.choice(losuj_z)
   return wybor

def dodaj_piksele(*tuples):
   return map(sum, zip(*tuples))

def wylosuj_cechy_piwa(nazwa, symulowany):

    zalozenia.niedozwolone_nazwy.append(nazwa)
    cena = random.randrange(1,6)
    smak = random.randrange(1,6)
    opakowanie = random.randrange(1,6)
    los = random.randrange(3)
    if los==0:
          premium=1
          budzetowe=0
    if los==1:
          premium=0
          budzetowe=1
    if los==2:
          premium=0
          budzetowe=0
    los = random.randrange(2)
    if los==1:
          lager=1
          smakowe=0
    if los==0:
          lager=0
          smakowe=1
    marketing = random.randrange(1,6)
    return [nazwa,cena,smak,opakowanie,premium,budzetowe,lager,smakowe,marketing]

def wypisz_cechy_klienta(wiek,plec,wyksztalcenie,zarobki,zainteresowania):
        tablica = []
        tablica.append(wiek)
        if plec=="Kobieta":
            tablica = tablica + [1,0]
        else:
            tablica = tablica + [0,1]
        tablica.append(wyksztalcenie)
        tablica.append(int(zarobki))
        tablica.append(0)
        tablica = tablica + konwertuj_zainteresowania(zainteresowania)
        return tablica

def wypisz_trasy(element,trasy):
    a = []
    for item in trasy:
        if element in item.elementy:
            a.append(trasy.index(item))
    return random.choice(a)

def koszt_jednostki(jednostka):
    return jednostka.koszt*jednostka.oblozenie**jednostka.efekt_skala

def koszt_trasy(trasa):
    oblozenie = trasa.oblozenie
    koszt = 0
    for jednostka in trasa.elementy:
        koszt += jednostka.koszt*oblozenie**jednostka.efekt_skala
    return koszt

