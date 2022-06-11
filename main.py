from tex_code import TexDocument, compile_tex
from templates.algebra.quadratics import Quadratics
from templates.proofs.proof import ProofFromTeXFile
from templates.calculus.derivatives import Differentiate
from templates.algebra.solve_for import TermRearrangement


if __name__ == '__main__':
    td = TexDocument()

    q = Quadratics()
    psdb24 = ProofFromTeXFile('./latex_examples/prime_square_divisible_by_24.tex')
    d = Differentiate(6)
    tr = TermRearrangement(depth=5)

    td.add_content(q)
    td.add_content(psdb24)
    td.add_content(d)
    td.add_content(tr)

    compile_tex('example.pdf', td, solutions=False, save_tex=True)
    compile_tex('example_solutions.pdf', td, solutions=True, save_tex=True)
