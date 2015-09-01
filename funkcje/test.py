import sympy
b = 13
x,y = sympy.symbols('x1 y2')

expr = x * y ** 2 + 30

print expr.subs([(x,2),(y,4)])

print sympy.diff(expr,x)