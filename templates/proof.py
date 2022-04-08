"""
Proof questions. Such as "Prove the closure of the integers mod 5 under addition".
"""
from tex_code import Problem

TEX_THEOREM_DELIMITER_START = r"% TEX THEOREM START %"
TEX_THEOREM_DELIMITER_END = r"% TEX THEOREM END %"

TEX_PROOF_DELIMITER_START = r"% TEX PROOF START %"
TEX_PROOF_DELIMITER_END = r"% TEX PROOF END %"


class ProofProblem(Problem):
    def __init__(self, theorem_statement, proof, vspace="8cm", qed_symbol=r"$\blacksquare$"):
        super(ProofProblem, self).__init__()
        self.prerequisite_packages = list(filter(lambda _: _, map(str.strip, r"""
        \usepackage{amsmath}
        \usepackage{amssymb}
        \usepackage{amsthm}
        \newtheorem{theorem}{Theorem}[section]
        \renewcommand\qedsymbol{QED_SYMBOL}
        """.replace("QED_SYMBOL", qed_symbol).split("\n"))))

        self.theorem_statement = theorem_statement
        self.proof = proof
        self.vspace = vspace

    def __str__(self, solved=False):
        prove_the_following = "Prove the following theorem."
        theorem_start = r"\begin{theorem}"
        theorem_end = r"\end{theorem}"
        proof_start = r"\begin{proof}"
        proof_end = r"\end{proof}"

        code_lines = [
            theorem_start,
            self.theorem_statement,
            theorem_end
        ]

        if solved:
            code_lines += [
                proof_start,
                self.proof,
                proof_end
            ]
        else:
            code_lines.insert(0, prove_the_following)
            code_lines.append(r"\vspace{"+self.vspace+"}")

        return "\n".join(code_lines)


class ProofFromTeXFile(ProofProblem):
    def __init__(self, tex_filepath):
        with open(tex_filepath, 'r') as f:
            tex_contents = f.read()

        theorem_start = tex_contents.index(TEX_THEOREM_DELIMITER_START) + len(TEX_THEOREM_DELIMITER_START)
        theorem_end = tex_contents.index(TEX_THEOREM_DELIMITER_END)
        proof_start = tex_contents.index(TEX_PROOF_DELIMITER_START) + len(TEX_PROOF_DELIMITER_START)
        proof_end = tex_contents.index(TEX_PROOF_DELIMITER_END)

        theorem = tex_contents[theorem_start: theorem_end]
        proof = tex_contents[proof_start: proof_end]

        super(ProofFromTeXFile, self).__init__(theorem, proof, qed_symbol="Q.E.D.")
