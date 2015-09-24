from funkcje import funkcje_zalozenia
import sympy
#Swiat

populacja = 2500
wymiar_x = 60
wymiar_y = 60
lokalizacja_rozklad_typ= {"Dom":0.6,"Praca":0.2,"Przestrzen komercyjna":0.2}
udzial_drog = 0.25
gestosc_zakretow = 0.05



# Tworzenie mapy
kolory_typow= {"Sklep":(255,151,51),"Magazyn":(255,255,55),"Fabryka":(153,255,255), "Pusty":(255,255,255),"Droga":(96,96,96),"Dom": (0,0,255),"Praca":(255,0,0),"Przestrzen komercyjna":(0,255,0)}
wymiar_obrazka = (1000,1000)



#Ludnosc
plec_rozklad = {"Kobieta":0.5,"Mezczyzna":0.5}
wiek_rozklad = funkcje_zalozenia.czytajprostyrozkladzcsv("dane/wiek")
wyksztalcenie_rozklad = funkcje_zalozenia.czytajzlozonyrozkladcsv("dane/wyksztalcenie",["Plec","Wyksztalcenie"],"p")
zarobki_rozklad = funkcje_zalozenia.czytajzlozonyrozkladcsv("dane/zarobki",["Wiek","Wyksztalcenie","Zarobki"],"p")
charaktery_rozklad = funkcje_zalozenia.czytajprostyrozkladzcsv("dane/zainteresowania")
szansa_na_zakupy = 1

#Firma
ilosc_fabryk = 2
ilosc_magazyn = 2
ilosc_sklepow = 4

koszt_fabryka = 1.3
koszt_magazyny = 1.2
koszt_sklepy = 1.1
koszt_sciezka = 0.005

skala_fabryka = 1
skala_magazyny = 1
skala_sklepy = 1
skala_sciezka = 1

produkt_cena = 7

#Konkurencja
prawdopodobienstwo_zakupu_piwa = 1
ilosc_produktow = 6
mozliwe_nazwy = ["Mocne","Baltyckie","Lebskie","Slaskie","Pszczeniczne","Pyszne","Gornik","Opolskie","Babskie"]
niedozwolone_nazwy = []

#modelowanie
udzial_treningowe = 0.3
zakres_prawdopodobienstwa_warunkowego = 5
znane_cechy = [0,1,2,3,4,29]
ilosc_iteracji_prognoz = 3
sposob = 1 # 1 dla LG, 2 dla K-N
sposob_wyboru_zmiennych = 1 #1 dla simple, 2 dla exhaustive

skok_dostawa = 3