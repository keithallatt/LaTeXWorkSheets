from tex_code import TexDocument, compile_tex
from templates.columns import Columns
from templates.quadratics import Quadratics

if __name__ == '__main__':
    td = TexDocument()
    c = Columns()
    q = Quadratics()

    td.add_content(c)
    td.add_content(q)

    compile_tex('example.pdf', td, solutions=False, save_tex=True)
    compile_tex('example_solutions.pdf', td, solutions=True, save_tex=True)
