from itertools import product
from random import sample

arity = 3
card = 5
density = 0.1
for t in sample(list(product(range(card),repeat=arity)),int(card**arity*density)):
    print(t)
