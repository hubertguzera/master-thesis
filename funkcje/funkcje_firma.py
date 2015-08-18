import random
import funkcje_losuj as f_l
import zalozenia

def wybierz_lokalizacje(swiat,typ,nowy_typ):
    istnieje_przestrzen_komercyjna = False
    for x in range(zalozenia.wymiar_x):
        for y in range(zalozenia.wymiar_y):
            if swiat.mapa[x][y].typ == "Przestrzen komercyjna":
                istnieje_przestrzen_komercyna = True
                break
    if istnieje_przestrzen_komercyjna == False:
        typ = "Dom"
    while True:
        x = random.randrange(0,zalozenia.wymiar_x)
        y = random.randrange(0,zalozenia.wymiar_y)
        if swiat.mapa[x][y].typ == typ:
            break
    swiat.mapa[x][y].typ = nowy_typ
    return [x,y]


def prawdopodobienstwo_zakupu_piwa(tablica_y):
    wybrany = ["",-1]
    if zalozenia.prawdopodobienstwo_zakupu_piwa == 0:
       for produkt in tablica_y:
           if produkt[1]>wybrany[1]:
               wybrany = produkt
       return wybrany
    if zalozenia.prawdopodobienstwo_zakupu_piwa == 1:
        tablica = {}
        max_p = float(0)
        for produkt in tablica_y:
            tablica[produkt[0]]=produkt[1]
            max_p += produkt[1]
        return f_l.losuj_rozklad_niestandardowy(tablica,max_p)
        

def zlicz_sprzedaz(sklepy,towar):
    suma = 0
    for sklep in sklepy:
        if towar in sklep.sprzedaz:
            suma += sklep.sprzedaz[towar]
    return suma
