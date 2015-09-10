import sympy
b = 13
x,y = sympy.symbols('x1 y2')

expr = x * x * x

print sympy.simplify(expr)

print expr.subs([(x,2),(y,5)])

print sympy.diff(expr,x)

print 2**2