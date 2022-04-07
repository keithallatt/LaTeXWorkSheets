import random
from functools import reduce
from math import gcd
from operator import mul
import numpy as np


FLOAT_TOLERANCE = 1e-15


def make_square_free(n):
    """ return $a, b$ such that $a^2 * b == n$ and b is square free. """
    if n == 0:
        return 0, 0
    if n == 1:
        return 1, 1

    pf = {}
    n_o = n

    d2 = 0
    while n % 2 == 0:
        d2 += 1
        n //= 2
    if d2:
        pf[2] = d2

    d = 3
    while True:
        dn = 0
        while n % d == 0:
            dn += 1
            n //= d
        if dn:
            pf[d] = dn

        d += 2
        if n == 1 or d > n:
            break

    assert reduce(mul, sum([[k for _ in range(v)] for k, v in pf.items()], []), 1) == n_o, f"Factorization failed {n_o}"

    pf_a = {k: v // 2 for k, v in pf.items()}
    pf_b = {k: v % 2 for k, v in pf.items()}

    a = reduce(mul, sum([[k for _ in range(v)] for k, v in pf_a.items()], []), 1)
    b = reduce(mul, sum([[k for _ in range(v)] for k, v in pf_b.items()], []), 1)

    assert a * a * b == n_o, f"SquareFree making failed ({a}^2 * {b} != {n_o}"

    return a, b


class QAdjointRoot:
    r""" Represents $x \in \mathbb{Q}[\sqrt(k)]$ for some $k$ """
    def __init__(self, n, r, d):
        r""" $\frac{n + \sqrt{r}}{d}$ """
        # make r square free.
        r_s, r_f = make_square_free(abs(r))
        if r < 0:
            r_f *= -1

        if r_f == 1:
            n += r_s
            r_s = 0
            r_f = 0

        # can be thought of as $\frac{n + r_s\sqrt{r_f}}{d}$

        g = gcd(n, gcd(r_s, d) if r_s else d)

        r_s //= g
        n //= g
        d //= g

        if d < 0:
            r_s *= -1
            n *= -1
            d *= -1

        self.n, self.r_s, self.r_f, self.d = n, r_s, r_f, d

    def __str__(self):
        """ Return a latex string representing this fraction. """
        numerator = ""

        if self.n:
            numerator += str(self.n)

            if self.r_s > 0:
                numerator += "+"

        if self.r_s:
            numerator += str(self.r_s)

            if abs(self.r_s) == 1:
                numerator = numerator[:-1]

            if self.r_f not in [0, 1]:
                numerator += r"\sqrt{" + str(self.r_f) + "}"

        fraction = numerator
        if (self.n or self.r_s) and self.d != 1:
            fraction = r"\frac{" + numerator + "}{" + str(self.d) + "}"

        if not (self.n or self.r_s or self.r_f):
            return "0"

        return fraction


class Polynomial(np.polynomial.Polynomial):
    def __str__(self, variable='x'):
        if not len(self.coef):
            return "0"
        if len(self.coef) == 1:
            c = self.coef[0]
            return str(int(c)) if abs(c-round(c)) < FLOAT_TOLERANCE else str(c)
        if not variable:
            raise ValueError("Variable must be defined")

        def term_of_deg_k(k):
            if k == 0:
                return ""
            if k == 1:
                return variable
            if len(str(k)) == 1:
                return variable + "^" + str(k)
            return variable + "^{" + str(k) + "}"

        terms = [term_of_deg_k(i) for i in range(len(self.coef))]

        # eliminate 0 terms
        term_coefficients = [(c, t) for c, t in zip(self.coef, terms) if abs(c) > FLOAT_TOLERANCE]

        # convert floats that are within 1e-15 of an integer to an integer (does not mutate internal values)
        term_coefficients = [
            (int(c) if abs(c - round(c)) < FLOAT_TOLERANCE else c, t) for c, t in term_coefficients
        ]

        # convert terms into strings
        term_coefficients = [
            (str(c) if not t else "" if c == 1 else "-" if c == -1 else str(c))+t for c, t in term_coefficients
        ]

        term_coefficients = [
            t if t.startswith("-") else "+"+t for t in term_coefficients
        ]
        term_coefficients[-1] = term_coefficients[-1].lstrip("+")
        return ''.join(term_coefficients[::-1])
