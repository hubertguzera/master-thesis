import random
import Image
import zalozenia
import csv
import operator
import funkcje_pomocnicze as f_p


#funkcje przy podaniu slownika z badaniami sondazowymi losuje wartosc zgodna z rozkladem


#funkcja rysuje mape swiata - drog i lokalizacji wedlug typow
def rysujmape(swiat, nazwa):
    img = Image.new('RGB', (zalozenia.wymiar_x,zalozenia.wymiar_y), "white")
    pixels = img.load()
    
    for x in range(zalozenia.wymiar_x):
        for y in range(zalozenia.wymiar_y):
            pixels[x,y] = zalozenia.kolory_typow[swiat.mapa[x][y].typ]
            
    for k in range(zalozenia.wymiar_x):
       if k % 2 == 0 : pixels[k,0] = (0,0,0)
    for k in range(zalozenia.wymiar_y):
       if k % 2 == 0 : pixels[0,k] = (0,0,0)
       
    obraz = img.resize(zalozenia.wymiar_obrazka)
    obraz.save(nazwa + ".png")

#funkcja rysuje mape swiata - gradient populacji przypisany do danej komorki
def rysujludnosc(swiat,ludnosc, nazwa):
    img = Image.new('RGB', (zalozenia.wymiar_x,zalozenia.wymiar_y), "white")
    pixels = img.load()
    for konsument in ludnosc:
        pixels[konsument.domx,konsument.domy] = tuple(map(operator.add, pixels[konsument.domx,konsument.domy], (-10,-10,-10)))
    obraz = img.resize(zalozenia.wymiar_obrazka)
    obraz.save(nazwa + ".png")

#funkcja sprawdza ile punktow danego typu sasiaduje z dana komorka
def sprawdz_punkt(punkt,swiat,szukaj):
    suma = 0
    sasiedztwo=["",""]
    granica = False
    x = punkt[0]
    y = punkt[1]
    przylegle = []
    przekatne = []
    suma_przylegle = 0
    suma_przekatne = 0 
    maxx = zalozenia.wymiar_x
    maxy = zalozenia.wymiar_y

    if x>1 and x<maxx-2 and y>1 and y<maxy-2:
       granica = True
       przylegle = [swiat.mapa[x-1][y].typ,swiat.mapa[x+1][y].typ,swiat.mapa[x][y+1].typ,swiat.mapa[x][y-1].typ]
       przekatne = [swiat.mapa[x-1][y-1].typ,swiat.mapa[x+1][y+1].typ,swiat.mapa[x-1][y+1].typ,swiat.mapa[x+1][y-1].typ]
       for wspolrzedna in przylegle:
          if wspolrzedna == szukaj:
             suma_przylegle = suma_przylegle +1
             
       for wspolrzedna in przekatne:
          if wspolrzedna == szukaj:
             suma_przekatne = suma_przekatne +1         

    return [suma_przylegle,suma_przekatne, granica]

#funkcja losuje nowy sasiadujacy punkt zgodnie z ustawieniami mapy
def nowy_punkt(punkt):
   kierunek = punkt[2]
   czas = punkt [3]
   los = random.random()
   if los<zalozenia.gestosc_zakretow * czas:
      if kierunek =="U" or kierunek =="D":
         kierunek = random.choice(["R","L"])
         czas = 0
      else:
         kierunek = random.choice(["U","D"])
         czas = 0
   czas = czas + 1
   
   if kierunek == "U":
      return [punkt[0],punkt[1]+1,"U",czas]
   if kierunek == "D":
      return [punkt[0],punkt[1]-1,"D",czas]
   if kierunek == "L":
      return [punkt[0]+1,punkt[1],"L",czas]
   if kierunek == "R":     
      return [punkt[0]-1,punkt[1],"R",czas]

#funkcja wypisuje sasiadujace komorki danego typu (potrafi pominac jedna z nich, np. przy szukaniu drogi)
def wypisz_sasiadujace(punkt, swiat, szukana, pomin = "", konwertuj = False):
   sasiadujace = []
   x = punkt[0]
   y = punkt[1]

   if x!=zalozenia.wymiar_x-1:
      if swiat.mapa[x+1][y].typ == szukana:
         sasiadujace.append([x+1,y])

   if x!=0:
      if swiat.mapa[x-1][y].typ == szukana:
         sasiadujace.append([x-1,y])
         
   if y!=zalozenia.wymiar_y-1:
      if swiat.mapa[x][y+1].typ == szukana:
         sasiadujace.append([x,y+1])
   
   if y!=0:
      if swiat.mapa[x][y-1].typ == szukana:
         sasiadujace.append([x,y-1])

   if pomin != "" and (pomin in sasiadujace):
      sasiadujace.remove(pomin)
   if konwertuj:
      for item in sasiadujace:
         item=tuple(item)
   return sasiadujace
   
def szukaj_drogi(nodes,poczatek,koniec,sciezka=[],nowy=False):
   if nowy:
      sciezka = []
   sciezka.append(list(poczatek))

   if poczatek == koniec:
      return sciezka
   if not nodes.has_key(poczatek):
      return None
   for node in nodes[poczatek]:
      node = tuple(node)
      if list(node) not in sciezka:
         nowa_sciezka = szukaj_drogi(nodes,node,koniec,sciezka)
         if nowa_sciezka: return nowa_sciezka
   return None

