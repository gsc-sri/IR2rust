# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# Dependencies : Python3, Prettier with Rust plugin

import os
from IRparser import *
from language import *
from datatypes import *

header = """
#![allow(
    non_snake_case,
    dead_code,
    non_upper_case_globals,
    non_camel_case_types,
    unused_variables,
    unused_parens,
    unused_imports
)]

use std::rc::Rc
use std::clone::Clone;
use std::hash::Hash;
use std::collections::HashMap;
use std::any::Any;"""

datatype_header = """

fn Rc_unwrap_or_clone<T : Clone>(rc : Rc<T>) -> T{
    Rc::try_unwrap(rc).unwrap_or_else(|rc| (*rc).clone())
}

#[derive(Clone, Debug, PartialEq)]
struct ordstruct_adt__ordstruct_adt {}
"""

function_header = """

struct funtype<A: Eq + Hash, V : Clone> {
    explicit: Rc<dyn Fn(A) -> V>,
    hashtable: HashMap<A, V>,
}

impl<A: Eq + Hash, V: Clone> funtype<A, V> {
    fn new(explicit: Rc<dyn Fn(A) -> V>) -> funtype<A, V> {
        funtype {
            explicit,
            hashtable: HashMap::new(),
        }
    }
    fn lookup(&self, a: A) -> V {
        match self.hashtable.get(&a) {
            Some(v) => v.clone(),
            None => (self.explicit)(a),
        }
    }
    fn update(mut self, a: A, v: V) -> Self{
        self.hashtable.insert(a, v);
        self
    }
}"""


isThereDatatype = False

if __name__ == "__main__":
    fichier = open("IR.lisp", 'r')
    src = fichier.read()
    fichier.close()

    rust = ""
    executed_rust = "fn main() {\n"
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
        else:
            parsed = get_els_from_str(code)
            e = get_expr(parsed[0], env(), None, name)
            if isinstance(e, Efn) or isinstance(e, Evalue):
                rust += e.toRust() + "\n\n"
            else:
                executed_rust += "let " + name + " = {" + e.toRust() + "}\n\n"
    executed_rust += "}"

    out = header
    if isThereDatatype:
        out += datatype_header
    if len(FUNCTIONS) > 0:
        out += function_header
    out += "\n\n"
    out += getTypeDecl()
    out += rust
    out += executed_rust
    
    fichier = open("out.rs", "w")
    fichier.write(out)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

