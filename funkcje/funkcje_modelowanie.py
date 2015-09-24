import itertools,random
import zalozenia
import numpy as np
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_raportowanie as f_r
from sklearn.metrics.pairwise import euclidean_distances
from sklearn import linear_model
from sklearn.neighbors import KNeighborsClassifier
import pickle

import numpy as np

class training(object):
    def __init__(self,sklepy):
        self.kolejnosc = []
        for subset in itertools.permutations([i for i in range(zalozenia.zakres_prawdopodobienstwa_warunkowego)]):
            self.kolejnosc.append(list(subset))
        self.historia = lacz_historie(historia_wszystkich(sklepy))
        self.training = self.historia[:int(len(self.historia)*zalozenia.udzial_treningowe)]

        a = {}

        if zalozenia.sposob_wyboru_zmiennych == 2:
            for kombinacja in self.kolejnosc:
                print self.kolejnosc.index(kombinacja),"/",len(self.kolejnosc)
                training_y = []
                for i in range(len(self.training)):
                    training_y.append(stworz_konsumenta(self.training,kombinacja))

                a[tuple(kombinacja)]= np.mean(euclidean_distances(f_p.usun_kolumny(self.training,[x for x in range(zalozenia.zakres_prawdopodobienstwa_warunkowego)]), training_y))

            self.kolejnosc = a.keys()[0]
        else:
            self.kolejnosc = self.kolejnosc[0]
        for key in a:
            if a[key]<a[self.kolejnosc]:
                self.kolejnosc = key

        self.historia= f_p.usun_kolumny(lacz_historie(historia_wszystkich(sklepy)),zalozenia.znane_cechy)
        self.historia_y = []
        self.historia_x = []

        for item in self.historia:
            if item[len(item)-1] == "Symulowane":
                self.historia_y.append(1)
            else:
                self.historia_y.append(0)
            self.historia_x.append(item[:(len(item)-1)])

        self.lg = linear_model.LogisticRegression()


        self.lg.fit(self.historia_x,self.historia_y)
        a= []

        for i in range(10):
            self.km = KNeighborsClassifier(n_neighbors=i+1)
            self.km.fit(self.historia_x,self.historia_y)
            a.append(self.km.score(self.historia_x,self.historia_y))

        self.km = KNeighborsClassifier(n_neighbors=a.index(max(a))+1)
        self.km.fit(self.historia_x,self.historia_y)

        f_r.zapis_przewidywania("rezultaty/przewidywania.csv",0,czysc=True)
        i = 0
        for element in self.historia_x:
            f_r.zapis_przewidywania("rezultaty/przewidywania.csv",[self.historia_y[i],self.lg.predict(element)[0],self.km.predict(element)[0]])
            i+=1

        pickle.dump(self.lg,open("lg.p","wb"))
        pickle.dump(self.km,open("km.p","wb"))








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

def stworz_konsumenta(historia_sklepu,kolejnosc):
     cechy = [[] for i in range(len(kolejnosc))]
     dotychczasowe = {}
     for i in kolejnosc:
         wylosowana_cecha = losuj_niestandardowy(licz_prawdopodobienstwo_cech(historia_sklepu,i,dotychczasowe))
         cechy[i] = wylosowana_cecha
         dotychczasowe[i]=wylosowana_cecha
     return cechy

def stworz_grupe(historia_sklepu,training):
    ilosc = ilosc_odwiedzajacych(historia_sklepu)
    grupa = []
    for i in range(ilosc):
        grupa.append(stworz_konsumenta(lacz_historie(historia_sklepu),training.kolejnosc))
    return grupa

def prognozuj_sprzedaz(historia_sklepu,training,rynek):
    if zalozenia.sposob == 1:
        model = training.lg
    else:
        model = training.km

    prognoza = [0 for x in range(zalozenia.ilosc_iteracji_prognoz)]

    for i in range(zalozenia.ilosc_iteracji_prognoz):
        for item in model.predict_proba(stworz_grupe(historia_sklepu,training)):
            prognoza[i] += f_p.losuj_proba(item)
        f_r.zapis_pojedynczej_prognozy("rezultaty/czesci_prognoz.csv",prognoza[i],rynek,czysc=True)
    return np.mean(prognoza)
