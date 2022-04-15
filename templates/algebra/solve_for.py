"""
Given $x = f(y)$, solve for $y$ in terms of $x$.
"""
import random
from tex_code import Problem, LaTeXPiece


class Variable(LaTeXPiece):
    def __init__(self, variable_name):
        super(LaTeXPiece, self).__init__()
        self.variable_name = variable_name

    def __str__(self, solved=False):
        return self.variable_name


class Constant(LaTeXPiece):
    def __init__(self, constant_value):
        super(LaTeXPiece, self).__init__()
        self.constant_value = constant_value

    def __str__(self, solved=False):
        return str(self.constant_value)


class LaTeXOperator(LaTeXPiece):
    def __init__(self, lhs: LaTeXPiece, rhs: LaTeXPiece):
        super(LaTeXPiece, self).__init__()
        self.lhs = lhs
        self.rhs = rhs

    def __str__(self, solved=False):
        pass


class Sum(LaTeXOperator):
    def __init__(self, lhs: LaTeXPiece, rhs: LaTeXPiece):
        super().__init__(lhs, rhs)

    def __str__(self, solved=False):
        return r"\left(" + str(self.lhs) + "+" + str(self.rhs) + r"\right)"


class Difference(LaTeXOperator):
    def __init__(self, lhs: LaTeXPiece, rhs: LaTeXPiece):
        super().__init__(lhs, rhs)

    def __str__(self, solved=False):
        return r"\left(" + str(self.lhs) + "-" + str(self.rhs) + r"\right)"


class Product(LaTeXOperator):
    def __init__(self, lhs: LaTeXPiece, rhs: LaTeXPiece):
        super().__init__(lhs, rhs)

    def __str__(self, solved=False):
        return str(self.lhs) + r" \times " + str(self.rhs)


class Quotient(LaTeXOperator):
    def __init__(self, lhs: LaTeXPiece, rhs: LaTeXPiece):
        super().__init__(lhs, rhs)

    def __str__(self, solved=False):
        return r"\frac{" + str(self.lhs) + "}{" + str(self.rhs) + "}"


OPPOSITE_OPERATORS = {
    Sum: Difference,
    Difference: Sum,
    Product: Quotient,
    Quotient: Product,
}


class TermRearrangement(Problem):
    """
    Given a function x = f(y), solve for y = g(x) by rearranging the terms. No simplification allowed.
    """
    def __init__(self, depth=3):
        super(Problem, self).__init__()

        ops = [
            Sum, Difference, Product, Quotient
        ]

        if int(random.random() * 2):
            ops = [
                Product, Quotient, Sum, Difference
            ]

        self.operations = [
            ops[2 * (i % 2) + int(random.random() * 2)] for i in range(depth)
        ]

        def _get_valid(operation: LaTeXOperator, min_val=1, max_val=10) -> int:
            assert min_val >= 1 and max_val >= 1, "Values must be strictly positive."

            value = random.randint(min_val, max_val)

            # prevents mul / div by 1.
            if operation in [Product, Quotient]:
                while value == 1:
                    value = random.randint(min_val, max_val)

            return value

        self.right_hand_sides = [
            Constant(_get_valid(self.operations[i])) for i in range(depth)
        ]

        self.opposites = list(map(lambda x: OPPOSITE_OPERATORS[x], self.operations))

        self.x_var = Variable("x")
        self.y_var = Variable("y")

        expression = self.y_var
        opp_expres = self.x_var

        for i in range(depth):
            expression = self.operations[i](expression, self.right_hand_sides[i])
        for i in range(depth-1, -1, -1):
            opp_expres = self.opposites[i](opp_expres, self.right_hand_sides[i])

        self.question_expression = str(self.x_var) + "=" + str(expression)
        self.solution = str(self.y_var) + "=" + str(opp_expres)

    def __str__(self, solved=False):
        question = ["Rearrange terms to solve for $y$. Do not simplify.", f"$${self.question_expression}$$"]

        if solved:
            question = [f"$${self.solution}$$"]
        else:
            question.append(r"\vspace{5cm}")

        return "\n".join(question)

