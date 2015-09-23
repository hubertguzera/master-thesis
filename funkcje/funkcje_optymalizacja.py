import sympy,math
import zalozenia

skok_dostawa = 1


def funkcja_do_optymalizacji(firma):
     expr = 0
     for sklep in firma.sklepy:
        expr = expr + (znajdz_oblozenie(firma,sklep)) * firma.cena
     for element in firma.magazyny+firma.sklepy+firma.fabryki+firma.trasy.drogi:
         expr = expr - element.koszt * (znajdz_oblozenie(firma,element)) ** element.efekt_skala
     return expr

def znajdz_oblozenie(firma,edge):
    oblozenie = 0
    for trasa in firma.trasy.trasy:
        for element in trasa.elementy:
            if element == edge:
                oblozenie = oblozenie + trasa.symbol
    return oblozenie

def podstaw(rownanie,liczby):
    return rownanie.subs(liczby)

def szukaj_symbolu(symbol,firma):
    for element in firma.sklepy + firma.magazyny + firma.fabryki + firma.trasy.trasy:
        if symbol == element.symbol:
            return element

def symbole_tras(trasy):
    a = []
    for trasa in trasy:
        a.append(trasa.symbol)
    return a

def pierwsze_pochodne(funkcja,trasy):
    a = []
    for trasa in trasy:

        a.append(sympy.diff(funkcja,trasa.symbol))

    return a

def prognozowana_sprzedaz(firma):
    a = []
    for sklep in firma.sklepy:
        a.append((sklep.symbol,sklep.przewidywana_sprzedaz))
    return a

def dotychczasowa_sprzedaz(firma):
    a = []
    for trasa in firma.trasy.trasy:
        a.append((trasa.symbol,trasa.oblozenie+1))
    return a

def punkty_stacjonarne(firma,prognozowana):
    return sympy.solve(pierwsze_pochodne(podstaw(funkcja_do_optymalizacji(firma),prognozowana),firma.trasy.trasy))

def dostawy_optymalne(firma,rynek):
    print "Startuje"
    kombinacje = []
    for element in firma.trasy.trasy:
        kombinacje.append(element)

    funkcja = funkcja_do_optymalizacji(firma)
    print funkcja
    b = {}
    for trasa in kombinacje:
        t = sympy.diff(funkcja,trasa.symbol)
        print "Gradint", trasa.symbol, t
        b[trasa] = t

    while kombinacje:
        a = {}
        for trasa in kombinacje:
            gradient = b[trasa]
            gradient = podstaw(gradient,dotychczasowa_sprzedaz(firma))
            a[trasa] = gradient.evalf()
            print trasa.symbol,a[trasa],trasa.elementy[2].oblozenie,"/", trasa.elementy[2].przewidywana_sprzedaz

        c={}
        for key in a:
            c[key] = a[key]
        for key in c:
            if c[key]<0:
                kombinacje.remove(key)
                del a[key]
                print "Usuniete bo niska pochodna"

        if a:
            max = a.keys()[0]
            for key in a:
                if a[max]<a[key]:
                    max = key
            trasa = max
            sklep = max.elementy[2]

            if sklep.oblozenie < sklep.przewidywana_sprzedaz:
                sklep.dostawa_towaru(rynek,trasa,symulowany_towar=skok_dostawa,inne_towary=0)
                print "Dostawa", trasa.symbol
            else:
                kombinacje.remove(max)
                print "Wyrzucam bo sklep", trasa.symbol



