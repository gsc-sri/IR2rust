# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# Dependencies : Python3, Prettier with Rust plugin

import os
from IRparser import *
from language import *


if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    name = fichier.readline()
    src = fichier.read()
    fichier.close()

    #uses parser to go from lisp with parenthesis, to the same but in an array structure
    parsed = get_els_from_str(src) 
    #print(parsed)
    #actual translation
    header = "use rug::Integer;\n"
    rust = "use std::rc::Rc\n\n#[allow(non_snake_case, dead_code)]\n" + Efn(parsed[0], env(), name).toRust() 

    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

