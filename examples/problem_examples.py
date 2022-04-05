import random
from math import gcd

from problems import Problem, GradeLevel, Difficulty
from structures import QAdjointRoot


class Columns(Problem):
    def __init__(self, num_rows: int = 6, num_columns=8, column_width: str = "1.5cm", row_spacing: str = None,
                 difficulty: int = Difficulty.Simple, operator: str = "+", op_solver=lambda x, y: x + y,
                 custom_range=None):
        super().__init__(variables=[], grade_level=GradeLevel.Grade1, difficulty=difficulty)

        ranges = {
            Difficulty.Basic:
                (0, 5, 0, 4),
            Difficulty.Simple:
                (0, 9, 0, 9),
            Difficulty.Intermediate:
                (1, 1, 1, 1),
            Difficulty.Advanced:
                (1, 1, 1, 1),
            Difficulty.Expert:
                (1, 1, 1, 1)
        }

        self.a_min, self.a_max, self.b_min, self.b_max = ranges[difficulty]

        if custom_range is not None:
            self.a_min, self.a_max, self.b_min, self.b_max = custom_range

        self.dims = (num_rows, num_columns)
        self.col_width = column_width
        self.row_spacing = row_spacing
        self.operator = operator
        self.solver = op_solver

        self.problems = [
            (random.randrange(self.a_min, self.a_max), random.randrange(self.b_min, self.b_max))
            for _ in range(num_columns * num_rows)
        ]

    def latex_single_sum(self, x, y, indent_level: int = 0):
        soln = self.solver(x, y)

        lines = [
            r"\begin{align*}",
            rf"       &\; {x} \\",
            rf"   {self.operator} \;&\; {y} \\",
            r"   \rule{0.4cm}{1pt}&\rule{0.4cm}{1pt} \\",
            r"\end{align*}",
            (r"\vspace{" + self.row_spacing + "}\n") if self.row_spacing is not None else "",
        ]
        no_solution = "\n".join(map(lambda x: "    " * indent_level + x, lines))
        lines.insert(4, f"    & {soln}")
        solution = "\n".join(map(lambda x: "    " * indent_level + x, lines))

        return solution, no_solution

    def __str__(self, solved=False):
        unsolved_code = [
            r"\begin{figure}[ht!]",
            r"\centering"
        ]
        solved_code = unsolved_code[::]

        nr, nc = self.dims

        pi = 0

        for col in range(nc):

            u_column = [
                r"\begin{minipage}{" + self.col_width + "}"
            ]
            s_column = [
                r"\begin{minipage}{" + self.col_width + "}"
            ]
            for row in range(nr):
                a, b = self.problems[pi]
                pi += 1
                ss, su = self.latex_single_sum(a, b, indent_level=1)
                u_column.append(su)
                s_column.append(ss)
            u_column.append(r"\end{minipage}")
            s_column.append(r"\end{minipage}")

            unsolved_code.append("\n".join(u_column))
            solved_code.append("\n".join(s_column))

        unsolved_code.append(r"\end{figure}")
        solved_code.append(r"\end{figure}")

        u_code_joined = "\n".join(unsolved_code)
        s_code_joined = "\n".join(solved_code)

        if solved:
            return s_code_joined
        else:
            return u_code_joined


class Quadratics(Problem):
    def __init__(self, num_problems: int = 3, difficulty: int = Difficulty.Basic, grade_level: int = GradeLevel.Grade7,
                 factorable: bool = False, real_solns: bool = False, vert_space: str = "7cm"):
        super().__init__(variables=[], grade_level=grade_level, difficulty=difficulty)
        self.num_problems = num_problems
        self.factorable = factorable
        self.real_solns = real_solns
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
            coefs = [b*c, b + a*c, a]
            answers = [QAdjointRoot(-b, 0, a), QAdjointRoot(-c, 0, 1)]
        else:
            if self.real_solns:
                # if discriminant is < 0, then solutions are strictly complex.
                while b * b - 4*a*c < 0:
                    a = random.randint(1, 4)
                    b = random.randint(-10, 10)
                    c = random.randint(-10, 10)

            coefs = [c, b, a]
            answers = [
                QAdjointRoot(-b, b * b - 4 * a * c, 2 * a),
                QAdjointRoot(b, b * b - 4 * a * c, -2 * a)
            ]

        return coefs, answers

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

        for formatted in questions_formatted:
            question, answers = formatted

            written_question = f"Solve: ${question}$"

            code_lines.append(written_question)

            if solved:
                code_lines.append("\n".join([r"\begin{align*}", answers, r"\end{align*}"]))
            else:
                code_lines.append(r"\vspace{" + self.vert_space + "}")

        return "\n\n".join(code_lines)


if __name__ == '__main__':
    qa = Quadratics()

    print(qa)
