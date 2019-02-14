import subprocess
import os
import tempfile
import shutil
import sys
if sys.platform == 'win32':
    import win32api
    import time

def makepdf(tex, pdfname, outputdir='.', printa=True):
    current = os.getcwd()
    temp = tempfile.mkdtemp()
    os.chdir(outputdir)
    outputdir = os.getcwd()
    os.chdir(temp)

    f = open('cover.tex', 'w', encoding="utf-8")
    f.write(tex)
    f.close()

    subprocess.call(['pdflatex', '-halt-on-error', 'cover.tex'], shell=False, stdout=subprocess.PIPE)

    if 'cover.pdf' in os.listdir():
        #printa
        if printa:
            if sys.platform == 'linux':
                subprocess.call(['lpr', 'cover.pdf'], shell=False)
            elif sys.platform == 'win32':
                try:
                    #TODO dont sleep
                    win32api.ShellExecute(0, 'print', 'cover.pdf', None, '.', 0)
                    time.sleep(2)
                except:
                    win32api.ShellExecute(0, 'open', 'cover.pdf', None, '.', 0)
                    time.sleep(2)
        os.rename('cover.pdf', pdfname)
        shutil.copy(pdfname, outputdir)
        os.chdir(current)
        shutil.rmtree(temp)
    else:
        os.chdir(current)
        shutil.rmtree(temp)
        raise SyntaxError('latex gevur feil')
        #TODO skal man geima loggin

def birjan():
    f = open('FA_DB_Interface/LaTeX/preamble.tex')
    out = f.read()
    f.close()
    f = open('FA_DB_Interface/LaTeX/fun.tex')
    out += f.read()
    f.close()
    return out

def endi():
    f = open('FA_DB_Interface/LaTeX/endin.tex')
    out = r"""\end{minipage}

"""
    out += f.read()
    f.close()
    return out

def midan():
    f = open('FA_DB_Interface/LaTeX/pythongenerera.tex')
    out = f.read()
    f.close()
    return out

def kjekkasyntax(ID):
    ID = str(ID).replace('\\', r'\backslash').replace('%', r'\%').replace('$', r'\$').replace('{', r'\{')\
        .replace('_', r'\_').replace('#', r'\#').replace('&', r'\&').replace('}', r'\}')
    return ID

def DepID(ID):
    return r"""\begin{document}

{\Huge Deployment ID\underline{\hspace{1cm}%s\hspace{1cm}}}\\\vspace{.5cm}

\underline{Instrument setup:}\\

\hspace{2cm}\begin{minipage}{\textwidth - 2cm}\addtolength{\baselineskip}{.5cm}""" % (kjekkasyntax(ID),)

def tveycol(parm1, val1, parm2, val2):
    return r"\tveycol{%s}{%s}{%s}{%s}" % (kjekkasyntax(parm1), kjekkasyntax(val1),
                                          kjekkasyntax(parm2), kjekkasyntax(val2))

def eincol(parm, val):
    return r"""\eincol{%s}{%s}\\
""" % (kjekkasyntax(parm), kjekkasyntax(val))


