import random
from structures import Polynomial
from tex_code import Problem


# do derivatives and stuff.
class Differentiate(Problem):
    def __init__(self, polynomial_degree, coefficient_range=(-10, 10), m=1, variable='x'):
        super(Differentiate, self).__init__()
        self.polynomial_coefficients = [random.randint(*coefficient_range) for _ in range(polynomial_degree + 1)]
        while self.polynomial_coefficients[-1] <= 0:  # want positive first term for simplicities sake.
            self.polynomial_coefficients[-1] = random.randint(*coefficient_range)
        self.polynomial = Polynomial(self.polynomial_coefficients)
        self.derivative = self.polynomial.deriv(m=m)
        self.derivative_order = m
        self.variable = variable

    def derivative_symbol(self):
        order = str(self.derivative_order) if self.derivative_order > 1 else ""
        return r"\frac{\mathrm{d}^{" + order + r"}}{\mathrm{d}" + self.variable + "^{" + order + "}}"

    def __str__(self, solved=False):
        question_prompt = "Compute $" + self.derivative_symbol() + str(self.polynomial) + "$."

        solution = "\\[" + question_prompt[9:-2] + "=" + str(self.derivative) + "\\]"

        if solved:
            question_prompt = solution
        else:
            question_prompt += "\n\n\\vspace{5cm}"

        return question_prompt
