# PVS 2 Rust PoC
# Translates the code from IR.lisp to out.rs
# Nathan Gasc - SRI International 

# Dependencies : Python3, Prettier with Rust plugin

# TODO:
# Handle arrays 
# Handle types
# Can we use Rust polymorphism for generic type ?
# Handle recordtypes :
#   (recordtype
#       ((=> (project_1 project_192) (subrange 0 * nil nil))
#        (=> (project_2 project_293) (subrange 0 * nil nil))))
#    where project_* are projections from tuples

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

    #actual translation
    header = "use rug::Integer;\n"
    rust = "use rug::Integer;\n\n" + Efn(parsed[0], [], name).toRust() 

    fichier = open("out.rs", "w")
    fichier.write(rust)
    fichier.close()

    os.system("prettier --write out.rs") # requires prettier

