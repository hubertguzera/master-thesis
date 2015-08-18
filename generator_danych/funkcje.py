import random
import csv


def losuj_rozklad(prawdopodobienstwa):
    los = random.random()
    skumulowany = 0
    for key in prawdopodobienstwa:
        if los > skumulowany and los < skumulowany + prawdopodobienstwa[key]:
            return key
            break
        else:
            skumulowany += prawdopodobienstwa[key]
    return random.choice(prawdopodobienstwa.keys())
   

def losuj_zlozony_rozklad(prawdopodobienstwa,kryterium):
    rozklad = {}
    for key in prawdopodobienstwa:
        if key[:len(key)-1] == tuple(kryterium):
           rozklad[key[len(key)-1]] = float(prawdopodobienstwa[key])
    return losuj_rozklad(rozklad)
        
            
def czytajprostyrozkladzcsv(plik):
   ifile = open(plik + ".csv", "rb")
   reader = csv.reader(ifile)
   d= {}
   for row in reader:
      d[(row[0])] = float(row[1])
   return d

def czytajzlozonyrozkladcsv(plik, kryteria, szukana):
   ifile = open(plik + '.csv', "rb")
   reader = csv.reader(ifile)
   d= {}
   row_num = 0
   for row in reader:
       if row_num == 0:
           header = row
           
           for i in range(len(header)):
                 
               for kryterium in range(len(kryteria)):
                   if kryteria[kryterium] == header[i]:
                       kryteria[kryterium] = i
               if szukana == header[i]:
                   szukana = i
       else:
           wlasciwosci= []
           for i in range(len(kryteria)):
               wlasciwosci.append(row[kryteria[i]])
           d[tuple(wlasciwosci)] = row[szukana]

       row_num += 1
   return d

plec_rozklad = {"Kobieta":0.5,"Mezczyzna":0.5}
wiek_rozklad = czytajprostyrozkladzcsv("wiek")
wyksztalcenie_rozklad = czytajzlozonyrozkladcsv("wyksztalcenie",["Plec","Wyksztalcenie"],"p")
zarobki_rozklad = czytajzlozonyrozkladcsv("zarobki",["Wiek","Wyksztalcenie","Zarobki"],"p")
miasto_rozklad = czytajprostyrozkladzcsv("ludnosc")
zainteresowania_rozklad = czytajprostyrozkladzcsv("zainteresowania")
