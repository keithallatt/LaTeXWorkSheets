import os
import shutil
import subprocess
import tempfile

from problems import Problem


class TexDocument(Problem):
    def __init__(self):
        super().__init__()
        self.doc_class = "\\documentclass{article}\n\n"
        self.preamble = [
            r"\usepackage[english]{babel}",
            r"\usepackage[letterpaper,top=2cm,bottom=2cm,left=3cm,right=3cm,marginparwidth=1.75cm]{geometry}",
            r"\usepackage{amsmath}",
            r"\usepackage{graphicx}",
            r"\usepackage[colorlinks=true, allcolors=blue]{hyperref}",
        ]
        self.doc_begin = "\\begin{document}\n\n"

        self.body = []

        self.doc_end = "\n\n\\end{document}"

    def add_content(self, tex):
        self.body.append(tex)

    def add_package(self, package, *options):
        self.preamble.append(fr"\usepackage[{', '.join(map(str, options))}]" + "{" + str(package) + "}")

    def __str__(self, solved=False):
        return "\n\n".join([
            self.doc_class,
            "\n".join(self.preamble),
            self.doc_begin,
            "\n\\newpage\n".join(map(lambda x: x.__str__(solved) if isinstance(x, Problem) else str(x), self.body)),
            self.doc_end
        ])


def compile_tex(filename, tex, solutions=True):
    current = os.getcwd()
    tex_content = tex.__str__(solutions) if isinstance(tex, Problem) else str(tex)
    # create temp folder to compile in.
    temp_path = tempfile.mkdtemp()
    # change directory to temp folder.
    os.chdir(temp_path)

    with open('cover.tex', 'w') as f:
        f.write(tex_content)

    proc = subprocess.Popen(['pdflatex', '\\input{cover.tex}'])
    proc.communicate()
    proc = subprocess.Popen(['pdflatex', '\\input{cover.tex}'])
    proc.communicate()

    os.rename('cover.pdf', filename)
    shutil.copy(filename, current)
    shutil.rmtree(temp_path)
    os.chdir(current)
