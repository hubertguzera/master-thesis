

import pickle

lg = pickle.load(open("../lg.p","rb"))

print lg.sparsify()
