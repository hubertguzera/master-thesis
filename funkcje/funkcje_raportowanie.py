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

def zapis_produkty(plik,rynek):
    czysc_plik(plik)
    print rynek.produkty_na_rynku
    dodaj_do_pliku(plik,["Cena","Smak","Opakowanie","Premium","Budzetowe","Lager","Smakowe","Marketing"])
    for produkt in rynek.produkty_na_rynku:
        dodaj_do_pliku(plik,produkt)

def zapis_prognoza(plik,rynek,czysc=False):
    if czysc:
        czysc_plik(plik)
        dodaj_do_pliku(plik,["Tura","Symbol","Przewidywane","Sprzedaz"])
    else:
        for sklep in rynek.symulowana_firma.sklepy:
            if "Symulowane" in sklep.sprzedaz:
                rekord = [rynek.tura,sklep.symbol,int(sklep.przewidywana_sprzedaz),sklep.sprzedaz["Symulowane"]]
            else:
                rekord = [rynek.tura,sklep.symbol,sklep.przewidywana_sprzedaz,0]
            print rekord
            dodaj_do_pliku(plik,rekord)

def zapis_koszty(plik,rynek,czysc=False):
    firma = rynek.symulowana_firma
    if czysc:
        czysc_plik(plik)
        dodaj_do_pliku(plik,["Tura","Symbol","Koszt","Efekt skali","Oblozenie","Koszt w turze"])
    else:
        for element in firma.fabryki + firma.sklepy + firma.magazyny:
            rekord = [rynek.tura,element.symbol,element.koszt,element.efekt_skala,element.oblozenie,element.koszt*element.oblozenie**element.efekt_skala]
            print rekord
            dodaj_do_pliku(plik,rekord)

def zapis_przychody(plik,rynek,czysc=False):
    firma = rynek.symulowana_firma
    if czysc:
        czysc_plik(plik)
        dodaj_do_pliku(plik,["Tura","Symbol","Cena","Oblozenie","Przychod"])
    else:
        for element in firma.sklepy:
            print element.sprzedaz
            if "Symulowane" in element.sprzedaz:
                rekord = [rynek.tura,element.symbol,firma.cena,element.sprzedaz["Symulowane"],firma.cena*element.sprzedaz["Symulowane"]]
            else:
                rekord = [rynek.tura,element.symbol,firma.cena,0,0]
            print rekord
            dodaj_do_pliku(plik,rekord)

def zapis_przewidywania(plik,wartosc,czysc=False):
    if czysc:
        czysc_plik(plik)
        dodaj_do_pliku(plik,["Prawdziwy","LM","K-Mean"])
    else:
        dodaj_do_pliku(plik,wartosc)