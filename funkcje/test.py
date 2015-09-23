import sympy

a,b = sympy.symbols("a b")
y = sympy.symbols("y")

expr = 2*a + 2*b

print expr.subs([(a,-2),(y,-2)])

print expr.subs([(a,2),(y,2)])>0

d = {"a":200 , "b":300}

print min(d.items(), key=lambda x: x[1])[0]