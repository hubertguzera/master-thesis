from sklearn.datasets import load_iris
from sklearn import tree
import joblib

iris = load_iris()

print iris.data, iris.target

clf = tree.DecisionTreeClassifier()
clf = clf.fit(iris.data, iris.target)

print clf.predict([ 5.1, 3.5, 1.4, 0.2])
