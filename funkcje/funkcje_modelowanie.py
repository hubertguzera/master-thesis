import itertools,random
import zalozenia
from funkcje import funkcje_pomocnicze as f_p
from sklearn.metrics.pairwise import euclidean_distances
import numpy as np

class training(object):
    def __init__(self,sklepy):
        self.kolejnosc = []
        for subset in itertools.permutations([i for i in range(zalozenia.zakres_prawdopodobienstwa_warunkowego)]):
            self.kolejnosc.append(list(subset) + [i for i in range(zalozenia.zakres_prawdopodobienstwa_warunkowego,29)])
        self.historia = lacz_historie(historia_wszystkich(sklepy))
        self.training = self.historia[:int(len(self.historia)*zalozenia.udzial_treningowe)]
        a = {}
        for kombinacja in self.kolejnosc:
            print self.kolejnosc.index(kombinacja),"/",len(self.kolejnosc)
            training_y = []
            for i in range(len(self.training)):
                training_y.append(stworz_konsumenta(self.training))
            a[tuple(kombinacja)]= np.mean(euclidean_distances(f_p.bez_ostatniej_kolumny(self.training), training_y))
        self.kolejnosc = a.keys()[0]
        for key in a:
            if a[key]<a[self.kolejnosc]:
                self.kolejnosc = key
        self.historia= f_p.usun_kolumny(lacz_historie(historia_wszystkich(sklepy)),zalozenia.znane_cechy)
        for item in self.historia:
            if item[len(item)-1] == "Symulowane":
                item[len(item)-1] = 1
            else:
                item[len(item)-1] = 0
            print item


def ilosc_odwiedzajacych(historia_sklepu):
    a = []
    for zapis in historia_sklepu:
        a.append(len(zapis))
    return int(sum(a)/len(a))

def historia_wszystkich(sklepy):
    a = []
    for sklep in sklepy:
        a = a + sklep.klienci_historycznie
    return a

def lacz_historie(historia_sklepu):
    a = []
    for item in historia_sklepu:
        for further_item in item:
            a.append(further_item)
    return a

def wypisz_cechy(historia_sklepu,i):
    a=[]
    for transakcja in historia_sklepu:
            if not(transakcja[i] in a):
                a.append(transakcja[i])
    return a

def licz_cechy(historia_sklepu,i,dotychczasowe=False):
    a={}
    for transakcja in historia_sklepu:
            if dotychczasowe:
                for key in dotychczasowe:
                    if transakcja[key]==dotychczasowe[key]:
                        status = True
                    else:
                        status = False
            else:
                status = True
            if status:
                if not(transakcja[i] in a):
                    a[transakcja[i]]=float(1)
                else:
                    a[transakcja[i]]+1
    return a

def licz_prawdopodobienstwo_cech(historia_sklepu,i,dotychczasowe=False):
    a = licz_cechy(historia_sklepu,i,dotychczasowe)
    suma = sum(a.values())
    for key in a:
        a[key] = a[key]/suma
    return a


def losuj_niestandardowy(prawdopodobienstwa):
    max_p = sum(prawdopodobienstwa.values())
    los = random.random()*max_p
    skumulowany = 0
    for key in prawdopodobienstwa:
        if los > skumulowany and los < skumulowany + prawdopodobienstwa[key]:
            return key
            break
        else:
            skumulowany += prawdopodobienstwa[key]
    return random.choice(prawdopodobienstwa.keys())

def stworz_konsumenta(historia_sklepu):
     kolejnosc = [i for i in range(29)]
     cechy = [[] for i in range(29) ]
     dotychczasowe = {}
     for i in kolejnosc:
         wylosowana_cecha = losuj_niestandardowy(licz_prawdopodobienstwo_cech(historia_sklepu,i,dotychczasowe))
         cechy[i] = wylosowana_cecha
         dotychczasowe[i]=wylosowana_cecha
     return cechy