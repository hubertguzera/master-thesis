import zalozenia, random, Image,pickle
from funkcje import funkcje_pomocnicze as f_p
from funkcje import funkcje_mapa as f_m
from funkcje import funkcje_losuj as f_l

class swiat(object):
    def __init__(self):
        #stworzenie pustej mapy
        self.nodes = {}
        self.mapa = [[lokalizacja(x,y, "Pusty") for x in range(zalozenia.wymiar_x)] for y in range(zalozenia.wymiar_y)]
        liczba_drog = int(zalozenia.wymiar_x*zalozenia.wymiar_y*zalozenia.udzial_drog)
        punkt = [int(zalozenia.wymiar_x/2),int(zalozenia.wymiar_y/2),"R",0] 
        lista_punktow= []
        print "Tworzenie drog"
        #populowanie mapy drogami
        for i in range(0,liczba_drog):
            print i, "/", liczba_drog
            punkt_jest_poprawny = True
            kontrola = 0
            while punkt_jest_poprawny:
                kontrola = kontrola + 1 
                nowy_punkt = f_m.nowy_punkt(punkt)
                if f_m.sprawdz_punkt(nowy_punkt,self,"Droga")[1]<2 and f_m.sprawdz_punkt(nowy_punkt,self,"Droga")[2]==True:
                    punkt_jest_poprawny = False
                if kontrola > 30:
                    punkt = random.choice(lista_punktow)
                    kontrola = 0
            lista_punktow.append(punkt)
            punkt = nowy_punkt
            self.mapa[punkt[0]][punkt[1]].typ = "Droga"
        print "Czekaj..."
        
        #stworzenie lokalizacji w komorkach sasiadujacych z drogami
        for x in range(zalozenia.wymiar_x):
            for y in range(zalozenia.wymiar_y):
                if self.mapa[x][y].typ == "Pusty":
                    if  f_m.sprawdz_punkt([x,y],self,"Droga")[0] >0:
                        self.mapa[x][y] = lokalizacja(x,y, "random")
                        self.mapa[x][y].droga = [tuple(f_m.wypisz_sasiadujace([x,y], self, "Droga")[random.randrange(len(f_m.wypisz_sasiadujace([x,y], self, "Droga")))])]

        print "Czekaj..."        
        #dla kazdej drogi wypisujemy sasiadujace nodes
        for x in range(zalozenia.wymiar_x):
            for y in range(zalozenia.wymiar_y):
                if self.mapa[x][y].typ=="Droga":
                    self.mapa[x][y].droga = f_m.wypisz_sasiadujace([x,y], self, "Droga",konwertuj=True)

        print "Czekaj..."            
        #tworzenie grafu z drog
        for x in range(zalozenia.wymiar_x):
            for y in range(zalozenia.wymiar_y):
                if self.mapa[x][y].droga:
                    self.nodes[x,y] = self.mapa[x][y].droga

        print "Czekaj..."
        #populowanie swiata                     
        self.ludnosc = [konsument(self) for x in range (zalozenia.populacja)]
        print "Prawie gotowe"
        for czlowiek in self.ludnosc:
            czlowiek.znajomi = [random.randrange(zalozenia.populacja) for x in range(3)]
        "Wypisuje sklepy"




class lokalizacja(swiat):
    def __init__(self,x,y, typ):
        self.x = x
        self.y = y
        self.droga = []
        if typ == "Pusty":
            self.typ = "Pusty"
        else:
            self.typ = f_l.losuj_rozklad(zalozenia.lokalizacja_rozklad_typ)

        
class konsument(object):
    def __init__(self, swiat):
        print "Tworze konsumenta"
        self.plec = f_l.losuj_rozklad(zalozenia.plec_rozklad)
        self.wiek = int(f_l.losuj_rozklad(zalozenia.wiek_rozklad))

        if self.wiek>18: self.wyksztalcenie = (f_l.losuj_zlozony_rozklad(zalozenia.wyksztalcenie_rozklad,[self.plec]))
        else: self.wyksztalcenie = "Brak"        

        self.zarobki = int((f_l.losuj_zlozony_rozklad(zalozenia.zarobki_rozklad,[str(self.wiek),self.wyksztalcenie])))
        self.zainteresowania = [f_l.losuj_rozklad(zalozenia.charaktery_rozklad) for x in range(3)]
        self.znajomi = []
        self.wyksztalcenie = f_p.konwertuj_wyksztalcenie(self.wyksztalcenie)
        self.okazja = 0

        #wybieranie domu
        while True: 
            self.domx = random.randrange(0,zalozenia.wymiar_x)
            self.domy = random.randrange(0,zalozenia.wymiar_y)
            if swiat.mapa[self.domx][self.domy].typ == "Dom":
                break
        #wybieranie pracy
        while True: 
            self.pracax = random.randrange(0,zalozenia.wymiar_x)
            self.pracay = random.randrange(0,zalozenia.wymiar_y)
            if swiat.mapa[self.pracax][self.pracay].typ == "Praca":
                break

        self.mozliwe_sklepy = []
            
    def macierz_cech(self):
            return f_p.wypisz_cechy_klienta(self.wiek,self.plec,self.wyksztalcenie,self.zarobki,self.zainteresowania)
    
    def odwiedzony_sklep(self, swiat):
        sklepy=[]
        if self.wiek > 17 and random.random()<zalozenia.szansa_na_zakupy:
            self.okazja = random.randrange(2)
            if self.okazja==0:
                start=(self.pracax,self.pracay)
                koniec=swiat.nodes[(self.domx,self.domy)][0]
            if self.okazja==1:
                start=(self.domx,self.domy)
                znajomy = swiat.ludnosc[random.choice(self.znajomi)]
                koniec=swiat.nodes[(znajomy.domx,znajomy.domy)][0]
            trasa = f_m.szukaj_drogi(swiat.nodes,start,koniec,nowy=True)
            for punkt in trasa:
                sklepy = sklepy + f_m.wypisz_sasiadujace(punkt,swiat,"Sklep")
            if sklepy : sklepy = random.choice(sklepy)
        return sklepy

    def wypisz_mozliwe_sklep(self, swiat):
        sklepy=[]
        if self.wiek > 17 and random.random()<zalozenia.szansa_na_zakupy:
            a = []
            start=(self.pracax,self.pracay)
            koniec=swiat.nodes[(self.domx,self.domy)][0]
            a.append([start,koniec])
            for i in range(3):
                start=(self.domx,self.domy)
                znajomy = swiat.ludnosc[self.znajomi[i]]
                koniec=swiat.nodes[(znajomy.domx,znajomy.domy)][0]
                a.append([start,koniec])
            trasa = []
            for element in a:
                trasa = trasa + f_m.szukaj_drogi(swiat.nodes,element[0],element[1],nowy=True)
            for punkt in trasa:
                sklepy = sklepy + f_m.wypisz_sasiadujace(punkt,swiat,"Sklep")
        return sklepy
        
def generowanie_swiata():
    wybor = raw_input("Wybierz 1 dla zapisu, 2 dla odczytu: ")
    if wybor =="1":
        print "Wybrano 1"
        moj_swiat = swiat()
        pickle.dump(moj_swiat,open("Swiat.p","wb"))

    if wybor =="2":
        print "Wybrano 2"
        moj_swiat = pickle.load(open("Swiat.p","rb"))
    f_m.rysujmape(moj_swiat,"mapy/typy")
    f_m.rysujludnosc(moj_swiat, moj_swiat.ludnosc,"mapy/ludnosc")

#generowanie_swiata()
