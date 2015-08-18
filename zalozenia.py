import funkcje_zalozenia
#Swiat

populacja = 350
wymiar_x = 25
wymiar_y = 25
lokalizacja_rozklad_typ= {"Dom":0.6,"Praca":0.2,"Przestrzen komercyjna":0.2}
udzial_drog = 0.3
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
ilosc_magazyn = 3
ilosc_sklepow = 7

#Konkurencja
prawdopodobienstwo_zakupu_piwa = 1
ilosc_produktow = 6
mozliwe_nazwy = ["Mocne","Baltyckie","Lebskie","Slaskie","Pszczeniczne","Pyszne","Gornik","Opolskie","Babskie"]
niedozwolone_nazwy = []
