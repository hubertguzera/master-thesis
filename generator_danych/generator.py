import csv
import sys
import funkcje
import random

f = open('daneoklientach.csv', 'wt')


try:
    writer = csv.writer(f)
    writer.writerow(('wiek', 'plec', 'wyksztallcenie', 'miasto', 'zarobki', 'zainteresowania1', 'zainteresowania2', 'zainteresowania3'))
    for i in range(250000):
        plec = funkcje.losuj_rozklad(funkcje.plec_rozklad)
        wiek = int(funkcje.losuj_rozklad(funkcje.wiek_rozklad))
        if wiek>18:
            wyksztalcenie = wyksztalcenie = (funkcje.losuj_zlozony_rozklad(funkcje.wyksztalcenie_rozklad,[plec]))
        else:
            wyksztalcenie = "Brak"
        miasto = funkcje.losuj_rozklad(funkcje.miasto_rozklad)
        zarobki = random.randrange(8,12)/10*(funkcje.losuj_zlozony_rozklad(funkcje.zarobki_rozklad,[str(wiek),wyksztalcenie]))
        zainteresowania1 = funkcje.losuj_rozklad(funkcje.zainteresowania_rozklad)
        zainteresowania2 = funkcje.losuj_rozklad(funkcje.zainteresowania_rozklad)
        zainteresowania3 = funkcje.losuj_rozklad(funkcje.zainteresowania_rozklad)

        if wyksztalcenie == "Wyzsze" and random.random()>0.4:
            los = random.random()
            if los<0.25:
                zainteresowania1 = "Kultura wyzsza"
            if los>0.25 and los<0.5:
                zainteresowania2 = "Teatr"
            if los>0.5 and los<0.75:
                zainteresowania2 = "Malarstwo"
            if los>0.75:
                zainteresowania2 = "Muzyka klasyczna"
        if zarobki >3000 and random.random()>0.6:
            zainteresowania2 = "Kultura alternatywna"
        
        writer.writerow((wiek,plec,wyksztalcenie,miasto, zarobki, zainteresowania1,zainteresowania2,zainteresowania3))

        
finally:
    f.close()

print open('daneoklientach.csv','rt').read()

