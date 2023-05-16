# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# Dependencies : Python3, Prettier with Rust plugin

import os
from IRparser import *
from language import *
from datatypes import *

header = """
#![allow(non_snake_case, dead_code, non_upper_case_globals, non_camel_case_types, unused_variables, unused_parens)]

use std::rc::Rc
use std::clone::Clone;"""

datatype_header = """use std::any::Any;

fn Rc_unwrap_or_clone<T : Clone>(rc : Rc<T>) -> T{
    Rc::try_unwrap(rc).unwrap_or_else(|rc| (*rc).clone())
}

#[derive(Clone, Debug, PartialEq)]
struct ordstruct_adt__ordstruct_adt {}

"""

isThereDatatype = False

if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    src = fichier.read()
    fichier.close()

    rust = ""
    functions = src.split("$")
    for fn in functions:
        name, code = fn.split("@")
        print(name)
        if "DATATYPE " in name:
            isThereDatatype = True
            th = name.split(" ")[3].strip(" \n")
            name = name.split(" ")[1]
            parsed = get_els_from_str(code)
            rust += datatype(parsed, name, th).toRust()
            isDatatype = True
        else:
            isDatatype = False
            parsed = get_els_from_str(code)
            rust += get_expr(parsed[0], env(), name).toRust() + "\n\n"

    if isThereDatatype:
        rust = header + datatype_header + getTypeDecl() + "\n\n" + rust
    else :
        rust = header + "\n\n" + getTypeDecl() + "\n\n" + rust
    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

