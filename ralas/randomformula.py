from first_order.formulas import variables, eq, RelSym, true, false
import random

arity = 3
r=("R",2)

r=RelSym(*r)
vs = variables(*range(arity))

result = []
for i in range(random.randint(1,5)):
    oendo = []
    for j in range(random.randint(1,5)):
        tup = tuple(random.choice(vs) for _ in range(r.arity))
        if random.randint(0,1):
            oendo.append(r(*tup))
        else:
            oendo.append(-r(*tup))
    result.append(oendo.pop())
    while oendo:
        result[-1]=result[-1]&oendo.pop()

formula=result.pop()
while result:
    formula=formula|result.pop()

print(formula)


