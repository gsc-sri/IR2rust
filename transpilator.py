# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# Dependencies : Python3, Prettier with Rust plugin

import os
from IRparser import *
from language import *


if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    src = fichier.read()
    fichier.close()

    header = "use std::rc::Rc\nuse std::clone::Clone;\n\n#[allow(non_snake_case, dead_code, non_upper_case_globals, non_camel_case_types)]\n\n"
    rust = ""
    functions = src.split("$")
    for fn in functions:
        name, code = fn.split("@")
        parsed = get_els_from_str(code)
        rust += get_expr(parsed[0], env(), name).toRust() + "\n\n"

    rust = header + getTypeDecl() + "\n\n" + rust

    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

