import random
from math import gcd

from tex_code import Problem, GradeLevel, Difficulty
from structures import QAdjointRoot


class Quadratics(Problem):
    def __init__(self, num_problems: int = 3, difficulty: int = Difficulty.Basic, grade_level: int = GradeLevel.Grade7,
                 factorable: bool = False, real_solutions: bool = False, vert_space: str = "7cm"):
        super().__init__(grade_level=grade_level, difficulty=difficulty)
        self.num_problems = num_problems
        self.factorable = factorable
        self.real_solutions = real_solutions
        self.vert_space = vert_space
        self.quad_problems = []

        for _ in range(self.num_problems):
            self.quad_problems.append(self.generate_quad_problem())

    def generate_quad_problem(self):
        a = random.randint(1, 4)
        b = random.randint(-10, 10)
        c = random.randint(-10, 10)
        if self.factorable:
            # generate (ax + b) and (x + c) to generate
            # (ax+b)(x+c) = (ax^2 + (b+ac)x + bc
            coefficients = [b*c, b + a*c, a]
            answers = [QAdjointRoot(-b, 0, a), QAdjointRoot(-c, 0, 1)]
        else:
            if self.real_solutions:
                # if discriminant is < 0, then solutions are strictly complex.
                while b * b - 4*a*c < 0:
                    a = random.randint(1, 4)
                    b = random.randint(-10, 10)
                    c = random.randint(-10, 10)

            coefficients = [c, b, a]
            answers = [
                QAdjointRoot(-b, b * b - 4 * a * c, 2 * a),
                QAdjointRoot(b, b * b - 4 * a * c, -2 * a)
            ]

        return coefficients, answers

    @staticmethod
    def format_quadratic(coefficients, answers, variable: str = 'x'):
        c, b, a = coefficients

        if a < 0:
            a *= -1
            b *= -1
            c *= -1

        g = gcd(a, gcd(b, c))
        a //= g
        b //= g
        c //= g

        a_term = (str(a) if a != 1 else "") + variable + "^2"
        b_term = (("-" if b == -1 else str(b) if b != 1 else "") + "x") if b else ""
        c_term = str(c) if c else ""

        if b_term and b_term[0] != "-":
            a_term += "+"

        if c_term and c_term[0] != "-":
            b_term += "+"

        quadratic = "".join([a_term, b_term, c_term]) + " = 0"

        answer_strs = list(map(str, answers))

        answer_str = variable + "=" + ", ".join(answer_strs)

        return quadratic, answer_str

    def __str__(self, solved=False):

        questions_formatted = [self.format_quadratic(*q) for q in self.quad_problems]

        code_lines = []
        if self._on_new_page:
            code_lines.append(r"\new""page")

        for formatted in questions_formatted:
            question, answers = formatted

            written_question = f"Solve: ${question}$"

            code_lines.append(written_question)

            if solved:
                code_lines.append("\n".join([r"\begin{align*}", answers, r"\end{align*}"]))
            else:
                code_lines.append(r"\vspace{" + self.vert_space + "}")

        return "\n\n".join(code_lines)
