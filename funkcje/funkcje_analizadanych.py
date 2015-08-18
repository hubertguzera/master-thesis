import csv
from sklearn import tree
from sklearn.externals.six import StringIO
import pydot

def czytajdaneklientow(plik, drukuj=False, pomin=[], kolumna_y = -1,usun_naglowek=True):
    tablica_x = list(csv.reader(open(plik + '.csv', "rb")))   
    for i in range(len(pomin)):
        for row in tablica_x:
            del row[pomin[i]-i]
    if kolumna_y == -1:
        kolumna_y = len(tablica_x[1])-1
    if usun_naglowek:
        del tablica_x[0]
    tablica_y = [tablica_x[x][kolumna_y] for x in range(len(tablica_x))]
    for row in tablica_x:
        del row[kolumna_y]    
    clf = tree.DecisionTreeClassifier(max_depth=5)
    clf = clf.fit(tablica_x, tablica_y)
    if drukuj:
        dot_data = StringIO()
        tree.export_graphviz(clf, out_file=dot_data) 
        graph = pydot.graph_from_dot_data(dot_data.getvalue()) 
        graph.write_pdf("graf.pdf")
    return clf


def bayes(plik, uwzglednij,usun_naglowek=True):
    tablica_x = list(csv.reader(open(plik + '.csv', "rb")))
    tablica_p = []
    if usun_naglowek:
        del tablica_x[0]
    for i in range(len(tablica_x[0])):
        wszystkich = float(0)
        takich_samych = float(0)
        if i in uwzglednij.keys():
            for row in tablica_x:
                wszystkich += 1
                if uwzglednij[i] == row[i]:
                       takich_samych += 1
            p = float(takich_samych / wszystkich)
            tablica_p.append(p)
    print tablica_p
    p = 1
    for element in tablica_p:
        p = p * element
    return p
    


# print  bayes("dane/cechy",{2:"Kobieta",5:'1'}) + bayes("dane/cechy",{2:"Kobieta",5:'0'}) 
