import csv

def czysc_plik(plik):
    f = open(plik, "w")
    f.truncate()
    f.close()

def dodaj_do_pliku(plik,wpis):
    f = open(plik, "ab")
    writer = csv.writer(f)
    writer.writerow(wpis)
    f.close()

def zapis_ludnosc(plik,swiat):
    czysc_plik(plik)
    dodaj_do_pliku(plik,["wiek","kobieta","mezczyzna","wyksztalcenie","zarobki","okazja","moda","gotowanie","finanse","kultura","historia","koncerty","motoryzacja","kosmetyki","malarstwo","ogrodnictwo","gry","sport","boks","fotografia","kulturaalternatywna","nightlife","teatr","ksiazka","historiapolski","natura","piwowarstwo","muzykaklasyczna","ksiazki"])
    for czlowiek in swiat.ludnosc:
        dodaj_do_pliku(plik,czlowiek.macierz_cech())


