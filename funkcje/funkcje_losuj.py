import random, zalozenia

def losuj_rozklad_niestandardowy(prawdopodobienstwa,max_p):
    los = max_p
    skumulowany = 0
    for key in prawdopodobienstwa:
        if los > skumulowany and los < skumulowany + prawdopodobienstwa[key]:
            return key
            break
        else:
            skumulowany += prawdopodobienstwa[key]
    return random.choice(prawdopodobienstwa.keys())

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

