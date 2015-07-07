

"""

ScrumPy -- Metabolic Modelling with Python

Copyright Mark Poolman 1995 - 2002

 This file is part of ScrumPy.

    ScrumPy is free software; you can redistribute it and/or modify
    it under the terms of the GNU General Public License as published by
    the Free Software Foundation; either version 2 of the License, or
    (at your option) any later version.

    ScrumPy is distributed in the hope that it will be useful,
    but WITHOUT ANY WARRANTY; without even the implied warranty of
    MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
    GNU General Public License for more details.

    You should have received a copy of the GNU General Public License
    along with ScrumPy; if not, write to the Free Software
    Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA

"""

####from ScrumPy.ThirdParty.Ply import lex
import lex

# some elementary regexes
Letter = r"[a-zA-Z]"

Int = r"\d+"                                                       # Integer
Dec = Int + "\." + Int                                         # Decimal
Exp = r"([E|e][\+|\-]?)" +Int                                # Exponent
Real = Dec  + "("+ Exp +")?" + "|" + Int + Exp     # Real - dec w/ optional exp or int with exp
Rat = Int+"/"+Int

NL = r"\n"





Lexer = None


DirecList = [
    "External",
    "Structural",
    "ElType",
    "AutoExtern",
    "AutoDuplicateR",
    "AutoPolymer",
    "Include",
    "DeQuote"]


MDStack =[]

def Init(ModelDesc,debug=0):
    "Not  a real token, just init everything"
    global Lexer
    MDStack.append(ModelDesc)
    Lexer = lex.lex(debug=debug)

def NewLineFunc(t):
    r"\n"
    MDStack[-1].CurLin += 1
    t.lineno = MDStack[-1].CurLin

def HashComFunc(t):
    r"\#.*\n"
    NewLineFunc(t)


def ReacIdFunc(t):
    r'([a-zA-Z]\w*:)|(".*?":)'
    t.type = "ReacId"
    t.value = t.value[:-1]  # remove the colon
    return t



def IdentFunc(t):
    r'([a-zA-Z][\.\w]*) | (".*?")'


    if t.value in DirecList:
        t.type = "Directive"
    else:
        t.type = "Ident"
        IdentList = MDStack[-1].IdList
        if t.value not in IdentList:
            IdentList.append(t.value)

    return t



tokens = ("HashCom",
          "NL",
          "DefaultKin",
          "Ident",
          "Irrev",
          "BackIrrev",
          "Rever",
          "ReacId",
          "Real",
          "Int",
          "Rat",
          "LPar",
          "RPar",
          "Add",
          "Sub",
          "Mul",
          "Div",
          "Pow",
          "Eq",
          "Comma",
          "Directive"#,
          #"Py"#,
          #"Thon"
          )


t_NL = NewLineFunc
t_HashCom = HashComFunc
t_ReacId = ReacIdFunc
t_Ident = IdentFunc
t_DefaultKin = "~"
t_Irrev = r"->"
t_BackIrrev = r"<-"
t_Rever = r"<>"
t_Real = Real
t_Int = Int
t_Rat = Rat
t_LPar = r"\("
t_RPar = r"\)"
t_Add = r"\+"
t_Sub = r"-"
t_Mul = r"\*"
t_Div = r"/"
t_Pow = "\*\*"
t_Eq = "="
t_Comma = ","
#t_Py = r"Py>"
#t_Thon = r"<Thon"
t_ignore = " \t"

def t_error(t):
    MDStack[-1].ErrList.append(("Bad character", t.lineno, t.value[0], t.type))
    t.lexer.skip(1)

def Finnish():
    MDStack.pop()
