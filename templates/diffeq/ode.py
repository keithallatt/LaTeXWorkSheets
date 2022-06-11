"""
Ordinary Differential Equations.
"""

from tex_code import Problem
from numpy.polynomial import polynomial as poly
from structures import Polynomial


def y_prime(degree, variable='y'):
    assert degree >= 0, "negative derivative not allowed in ODE's"

    if degree <= 3:
        return variable + "'" * degree

    return "".join([variable, "^{(", str(degree), ")}"])


class ConstantCoefficientHomogeneousODE(Problem):
    def __init__(self, r_values: tuple, dependent_variable: str = 'y', independent_variable: str = 'x'):
        """
        Construct an ODE problem such as $y'' - 2y' + y = 0$, where
        the R.H.S is 0 and all coefficients are constants.

        :param r_values:
        :param dependent_variable:
        :param independent_variable:
        """
        super(ConstantCoefficientHomogeneousODE, self).__init__()
        self.r_values = r_values
        self.dependent = dependent_variable
        self.independent = independent_variable

        self.characteristic_polynomial = Polynomial(poly.polyfromroots(r_values))
        self.char_poly_str = self.characteristic_polynomial.__str__(variable='r')
        self.diff_eq = self.format_diff_eq()

    def format_diff_eq(self):
        diff_eq = []
        for i, coefficient in enumerate(self.characteristic_polynomial):
            derivative = y_prime(i, variable=self.dependent)
            rounded_coefficient = round(coefficient)
            if abs(coefficient - rounded_coefficient) < 1e-15:
                coefficient = rounded_coefficient
            if coefficient == 0:
                continue

            if abs(coefficient) == 1:
                coefficient_str = str(coefficient)[:-1]
            else:
                coefficient_str = str(coefficient)

            if not coefficient_str or coefficient_str[0] != '-':
                coefficient_str = "+" + coefficient_str

            diff_eq.append(coefficient_str + derivative)

        diff_eq_str = ''.join(diff_eq[::-1]).lstrip("+")
        return diff_eq_str

    def __str__(self, solved=False):
        problem_text = f"Solve ${self.diff_eq} = 0$."

        print(problem_text)


if __name__ == '__main__':
    sode = ConstantCoefficientHomogeneousODE(r_values=(1, 2, 3))
    print(sode.__str__())
