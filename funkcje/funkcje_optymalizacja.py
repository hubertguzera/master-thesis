import sympy,math

def funkcja_do_optymalizacji(firma,stala_cena=True):
     expr = 0
     for trasa in firma.trasy.trasy:
            if stala_cena:
                expr = expr + trasa.symbol * trasa.elementy[2].symbol * firma.cena
            else:
                expr = expr + trasa.symbol * trasa.elementy[2].symbol * sympy.symbol("cena")

            for element in trasa.elementy:
                expr = expr - element.koszt * (trasa.symbol * trasa.elementy[2].symbol) ** element.efekt_skala
     return expr

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
    for sklep in firma.sklepy:
        a.append((sklep.symbol,sklep.oblozenie+1))
    return a

def punkty_stacjonarne(firma,prognozowana):
    return sympy.solve(pierwsze_pochodne(podstaw(funkcja_do_optymalizacji(firma),prognozowana),firma.trasy.trasy))

def dostawy_optymalne(firma,rynek):
    kombinacje = firma.trasy.trasy

    while kombinacje:
        a = {}
        for trasa in kombinacje:
            funkcja = podstaw(funkcja_do_optymalizacji(firma),dotychczasowa_sprzedaz(firma))

            if sympy.diff(funkcja,trasa.symbol).subs(trasa.symbol,1) > 0:
                a[trasa] = sympy.diff(funkcja,trasa.symbol).subs(trasa.symbol,1)
            else:
                kombinacje.remove(trasa)
        if a:
            max = a.keys()[0]
            for key in a:
                if a[max]<a[key]:
                    max = key

            trasa = max.elementy
            sklep = trasa[2]

            if sklep.oblozenie < sklep.przewidywana_sprzedaz:
                sklep.dostawa_towaru(rynek,trasa,symulowany_towar=1,inne_towary=0)
            else:
                kombinacje.remove(max)



