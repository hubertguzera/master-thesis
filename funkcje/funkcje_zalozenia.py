import csv

def czytajprostyrozkladzcsv(plik):
   ifile = open(plik + ".csv", "rb")
   reader = csv.reader(ifile)
   d= {}
   for row in reader:
      d[(row[0])] = float(row[1])
   return d

#funkcja tworzy tablice z rozkladami procentowymi na podstawie pliku cvs, gdy mamy koniunkcje warunkow
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
