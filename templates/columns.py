import random
from math import gcd

from problems import Problem, GradeLevel, Difficulty
from structures import QAdjointRoot


class Columns(Problem):
    def __init__(self, num_rows: int = 6, num_columns=8, column_width: str = "1.5cm", row_spacing: str = None,
                 difficulty: int = Difficulty.Simple, operator: str = "+", op_solver=lambda x, y: x + y,
                 custom_range=None):
        super().__init__(grade_level=GradeLevel.Grade1, difficulty=difficulty)

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
        code_lines = [
            r"\begin{figure}[ht!]",
            r"\centering"
        ]

        if self._on_new_page:
            code_lines.insert(0, r"\newpage")

        nr, nc = self.dims
        pi = 0

        for col in range(nc):
            column = [r"\begin{minipage}{" + self.col_width + "}"]
            for row in range(nr):
                a, b = self.problems[pi]
                pi += 1
                ss, su = self.latex_single_sum(a, b, indent_level=1)
                if solved:
                    column.append(ss)
                else:
                    column.append(su)

            column.append(r"\end{minipage}")
            code_lines.append("\n".join(column))

        code_lines.append(r"\end{figure}")

        return "\n".join(code_lines)
