import string
from tkinter import *
import os
from tkinter.filedialog import asksaveasfilename, askopenfilename
import subprocess
import re

compiler = Tk(className='Mehdi Compiler')
file_path = ''
compiler.configure(bg='#565656')
menubar = Menu(compiler)
compiler.config(menu=menubar)

#     -   +   *  <   _  n   c   .  |  &  =   (
M = [[17, 12, 6, 7, -1, 9, 22, -1, 4, 2, 1, 26, -1],  # 0
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 1
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, 3, -1, -1, -1],  # 2
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 3
     [-1, -1, -1, -1, -1, -1, -1, -1, 5, -1, -1, -1, -1],  # 4
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 5
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 6
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, 8, -1, -1],  # 7
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 8
     [-1, -1, -1, -1, -1, 9, -1, 10, -1, -1, -1, -1, -1],  # 9
     [-1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1],  # 10
     [-1, -1, -1, -1, -1, 11, -1, -1, -1, -1, -1, -1, -1],  # 11
     [-1, 13, -1, -1, -1, 14, -1, -1, -1, -1, -1, -1, -1],  # 12
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 13
     [-1, -1, -1, -1, -1, 14, -1, 15, -1, -1, -1, -1, -1],  # 14
     [-1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1],  # 15
     [-1, -1, -1, -1, -1, 16, -1, -1, -1, -1, -1, -1, -1],  # 16
     [18, -1, -1, -1, -1, 19, -1, -1, -1, -1, -1, -1, -1],  # 17
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1],  # 18
     [-1, -1, -1, -1, -1, 19, -1, 20, -1, -1, -1, -1, -1],  # 19
     [-1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1],  # 20
     [-1, -1, -1, -1, -1, 21, -1, -1, -1, -1, -1, -1, -1],  # 21
     [-1, -1, -1, -1, 23, 22, 22, -1, -1, -1, -1, -1, -1],  # 22
     [-1, -1, -1, -1, 24, 22, 22, -1, -1, -1, -1, -1, -1],  # 23
     [-1, -1, -1, -1, 25, 22, 22, -1, -1, -1, -1, -1, -1],  # 24
     [-1, -1, -1, -1, 24, -1, -1, -1, -1, -1, -1, -1, -1],  # 25
     [-1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1, -1]]  # 26

def set_file_path(path):
    global file_path
    file_path = path


def open_file():
    path = askopenfilename(filetypes=[('Python Files', '*.py')])
    with open(path, 'r') as file:
        code = file.read()
        editor.delete('1.0', END)
        editor.insert('1.0', code)
        set_file_path(path)


def save_as():
    if file_path == '':
        path = asksaveasfilename(filetypes=[('Python Files', '*.py')])
    else:
        path = file_path
    with open(path, 'w') as file:
        code = editor.get('1.0', END)
        file.write(code)
        set_file_path(path)

def clearblank(s):
    s = s.replace("\n", " ")
    a = 0
    while a == 0:
        sr = s
        s = s.replace("  ", " ")
        if (sr == s):
            a = 1
    s = s.replace(" ", "#")
    return s

def comment_spaces(s):
    i = 0
    a = 0
    s = list(s)
    while (i < len(s)):
        if a == 0:
            if s[i] == "$":
                a = 1
                x = i
            i += 1
            continue
        if a == 1:
            if s[i] == "$":
                a = 0
                y = i + 1
                for j in range(x, y, 1):
                    s[j] = " "
            i += 1
    if a == 1:
        for j in range(x, len(s), 1):
            s[j] = " "
    s = "".join(s)
    #Remove spaces
    s=" ".join(s.split())
    return s

def lexicale():
    s = editor.get('1.0', END)
    s = comment_spaces(s)
    s = clearblank(s)
    s = list(s)
    i = 0
    c = '#'
    z = 'abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ'
    w = '0123456789'
    ww = ';()[]"<>*/'
    www = '0123456789.'
    oo = -10

    s.insert(len(s),c)

    while (i < len(s)):
        if s[i] == "!" or s[i] == ":":
            if s[i+1] == "=" and s[i-1] != "#":
                s.insert(i, c)
            if s[i + 1] == "=" and s[i + 2] != "#":
                s.insert(i+2, c)

        if s[i] == ">" or s[i] == "<":
            if s[i+1] == "=" and s[i-1] != "#":
                s.insert(i, c)
            if s[i + 1] == "=" and s[i + 2] != "#":
                s.insert(i+2, c)

        if s[i] == "-":
            if s[i + 1] == "-" and s[i - 1] != "#":
                s.insert(i, c)
                i += 1
            if s[i + 1] == "-" and s[i + 2] != "#" and s[i+2] not in w:
                s.insert(i + 2, c)
            if s[i + 1] == "-" and s[i + 2] != "#" and s[i+2] in w:
                s.insert(i + 1, c)

            if s[i + 1] in z and s[i - 1] != "#" and s[i - 1] != "-":
                s.insert(i, c)
            if s[i + 1] in z:
                s.insert(i + 1, c)
            if s[i + 1] in w and s[i - 1] != "-" and s[i-1] not in w:
                oo=i+1
                if s[i - 1] != "#":
                   s.insert(i, c)
                   oo = i + 2
                while (s[oo] in www):
                    if s[oo+1] not in www:
                        if s[oo + 1] != "#":
                           s.insert(oo+1,c)
                        i = oo
                    oo += 1
            if s[i + 1] in w and s[i-1] in w:
                s.insert(i, c)
                s.insert(i + 2, c)
            if s[i-1] in z and s[i+1] != "-" and s[i+1] != "#":
                s.insert(i, c)

        if s[i] == "+":
            if s[i + 1] == "+" and s[i - 1] != "#":
                s.insert(i, c)
                i += 1
            if s[i + 1] == "+" and s[i + 2] != "#" and s[i+2] not in w:
                s.insert(i + 2, c)
            if s[i + 1] == "+" and s[i + 2] != "#" and s[i+2] in w:
                s.insert(i + 1, c)
            if s[i + 1] in z and s[i - 1] != "#" and s[i - 1] != "+":
                s.insert(i, c)
            if s[i + 1] in z:
                s.insert(i + 1, c)
            if s[i + 1] in w and s[i - 1] != "+" and s[i-1] not in w:
                oo=i+1
                if s[i - 1] != "#":
                   s.insert(i, c)
                   oo = i + 2
                while (s[oo] in www):
                    if s[oo+1] not in www:
                        if s[oo + 1] != "#":
                           s.insert(oo+1,c)
                        i = oo
                    oo += 1
            if s[i + 1] in w and s[i-1] in w:
                s.insert(i, c)
                s.insert(i + 2, c)
            if s[i-1] in z and s[i+1] != "+" and s[i+1] != "#":
                s.insert(i, c)

        if s[i] in ww:
            if s[i-1] != "#" and s[i + 1] != "=":
                s.insert(i, c)
                i += 1
            if s[i + 1] != "#" and s[i + 1] != "=":
                s.insert(i+1, c)

        if s[i] == ".":
            if s[i-1] in w and s[i+1] in w:
                if s[i-2] != "#":
                    s.insert(i-1,c)
                    i += 2
                    s.insert(i+1,c)

        if s[i] == "=":
            if s[i + 1] == "=" and s[i - 1] != "#":
                s.insert(i, c)
                i += 1
            if s[i + 1] == "=" and s[i + 2] != "#":
                s.insert(i + 2, c)
            if s[i + 1] in z and s[i - 1] != "#" and s[i - 1] != "=":
                s.insert(i, c)
            if s[i + 1] in z:
                s.insert(i + 1, c)
            if s[i + 1] in w and s[i - 1] != "#" and s[i - 1] != "=":
                s.insert(i, c)
            if s[i + 1] in w:
                s.insert(i + 1, c)
            if s[i+1] != "=" and s[i-1] != "#" and s[i-1] != "!" and s[i-1] != "<" and s[i-1] != ">":
                s.insert(i, c)
            if s[i+1] != "=" and s[i+1] != "#" and s[i-1] != "!" and s[i-1] != "<" and s[i-1] != ">":
                s.insert(i + 1, c)
        i += 1
    s = ''.join(s)
    s = list(s)
    v = ""
    i = 0
    sr=""
    while (i < len(s)):
        v=v+s[i]
        if(s[i]=="#"):
            sr = sr + f"{v[:-1]}: {reconnaitre(v)}\n"
            v=""
        i=i+1
    code_output.delete('1.0', END)
    code_output.insert('1.0', s)
    code_output.insert(END,  "\n" )
    code_output.insert(END,sr)

numbers = [str(i) for i in range(0,10)]
letters = list(string.ascii_lowercase)
motscle = ["FOR"]


def dec(t):
    if(t =="-"):
        return 0
    elif(t =="+"):
        return 1
    elif t in["*","/"]:
        return 2
    elif(t in ["<",">","!",":"]):
        return 3
    elif(t=="_"):
        return 4
    elif t in numbers:
        return 5
    elif t in letters:
        return 6
    elif t==".":
        return 7
    elif t=="|":
        return 8
    elif t=="&":
        return 9
    elif t=="=":
        return 10
    elif t in ["{","}","(",")",";"]:
        return 11
    else:
        return 12
def reconnaitre(s):
    if(s[:-1] in motscle):
        return "Mot clé"
    tc = s[0]
    ec=0
    i=0
    long=0
    while ec != -1 and tc!="#":

        ec = M[ec][dec(tc)]

        i+=1
        long+=1
        tc = s[i]

    if ec == -1:
        return "Erreur"
    elif ec in [1,6,7,8,12,13,17,18]:
        return "operateur"
    elif ec in [3,5,26]:
        return "separateur"
    elif ec == 9:
        if (long <= 9):
            return "int"
        else:
            return 'Erreur'
    elif ec ==11:
        if (long <= 9):
            return "float"
        else:
            return 'Erreur'
    elif ec in[14,19]:
        if (long <= 9):
            return "signed int"
        else:
            return 'Erreur'
    elif ec in[16,21]:
        if (long <= 9):
            return "signed float"
        else:
            return 'Erreur'
    elif ec == 22:
        if(long<=9):
            return "identificateur"
        else:
            return 'Erreur'
    else:
        return 'Erreur'

def maintenance():
    cut = Toplevel()
    text = Label(cut, text='Maintenance . . Soon !')
    text.pack()


menu_bar = Menu(compiler)

file_menu = Menu(menubar, tearoff=0, font=("Comic Sans MS", 12))
file_menu.add_command(label='Open', command=open_file)
file_menu.add_command(label='Save', command=save_as)
file_menu.add_command(label='Exit', command=exit)
menu_bar.add_cascade(label='     File     ', menu=file_menu)



analyse_bar = Menu(menubar, tearoff=0, font=("Comic Sans MS", 12))
analyse_bar.add_command(label='Analyse lexicale', command=lexicale)
analyse_bar.add_command(label='Analyse syntaxique')
analyse_bar.add_command(label='Analyse sémantique ', command=maintenance)
menu_bar.add_cascade(label='     Analyse     ', menu=analyse_bar)



compiler.config(menu=menu_bar)

editor = Text(height=20, width=50)
editor.pack(padx=70, pady=60, side=LEFT, expand=TRUE, fill=BOTH)

code_output = Text(height=20, width=50)
code_output.pack(padx=70, pady=60, side=LEFT, expand=TRUE, fill=BOTH)



compiler.mainloop()