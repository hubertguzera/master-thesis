import random,zalozenia

def konwertuj_wyksztalcenie(wyksztalcenie):
   mozliwosci = {"Podstawowe":1,"Zawodowe":2,"Srednie":3,"Wyzsze":4,"Brak":0}
   return mozliwosci[wyksztalcenie]
      
def konwertuj_zainteresowania(zainteresowania):
   mozliwe = ["moda","gotowanie","finanse","kultura","historia","koncerty","motoryzacja","kosmetyki","malarstwo","ogrodnictwo","gry","sport","boks","fotografia","kulturaalternatywna","nightlife","teatr","ksiazka","historiapolski","natura","piwowarstwo","muzykaklasyczna","ksiazki"]
   macierz = [0 for x in range(23)]
   for item in zainteresowania:
      for i in range(len(mozliwe)):
         if item==mozliwe[i]:
            macierz[i]=1
   return macierz
         
def losuj_bez_powtorzen(losuj_z,sprawdz_z=[]):
   wybor = random.choice(losuj_z)
   while wybor in sprawdz_z:
      wybor = random.choice(losuj_z)
   return wybor

def dodaj_piksele(*tuples):
   return map(sum, zip(*tuples))
