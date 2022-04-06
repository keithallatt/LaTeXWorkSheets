from tex_code import TexDocument, compile_tex
from templates.columns import Columns
from templates.quadratics import Quadratics
from templates.proof import ProofFromTeXFile


if __name__ == '__main__':
    td = TexDocument()
    c = Columns()
    # q = Quadratics()
    # psdb24 = ProofFromTeXFile('./latex_examples/prime_square_divisible_by_24.tex')

    td.add_content(c)
    # td.add_content(q)
    # td.add_content(psdb24)

    compile_tex('example.pdf', td, solutions=False, save_tex=True)
    compile_tex('example_solutions.pdf', td, solutions=True, save_tex=True)
