from tex_compile import compile_tex, TexDocument
from examples.problem_examples import Columns, Quadratics

if __name__ == '__main__':
    td = TexDocument()
    c = Columns()
    q = Quadratics()

    td.add_content(c)
    td.add_content(q)

    compile_tex('example.pdf', td, solutions=False)
    compile_tex('example_solns.pdf', td, solutions=True)

